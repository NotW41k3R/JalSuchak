import pandas as pd
import os
from flask import send_file
from io import BytesIO

class HMPIOutput:
    def output(self, df, filename='HMPI_Results.csv'):
        """
        Returns the CSV as a BytesIO object instead of saving to disk.
        """
        buffer = BytesIO()
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        return buffer
