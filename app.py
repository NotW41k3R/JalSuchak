print("Script started")  # Add this line at the top
import pandas as pd

from backend.features.data_processing import DataProcessor
from backend.features.hmpi_calculation import  HMPICalculation

# Processing Input Data
processor = DataProcessor()
df=processor.load('data/datanew.csv') 
print("Loaded DataFrame shape:", df.shape)
print(df)
print("Data Loaded Successfully")


# Calculating HMPI
print("Running Calculation Module")
HMPICalculation().calculate(df)
print(df)

print("It Works")