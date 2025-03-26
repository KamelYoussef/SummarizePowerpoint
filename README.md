library(ggplot2)

# Convert to long format for easier plotting
comparison_long <- reshape(comparison_results, 
                           varying = c("Abs_Difference_Mean", "Squared_Difference_Mean"), 
                           v.names = "Difference", 
                           timevar = "Type", 
                           times = c("Absolute", "Squared"), 
                           direction = "long")

# Plot
ggplot(comparison_long, aes(x = Month, y = Difference, color = Type)) +
  geom_line() +
  labs(title = "Comparison of Absolute vs Squared Differences", 
       x = "Month", 
       y = "Difference", 
       color = "Difference Type") +
  theme_minimal()
