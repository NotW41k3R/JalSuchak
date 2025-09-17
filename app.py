print("Script started")  # Add this line at the top
import pandas as pd

from backend.features.data_processing import DataProcessor

processor = DataProcessor()

df=processor.load('D:\Classroom\hmpi-calculator\data\datanew.csv')


print("Loaded DataFrame shape:", df.shape)
print(df.head())
print(df)

print("Hello")