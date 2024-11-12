normalize <- function(x) {
  return((x - min(x)) / (max(x) - min(x)))
}

# Apply to data frame
normalized_data <- as.data.frame(lapply(data, normalize))
