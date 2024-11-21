conf_matrix_values <- conf_matrix$table
accuracy <- conf_matrix$overall['Accuracy']
precision <- conf_matrix$byClass['Pos Pred Value']
recall <- conf_matrix$byClass['Sensitivity']
f1_score <- 2 * (precision * recall) / (precision + recall)

# Extract counts (TP, FP, TN, FN) for a binary classification
TP <- conf_matrix_values[1, 1]
FP <- conf_matrix_values[1, 2]
TN <- conf_matrix_values[2, 2]
FN <- conf_matrix_values[2, 1]

# Start an MLflow run
mlflow_start_run()

# Log confusion matrix components as parameters
mlflow_log_param("Accuracy", accuracy)
mlflow_log_param("Precision", precision)
mlflow_log_param("Recall", recall)
mlflow_log_param("F1_Score", f1_score)
mlflow_log_param("TP", TP)
mlflow_log_param("FP", FP)
mlflow_log_param("TN", TN)
mlflow_log_param("FN", FN)

