# ================= 模拟数据集 =================

# 加载一些包
library(edgeR)
library(Matrix)
library(splatter)
library(scater)
library(Seurat)


# function 2 : 主要负责生成模拟数据集
# the function generating the simulation data using bioconductor package Splatter
generate_simulation_splatter <- function(dropout_index, params_list){
  # Parameter in the function
  # dropout_index: the index of dropout_mid to control the dropout rate
  # seed_value: the random seed
  # nGenes: the number of genes in the simulation data.
  
  # Set up the parameters
  params = newSplatParams()
  params = setParams(params, list(batchCells = params_list$nCells,
                                  nGenes = params_list$nGenes,
                                  group.prob = params_list$group.prob,
                                  de.prob = params_list$de.prob,
                                  de.facLoc = params_list$de.facLoc,
                                  de.facScale = params_list$de.facScale)
  )
  # determine if it is a good parameter
  if(dropout_index > length(params_list$dropout_mid)){
    stop(
      paste0('The dropout_index shold not be greater than ', 
             length(params_list$dropout_mid), 
             ' . Please input a proper one.\n')
    )
  }
  # Generate the simulation data using Splatter package
  sim = splatSimulateGroups(params,
                            dropout.type = "experiment",
                            dropout.shape = params_list$dropout.shape,
                            dropout.mid = params_list$dropout_mid[dropout_index],
                            seed = params_list$seed_value)
  
  # genereate the cpm levels of the true simulation data
  # 生成真实模拟数据的cpm水平
  data_true = (assay(sim, "TrueCounts"))
  data_dropout = data_true
  # generate the dropout data based on the counts in sim
  data_dropout[as.matrix(counts(sim)) == 0] = 0
  # calculate the dropout rate
  percentage_zeros = round(nnzero(data_dropout == 0, na.counted = NA)/
                             (dim(data_dropout)[1]*dim(data_dropout)[2])*100)
  # generate the bulk RNAseq data
  data_bulk = data.frame(val = rowMeans(data_true))
  
  
  # define the data list for the simulation data
  # indcluding: data_true: true data
  #          data_dropout: dropout data
  #             data_bluk: bulk data
  #      percentage_zeros: dropout rate
  #                 group: the group label
  data = list()
  data$data_true = data_true
  data$data_dropout = data_dropout
  data$data_bulk = data_bulk
  data$percentage_zeros = percentage_zeros
  data$group = colData(sim)@listData$Group
  return(data)
}


# function 1 : 主要负责将生成的模拟数据集信息以rds保存
# generate the simulation data and save the data
generate_save_data <- function(dropout_index, params_list){
  # Parameter in the function
  # dropout_index: the index of dropout_mid to control the dropout rate
  # seed_value: the random seed
  
  # generate the simulation data
  data_simulation = generate_simulation_splatter(dropout_index, params_list)
  
  # generate the folder saving the simulation data
  dir.create(file.path('simulation_data'), showWarnings = FALSE)
  
  # save the data as RDS format
  saveRDS(data_simulation, 
          file = paste0('simulation_data/simulation_data_dropout_index_',
                        dropout_index, 
                        '_seed_', 
                        params_list$seed_value,
                        '.rds')
  )
}

