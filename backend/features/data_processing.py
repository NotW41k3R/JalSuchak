# Data Processing
# Only CSV  and XLSX initially

import pandas as pd

class DataProcessor:

    def __init__(self):
        
        # Essential metals to be checked in every dataset
        self.required_columns = [
            "As", "Cd", "Cr", "Pb", "Hg", "Ni", "Cu", "Zn", "Fe", "Mn", "Co", "Al", "Se", "Sb", "Ba", "V"
        ]

        # Optional Data
        self.optional_columns = [
            "Sample_ID", "Latitude", "Longitude", "Location", "Date_Collected"
        ]

        # Normalize common variations of column names
        self.column_mappings = {
            # Samples
            "sample_id": "Sample_ID",
            "sampleid": "Sample_ID",
            "id": "Sample_ID",
            "sample": "Sample_ID",

            # Geo-Coordinates
            "lat": "Latitude",
            "latitude": "Latitude",
            "lon": "Longitude",
            "lng": "Longitude",
            "long": "Longitude",
            "longitude": "Longitude",

            # Site or locations
            "location": "Location",
            "site": "Location",
            "place": "Location",

            # Dates
            "date": "Date_Collected",
            "date_collected": "Date_Collected",
            "sampling_date": "Date_Collected",
            "collection_date": "Date_Collected"
        }

        # Map full names of metals to their standard symbols
        self.metal_mappings = {
            "arsenic": "As",
            "cadmium": "Cd",
            "chromium": "Cr",
            "copper": "Cu",
            "iron": "Fe",
            "manganese": "Mn",
            "nickel": "Ni",
            "lead": "Pb",
            "zinc": "Zn"
        }

    def load(self,file_input):
        # file_input='D:\Classroom\hmpi-calculator\data\datanew.csv'
        #Loading Data into a dataframe
        filename=str(file_input).lower()
        if(filename.endswith('.csv')):
            df=pd.read_csv(file_input)
        elif(filename.endswith(('.xls','xlsx'))):
            df=pd.read_excel(file_input)
        else:
            raise ValueError("Unsupported file format. Please use an Excel or CSV file.")
        
        print(f"Loaded data shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")

        return df
    
    # def cleaning_data(self, df):
    #     df.columns = df.columns.str.strip() #removing leading and trailing spaces
        
