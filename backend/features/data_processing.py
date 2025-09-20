# Data Processing
# Only CSV  and XLSX initially

import pandas as pd

class DataProcessor:

    def __init__(self):
        
        # Essential metals to be checked in every dataset
        self.required_columns = ["as", "cd", "cr", "pb", "hg", "ni", "cu", "zn", "fe", "mn", "co", "al", "se", "sb", "ba", "v"]


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
            "arsenic": "as",
            "cadmium": "cd",
            "chromium": "cr",
            "copper": "cu",
            "iron": "fe",
            "manganese": "mn",
            "nickel": "ni",
            "lead": "pb",
            "zinc": "zn"
        }

    def load(self,file_input):
        # file_input='D:\Classroom\hmpi-calculator\data\datanew.csv'
        #Loading Data into a dataframe
        filename=file_input.filename.lower()
        if(filename.endswith('.csv')):
            df=pd.read_csv(file_input)
        elif(filename.endswith(('.xls','xlsx'))):
            df=pd.read_excel(file_input)
        else:
            raise ValueError("Unsupported file format. Please use an Excel or CSV file.")
        
        print(f"Loaded data shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")

        df = self.cleaning_data(df)

        return df

    def cleaning_data(self, df):
        """
        Clean and standardize a metal concentration dataset.
        Steps:
        1. Strip and normalize column names
        2. Strip and lowercase string values
        3. Normalize metal column names (full names → symbols)
        4. Convert metal columns to numeric, handle negatives and missing values
        5. Convert coordinates to numeric and filter valid ranges
        """

        # 1. Normalize column names
        df.columns = df.columns.str.strip().str.lower()
        df.rename(columns={k.lower(): v for k, v in self.column_mappings.items()}, inplace=True)
        df.rename(columns={k.lower(): v for k, v in self.metal_mappings.items()}, inplace=True)

        # 2. Strip and lowercase all string/object columns
        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].astype(str).str.strip().str.lower()
            # Convert empty strings or 'nd' to NaN
            df[col] = df[col].replace({'': pd.NA, 'nd': pd.NA})

        # 3. Convert metal columns to numeric
        for col in self.required_columns:
            if col in df.columns:
                # Strip & convert
                df[col] = pd.to_numeric(df[col], errors='coerce')
                # Replace negative values with 0
                df[col] = df[col].clip(lower=0)

        # 4. Handle coordinates if present
        if 'Latitude' in df.columns and 'Longitude' in df.columns:
            df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
            df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
            # Keep only valid coordinate ranges
            df = df[
                df['Latitude'].between(-90, 90, na=False) &
                df['Longitude'].between(-180, 180, na=False)
            ]

        return df
