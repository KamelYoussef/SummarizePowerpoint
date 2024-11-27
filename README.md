# Function to calculate Silhouette Score using anomaly scores directly
calculate_silhouette_using_scores <- function(anomaly_scores) {
  # Convert anomaly scores to binary labels (0 = normal, 1 = anomaly)
  threshold <- quantile(anomaly_scores, 0.95)  # Top 5% considered anomalies
  labels <- ifelse(anomaly_scores >= threshold, 1, 0)  # Binary classification
  
  # Compute silhouette score based on these labels
  sil_score <- silhouette(labels, dist(data[, c("amount", "category")]))  # Calculate Silhouette Score
  return(mean(sil_score[, 3]))  # Return average silhouette width
}

# Define a range of ntrees values
ntrees_values <- c(50, 100, 150, 200, 250)

# Initialize an empty list to store results
results <- data.frame(ntrees = ntrees_values, silhouette_score = numeric(length(ntrees_values)))

# Iterate over different ntrees values
for (i in seq_along(ntrees_values)) {
  # Initialize Isolation Forest with the current ntrees value
  iso_forest <- isolationForest$new(ntrees = ntrees_values[i])
  iso_forest$fit(data[, c("amount", "category")])  # Use relevant features only
  
  # Get anomaly scores
  anomaly_scores <- iso_forest$predict(data[, c("amount", "category")])$anomaly_score
  
  # Calculate Silhouette Score using the anomaly scores
  silhouette_score <- calculate_silhouette_using_scores(anomaly_scores)
  
  # Store the result
  results$silhouette_score[i] <- silhouette_score
}

# Print the results
print(results)
