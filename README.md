# Create a list of prediction variable names
month_names <- paste0("pred_", 202301:202412)

# Retrieve all predictions into a list
predictions <- mget(month_names)

# Initialize results dataframe
results <- data.frame(
  Month = 202301:202412,
  Pearson_Correlation = NA
)

# Compute Pearson correlation for each month compared to January 2023 model
for (t in 2:length(predictions)) {
  results$Pearson_Correlation[t] <- cor(predictions[[1]], predictions[[t]], method = "pearson")
}

# Print results
print(results)
