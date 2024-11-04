# Load necessary libraries
library(caret)   # for train-test split
library(Metrics) # for MAE and MSE functions

# Load the dataset
df <- read.csv("montreal_house_data_500_rows.csv")

# Define the feature variables (X) and the target variable (y)
X <- df[, c("surface", "nombre_de_pieces", "age")]
y <- df$prix

# Split the dataset into training and test sets
set.seed(42) # for reproducibility
train_indices <- createDataPartition(y, p = 0.8, list = FALSE)
X_train <- X[train_indices, ]
X_test <- X[-train_indices, ]
y_train <- y[train_indices]
y_test <- y[-train_indices]

# Combine X_train and y_train into a single DataFrame for model fitting
train_data <- data.frame(X_train, prix = y_train)

# Train the linear regression model
model <- lm(prix ~ surface + nombre_de_pieces + age, data = train_data)

# Make predictions on the test set
test_data <- data.frame(X_test)
y_pred <- predict(model, newdata = test_data)

# Evaluate the model
mae <- mae(y_test, y_pred)
mse <- mse(y_test, y_pred)
rmse <- sqrt(mse)
r2 <- 1 - sum((y_test - y_pred)^2) / sum((y_test - mean(y_test))^2)

# Print evaluation metrics
cat("Model Evaluation Metrics:\n")
cat(sprintf("Mean Absolute Error (MAE): %.2f\n", mae))
cat(sprintf("Mean Squared Error (MSE): %.2f\n", mse))
cat(sprintf("Root Mean Squared Error (RMSE): %.2f\n", rmse))
cat(sprintf("R-squared (R2): %.2f\n", r2))

# Print model coefficients and intercept
cat("\nModel Coefficients:\n")
cat(sprintf("Intercept: %.2f\n", coef(model)[1]))
cat(sprintf("Surface Coefficient: %.2f\n", coef(model)["surface"]))
cat(sprintf("Nombre de Pièces Coefficient: %.2f\n", coef(model)["nombre_de_pieces"]))
cat(sprintf("Age Coefficient: %.2f\n", coef(model)["age"]))
