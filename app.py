print("Script started")
import pandas as pd
from flask import Flask, request, jsonify, render_template

from backend.features.data_processing import DataProcessor
from backend.features.hmpi_calculation import  HMPICalculation
from backend.features.basic_output import HMPIOutput

app=Flask(__name__)

processor = DataProcessor()
calculator = HMPICalculation()
outputter = HMPIOutput()

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():

    # Check for input file
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file=request.files['file']

    # Processing Input Data
    df=processor.load(file) 
    print("Data Loaded Successfully")

    # Send a preview back to frontend
    return jsonify({
            'message': 'File uploaded and cleaned successfully!',
            'rows': len(df),
            'columns': list(df.columns),
            'preview': df.to_dict(orient='records')
        })

@app.route('/calculate', methods=['POST'])
def calculate_hmpi():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    df = processor.load(file)

    # Calculating HMPI
    print("Running Calculation Module")
    df = calculator.calculate(df)
    print(df)

    # Saving output in Data Folder
    outputter.output(df)
    print("It Works")

    return jsonify({
        'message': 'HMPI calculated successfully!',
        'rows': len(df),
        'columns': list(df.columns),
        'preview': df.to_dict(orient='records')
        })

if __name__ == '__main__':
    app.run(debug=True)