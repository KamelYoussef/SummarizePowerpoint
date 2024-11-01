regressors = {
    "Random Forest": RandomForestRegressor(random_state=42),
    "Support Vector Regressor": SVR(kernel='linear'),
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(random_state=42),
    "K-Nearest Neighbors": KNeighborsRegressor(n_neighbors=5)
}
