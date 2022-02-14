library(dplyr)

# Folder you're dumping your image files into.
#old_folder <- file.path("E:", "Leaf_PCA_data", "new")
old_folder <- file.path("E:", "Leaf_PCA_data", "dataset", "segmented")
new_folder <- file.path("E:", "Leaf_PCA_data", "2021-12-04_segmented_RESIZED")
target_file_type <- "*.png"
file_name <- "image.png"
resize_dimensions <- "700x700"

# Remove the parent folders from the list.
species_folders <- tibble(paths = list.dirs(old_folder)) %>%
  filter(!(basename(paths) %in% c("lab", "field", "dataset", "segmented", "new")))

for (current_folder in species_folders$paths) {
  destination <- file.path(new_folder, basename(current_folder))
  if (!dir.exists(destination)) {
    print(paste0("Created DIR:", destination))
    dir.create(destination)
  }
  command <- paste("E: &&",  
                   "cd", paste0('"', current_folder, '"'),
                   "&&",
                   "magick", target_file_type, 
                   "-background black",
                   "-gravity center",
                   "-extent", resize_dimensions,
                   paste0('"', file.path(destination, file_name), '"'))
  print(command)
  shell(command)
}