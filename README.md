# Initialize result dataframe for squared difference
squared_diff_results <- data.frame(Month = months, Squared_Difference_Mean = NA)

for (t in 2:length(predictions)) {
  # Compute the squared difference between the first month's predictions and each subsequent month's predictions
  squared_diff_results$Squared_Difference_Mean[t] <- mean((predictions[[1]] - predictions[[t]])^2)
}

# Display results
print(squared_diff_results)
