library(transport)

# Calculate Wasserstein Distance
wasserstein_results <- data.frame(Month = months, Wasserstein_Distance = NA)

for (t in 2:length(predictions)) {
  wasserstein_results$Wasserstein_Distance[t] <- wasserstein1d(predictions[[1]], predictions[[t]])
}

# Display results
print(wasserstein_results)
