import pandas as pd
from truEstimate.services import EstimateService
from truEstimate.models import Preprocessor
import json

def csv_to_json(csv_path, json_path):
    """
    Reads a CSV file and writes it as a JSON file.
    """
    df = pd.read_csv(csv_path)
    df.to_json(json_path, orient='records', indent=4)
    print(f"Converted CSV {csv_path} to JSON {json_path}")

def json_to_csv(json_path, csv_path):
    """
    Reads a JSON file and writes it as a CSV file.
    """
    df = pd.read_json(json_path)
    df.to_csv(csv_path, index=False)
    print(f"Converted JSON {json_path} to CSV {csv_path}")

import pandas as pd
import numpy as np

def preprocess_csv(csv_path, output_path=None):
    """
    Loads CSV, drops rows with missing values,
    fills missing values (just in case), drops duplicates,
    applies Preprocessor transformations, and returns DataFrame.
    """
    df = pd.read_csv(csv_path)
    
    # Drop rows with any missing values (strict)
    df.dropna(inplace=True)
    
    # # Fill missing numerical values with median (if any left)
    # numeric_cols = df.select_dtypes(include='number').columns
    # for col in numeric_cols:
    #     df[col].fillna(df[col].median(), inplace=True)
    
    # # Fill missing categorical values with mode (if any left)
    # categorical_cols = df.select_dtypes(include='object').columns
    # for col in categorical_cols:
    #     df[col].fillna(df[col].mode()[0], inplace=True)
    
    # Drop exact duplicates
    df.drop_duplicates(inplace=True)
    
    # Now apply Preprocessor fit and transform
    preprocessor = Preprocessor({'cagr':[0,15],'projectLandArea':[0,100]})
    
    # Convert DataFrame to list of dicts for Preprocessor input
    data_dicts = df.to_dict(orient='records')
    
    
    # Apply preprocessing to each row
    processed_data = [preprocessor.preprocess_property(d) for d in data_dicts]
    
    # Convert back to DataFrame
    processed_df = pd.DataFrame(processed_data)
    
    if output_path:
        processed_df.to_csv(output_path, index=False)
        print(f"Processed CSV saved to: {output_path}")
    
    return processed_df

def calculate_true_estimate_for_csv(csv_path, output_path, k=5):
    """
    Calculate trueEstimate for every property in the CSV using similarity model.
    Saves output CSV with an additional 'trueEstimate' column.
    
    Args:
        csv_path (str): Input CSV file path.
        output_path (str): Output CSV file path to save results.
        k (int): Number of neighbors or parameter for similarity.
    """
    # Load CSV
    df = pd.read_csv(csv_path)
    
    # Initialize preprocessing and similarity models
    estimate_service = EstimateService('truEstimate/data/rtm_properties.json')
    
    # Calculate trueEstimate for each row
    estimates = []
    for _, row in df.iterrows():
        prop_dict = row.to_dict()
        estimate = estimate_service.estimate_price(prop_dict)
        estimates.append(estimate)
    
    # Add estimates to DataFrame
    df['trueEstimate'] = estimates
    
    # Save results
    df.to_csv(output_path, index=False)
    print(f"Saved estimated results to {output_path}")

calculate_true_estimate_for_csv(r"C:\Users\deepa\OneDrive\Documents\truEstate\propertyDatanewlaunch.csv",r"C:\Users\deepa\OneDrive\Documents\truEstate\propertyDatanewlaunch1.csv")