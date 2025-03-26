# Perform KS-test to compare the distributions of anomaly scores for each month
ks_results <- data.frame(Month = months, KS_p_value = NA)

for (t in 2:length(predictions)) {
  ks_results$KS_p_value[t] <- ks.test(predictions[[1]], predictions[[t]])$p.value
}

# Display results
print(ks_results)
