print("Script started")
import pandas as pd
from flask import Flask, request, jsonify

from backend.features.data_processing import DataProcessor
from backend.features.hmpi_calculation import  HMPICalculation
from backend.features.basic_output import HMPIOutput

app=Flask(__name__)

processor = DataProcessor()
calculator = HMPICalculation()
outputter = HMPIOutput()

@app.route('/upload', methods=['POST'])
def upload_file():

    # Check for input file
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file=request.files['file']

    # Processing Input Data
    df=processor.load(file) 
    print("Data Loaded Successfully")


    # Calculating HMPI
    print("Running Calculation Module")
    calculator.calculate(df)
    print(df)

    # Saving output in Data Folder
    outputter.output(df)
    print("It Works")

    # Send a preview back to frontend
    return jsonify({
        'message': 'HMPI calculated successfully!',
        'rows': len(df),
        'preview': df.head(5).to_dict(orient='records')
    })


if __name__ == '__main__':
    app.run(debug=True)