# Revamp
A python library that helps in data preparation. Data cleansing steps like missing value imputation, encoding, one-hot encoding, and scaling can be performed by using this libraray.

### Installation
```
pip install revamp
```

### Get started
Prepare your tabular data for statistical analysis or predictive modeling.

```Python
from revamp import DataPreperation

# Instantiate object
transformation = DataPreperation()

# Call the object method
print(transformation.Transform(X=train, cleansing_step="all"))
```