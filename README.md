library(philentropy)

# Initialize result dataframe
kl_results <- data.frame(Month = months, KL_Divergence = NA)

for (t in 2:length(predictions)) {
  # Normalize histograms for comparison
  hist1 <- hist(predictions[[1]], breaks = 50, plot = FALSE)$density
  hist2 <- hist(predictions[[t]], breaks = 50, plot = FALSE)$density
  
  # Compute KL Divergence (to prevent negative values, we use JSD)
  kl_results$KL_Divergence[t] <- KL.divergence(hist1, hist2)
}

# Display results
print(kl_results)
