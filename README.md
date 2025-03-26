# Initialize result dataframe for absolute difference
abs_diff_results <- data.frame(Month = months, Abs_Difference_Mean = NA)

for (t in 2:length(predictions)) {
  # Compute the absolute difference between the first month's predictions and each subsequent month's predictions
  abs_diff_results$Abs_Difference_Mean[t] <- mean(abs(predictions[[1]] - predictions[[t]]))
}

# Display results
print(abs_diff_results)
