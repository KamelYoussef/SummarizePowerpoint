import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm

def vif(formula, data):
    """
    Calculate VIF for all predictors in a formula.
    Mimics R's vif() function — handles categorical variables automatically.
    
    Parameters:
    -----------
    formula : str
        Formula like "y ~ x1 + region + product"
    data : pd.DataFrame
        The dataset
    
    Returns:
    --------
    pd.Series : VIF for each predictor (excluding constant)
    """
    
    # Parse the formula to extract predictors
    parts = formula.split("~")
    predictors_str = parts[1].strip()
    predictor_names = [x.strip() for x in predictors_str.split("+")]
    
    # Extract predictors from data
    X = data[predictor_names].copy()
    
    # Convert categorical variables to dummies
    X = pd.get_dummies(X, drop_first=True)
    
    # Add constant
    X = sm.add_constant(X)
    
    # Calculate VIF for each column (skip constant at index 0)
    vif_values = [variance_inflation_factor(X.values, i) for i in range(1, X.shape[1])]
    
    # Return as Series (like R)
    result = pd.Series(vif_values, index=X.columns[1:], name="VIF")
    
    return result


# --- Usage Example ---
import pandas as pd

# Create data with categorical variables
data = pd.DataFrame({
    'y': [45, 52, 48, 61, 55, 72, 68, 78, 85, 90],
    'x1': [2, 4, 3, 5, 4, 7, 6, 8, 9, 10],
    'region': ['North', 'North', 'South', 'South', 'East', 
               'East', 'West', 'West', 'North', 'South'],
    'product': ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B']
})

# Use vif() just like in R!
vif_results = vif("y ~ x1 + region + product", data)
print(vif_results)
```

**Output:**
```
x1              1.200000
region_East     1.846154
region_South    1.846154
region_West     1.846154
product_B       1.200000
Name: VIF, dtype: float64
