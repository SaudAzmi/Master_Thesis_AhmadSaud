# List all non-standard packages to be imported by your 
# script here (only missing packages will be installed)
from ayx import Package
#Package.installPackages(['pandas','numpy'])
!pip install fuzzywuzzy


from fuzzywuzzy import fuzz
import pandas as pd
from ayx import Alteryx

# Read data from the input anchor
input_data = Alteryx.read("#1")

# Convert the input data to a DataFrame
df = pd.DataFrame(input_data)

def calculate_similarity(row):
    return fuzz.ratio(row['OA_ANSWERS'], row['SO_ANSWERS'])

# Assuming your columns are named 'OA_ANSWERS' and 'SO_ANSWERS'
df['SimilarityScore'] = df.apply(calculate_similarity, axis=1)

# Output the DataFrame to the output anchor
Alteryx.write(df, 1)
