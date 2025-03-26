library(ggplot2)

# Create a dataframe to store both absolute and squared differences
comparison_results <- data.frame(Month = months, 
                                Abs_Difference_Mean = NA,
                                Squared_Difference_Mean = NA)

# Calculate both absolute and squared differences
for (t in 2:length(predictions)) {
  # Calculate absolute differences for each data point
  abs_diff <- abs(predictions[[1]] - predictions[[t]])
  
  # Calculate squared differences for each data point
  squared_diff <- (predictions[[1]] - predictions[[t]])^2
  
  # Store the mean of absolute and squared differences for each month comparison
  comparison_results$Abs_Difference_Mean[t] <- mean(abs_diff)
  comparison_results$Squared_Difference_Mean[t] <- mean(squared_diff)
  
  # Plot the distribution of absolute differences for the current month comparison
  ggplot(data.frame(abs_diff), aes(x = abs_diff)) +
    geom_histogram(binwidth = 0.01, fill = "blue", color = "black", alpha = 0.7) +
    geom_density(aes(y = ..density..), fill = "blue", alpha = 0.2) +
    labs(title = paste("Distribution of Absolute Differences: Month 1 vs Month", months[t]),
         x = "Absolute Difference", y = "Density") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  # Plot the distribution of squared differences for the current month comparison
  ggplot(data.frame(squared_diff), aes(x = squared_diff)) +
    geom_histogram(binwidth = 0.01, fill = "red", color = "black", alpha = 0.7) +
    geom_density(aes(y = ..density..), fill = "red", alpha = 0.2) +
    labs(title = paste("Distribution of Squared Differences: Month 1 vs Month", months[t]),
         x = "Squared Difference", y = "Density") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
}

# Display the comparison results dataframe
print(comparison_results)