# function 3 : 主要负责将已经生成的模拟数据集信息(rds)转为csv文件并保存
preprocess_simulation_data_rds_to_csv <- function(dropout_index, seed_value, executed, if_normalize_data){
  filename <- paste("simulation_data\\simulation_data_dropout_index_", dropout_index, "_seed_", seed_value, ".rds", sep = "")
  # 读取生成的数据集的rds文件
  loaded_data <- readRDS(filename)
  # 只执行一次if 中的代码
  if (executed){
    print("====已执行if中代码====")
    # # 查看加载的数据结构
    # # str(loaded_data)
    # # 访问 data_bulk
    # # bulk_data <- loaded_data$data_bulk
    # 读取完整数据集（无缺失）
    true_data <- loaded_data$data_true
    write.csv(true_data, "complete_data.csv")
    if (if_normalize_data){
      # 归一化完整数据集
      normalize_true_data <- NormalizeData(true_data, normalization.method = "LogNormalize", scale.factor = 10000)
      write.csv(normalize_true_data, "normalize_complete_data.csv")
    }
    # 读取真实细胞类型
    cell_groups <- loaded_data$group
    write.csv(cell_groups, "labels.csv")
  }
  # 缺失概率
  zeros_percentage <- loaded_data$percentage_zeros
  print(paste(dropout_index, "生成的模拟数据集缺失概率为:", zeros_percentage, "%"))
  # 读取缺失数据集（缺失）
  dropout_data <- loaded_data$data_dropout
  # 缺失数据保存的文件名
  dropout_data_tosave_path = paste("simulation_data_dropout_index_", dropout_index, "_seed_", seed_value, "_", zeros_percentage, ".csv", sep = "")
  write.csv(dropout_data, dropout_data_tosave_path)
  if(if_normalize_data){
    # # 归一化缺失数据集
    # normalize_dropout_data <- NormalizeData(dropout_data, normalization.method = "LogNormalize", scale.factor = 10000)
    # normalize_dropout_data_tosave_path = paste("normalize_simulation_data_dropout_index_", dropout_index, "_seed_", seed_value, "_", zeros_percentage, ".csv", sep = "")
    # write.csv(normalize_dropout_data, normalize_dropout_data_tosave_path)
    
    # 归一化缺失数据集
    # Create a Seurat object with the dropout data
    seurat_object <- CreateSeuratObject(counts = dropout_data, project = "SCRNA_SEQ")
    # Normalize the Seurat object
    seurat_object <- NormalizeData(seurat_object, normalization.method = "LogNormalize", scale.factor = 10000)
    # Scale the Seurat object
    seurat_object <- ScaleData(seurat_object, features = rownames(seurat_object))
    # 提取归一化后的数据
    normalized_data <- GetAssayData(seurat_object, slot = "data")
    # 将矩阵转换为数据框，以便导出为 CSV 文件
    normalized_data_df <- as.data.frame(as.matrix(normalized_data))
    # Save the normalized data to a CSV file
    normalize_dropout_data_tosave_path <- paste("normalize_simulation_data_dropout_index_", dropout_index, "_seed_", seed_value, "_", zeros_percentage, ".csv", sep = "")
    write.csv(normalized_data_df, normalize_dropout_data_tosave_path, row.names = TRUE)
  }
}


# function 4 : 主要负责备份参数信息到txt文件里
write_parameters_to_file <- function(filename, params_list) {
  # Get current date and time
  current_datetime <- format(Sys.time(), "%Y-%m-%d %H:%M:%S")
  
  # Write parameters to a text file
  cat("Parameter Information:\n", file = filename, append = FALSE)
  cat(sprintf("simulate data time: %s\n", current_datetime), file = filename, append = TRUE)
  
  # Iterate over params_list and write each parameter
  for (param_name in names(params_list)) {
    param_value <- params_list[[param_name]]
    if (is.numeric(param_value)) {
      cat(sprintf("%s: %s\n", param_name, paste(param_value, collapse = ", ")), file = filename, append = TRUE)
    } else if (is.integer(param_value)) {
      cat(sprintf("%s: %d\n", param_name, param_value), file = filename, append = TRUE)
    } else if (is.character(param_value)) {
      cat(sprintf("%s: %s\n", param_name, param_value), file = filename, append = TRUE)
    } else if (is.logical(param_value)) {
      cat(sprintf("%s: %s\n", param_name, ifelse(param_value, "TRUE", "FALSE")), file = filename, append = TRUE)
    } else if (is.vector(param_value)) {
      cat(sprintf("%s: %s\n", param_name, paste(param_value, collapse = ", ")), file = filename, append = TRUE)
    } else {
      cat(sprintf("%s: %s\n", param_name, "Unsupported type"), file = filename, append = TRUE)
    }
  }
}


# ===以上为定义的函数，以下为需要执行的命令或代码===

params_list <- list(
  seed_value = 10086,
  nCells = 3000,
  nGenes = 1500,
  group.prob = c(0.1, 0.1, 0.2, 0.1, 0.1, 0.2, 0.2),
  de.prob = c(0.045, 0.045, 0.045, 0.045, 0.045, 0.045, 0.045),
  de.facLoc = 0.1,
  de.facScale = 0.4,
  dropout_mid = c(0.2, 1, 2, 3, 4),
  running_times = c(1, 2, 3, 4, 5),
  dropout.shape = -1
)

# save some parameters in a file
param_file <- "parameter_info.txt"
write_parameters_to_file(param_file, params_list)

# simulate data
for (dropout_index in params_list$running_times) {
  generate_save_data(dropout_index, params_list)
}


executed <- TRUE 
if_normalize_data = TRUE
for (dropout_index in params_list$running_times){
  preprocess_simulation_data_rds_to_csv(dropout_index, params_list$seed_value, executed, if_normalize_data)
  executed <- FALSE
}
print("模拟数据集生成完成")


# ================= 模拟数据集 =================