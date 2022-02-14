library(rmarkdown)
file = list.files(pattern = ".Rmd")
render(file)
system(paste("open PCA_writeup.html"))