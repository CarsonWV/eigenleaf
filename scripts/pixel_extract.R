library(png)
library(colorspace)
library(dplyr)

manifest <- read.delim("E:\\Leaf_PCA_data\\leafsnap-dataset-images.txt", header = TRUE)
leaf_image_matrix = matrix()

for (path in manifest$segmented_path[1:1000]) {
  path = file.path("E:/Leaf_PCA_data", path)
  image <- readPNG(path)
  print(as.vector(image))
}