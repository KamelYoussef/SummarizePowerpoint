# Create a dataframe to store both absolute and squared differences
comparison_results <- data.frame(Month = months, 
                                Abs_Difference_Mean = NA,
                                Squared_Difference_Mean = NA)

# Calculate both absolute and squared differences
for (t in 2:length(predictions)) {
  comparison_results$Abs_Difference_Mean[t] <- mean(abs(predictions[[1]] - predictions[[t]]))
  comparison_results$Squared_Difference_Mean[t] <- mean((predictions[[1]] - predictions[[t]])^2)
}

# Display results
print(comparison_results)
