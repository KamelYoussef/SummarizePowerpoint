# Generate valid month-year sequence
months <- format(seq(as.Date("2023-01-01"), as.Date("2024-12-01"), by = "month"), "%Y%m")

# Retrieve predictions dynamically
predictions <- mget(paste0("pred_", months))

# Initialize results dataframe
results <- data.frame(
  Month = months,
  Pearson_Correlation = NA
)

# Compute Pearson correlation for each month compared to January 2023
for (t in 2:length(predictions)) {
  results$Pearson_Correlation[t] <- cor(predictions[[1]], predictions[[t]], method = "pearson")
}

# Print results
print(results)
