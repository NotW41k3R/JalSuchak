print("Script started")
import pandas as pd

from backend.features.data_processing import DataProcessor
from backend.features.hmpi_calculation import  HMPICalculation
from backend.features.basic_output import HMPIOutput

# Processing Input Data
processor = DataProcessor()
df=processor.load('data/data_excel.xlsx') 
print("Data Loaded Successfully")


# Calculating HMPI
print("Running Calculation Module")
HMPICalculation().calculate(df)
print(df)

# Saving output in Data Folder
HMPIOutput().output(df)

print("It Works")