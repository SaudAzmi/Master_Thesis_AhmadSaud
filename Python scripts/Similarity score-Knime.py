import pandas as pd
from fuzzywuzzy import fuzz

# Define a function to calculate the similarity between Stackoverflow and OpenAI responses
def calculate_similarity(row):
    return fuzz.ratio(row['Stackoverflow_response'], row['OpenAI_response'])

# Apply the calculate_similarity function to each row to compute the similarity score
# and create a new column 'SimilarityScore' to store these scores
input_table_1['SimilarityScore'] = input_table_1.apply(calculate_similarity, axis=1)

# Assign the modified DataFrame to 'output_table_1' to pass it back to the main KNIME workflow
output_table_1 = input_table_1
