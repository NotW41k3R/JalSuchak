#HMPI Calculations

import pandas as pd

class HMPICalculation:

    def __init__(self):
        # Defining standards
        self.standards = {
            'As': {'S': 0.01, 'W': 100,   'I': 0},
            'Cd': {'S': 0.003, 'W': 333.3, 'I': 0},
            'Cr': {'S': 0.05, 'W': 20,    'I': 0},
            'Pb': {'S': 0.01, 'W': 100,   'I': 0},
            'Hg': {'S': 0.001, 'W': 1000,  'I': 0},
            'Ni': {'S': 0.02, 'W': 50,    'I': 0},
            'Cu': {'S': 1.5, 'W': 0.67,   'I': 0},
            'Zn': {'S': 3, 'W': 0.33,     'I': 0},
            'Fe': {'S': 0.3, 'W': 3.33,   'I': 0},
            'Mn': {'S': 0.1, 'W': 10,     'I': 0},
            'Co': {'S': 0.05, 'W': 20,    'I': 0},
            'Al': {'S': 0.2, 'W': 5,      'I': 0},
            'Se': {'S': 0.01, 'W': 100,   'I': 0},
            'Sb': {'S': 0.005, 'W': 200,   'I': 0},
            'Ba': {'S': 0.7, 'W': 1.43,   'I': 0},
            'V': {'S': 0.05, 'W': 20,     'I': 0}
            }

    def calculate(self,df):
        hmpi_list=[]
        for index, row in df.iterrows():
            num=0
            den=0
            for metal, vals in self.standards.items():
                Mi = row.get(metal,0)
                Si = vals['S']
                Ii = vals['I']
                Wi = vals['W']
                
                Qi=100*(Mi-Ii)/(Si-Ii)
                num+= Wi*Qi
                den+= Wi
            hmpi=num/den
            hmpi_list.append(hmpi)
        
        df['HMPI']=hmpi_list
        return df