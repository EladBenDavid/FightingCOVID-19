import os
from config import config  # Importing the 'config' module for configuration settings
import logging
import pandas as pd
from pandasql import sqldf
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth


def calculate_humidity_and_temperature_delta():
    df = pd.read_csv(config['raw_data_file'], index_col=0)  # Read the raw data file into a DataFrame
    logging.info(f"load df {df.describe().to_string()}")  # Log information about the loaded DataFrame

    # Select the necessary columns and calculate the temperature difference from the previous day for each postal code
    q1 = "SELECT date," \
         "postal_code," \
         "avg_temperature_air_2m_f - LAG(avg_temperature_air_2m_f) OVER (PARTITION BY postal_code ORDER BY date) AS delta_temperature_previous_day," \
         "avg_humidity_relative_2m_pct - LAG(avg_humidity_relative_2m_pct) OVER (PARTITION BY postal_code ORDER BY date) AS delta_humidity_previous_day " \
         "FROM df"
    df = sqldf(q1, locals()).dropna(subset=['delta_temperature_previous_day',
                                            'delta_humidity_previous_day'])  # Perform SQL-like operations on the DataFrame
    logging.info(
        f"delta temperature previous day df {df.describe().to_string()}")  # Log information about the modified DataFrame

    for idx, postal_code in df.groupby('postal_code'):  # Group the DataFrame by postal code
        postal_code.to_json(
            f"{config['output_folder']}/{config['output_file_prefix']}{idx}{config['output_file_suffix']}.json",
            orient="records", lines=True)  # Save each postal code group as a JSON file


def upload():
    gauth = GoogleAuth()  # Initialize GoogleAuth for authentication
    gauth.LocalWebserverAuth()  # Authenticate using a local web server
    drive = GoogleDrive(gauth)  # Create a GoogleDrive instance using the authenticated GoogleAuth

    for upload_file in os.listdir(config['output_folder']):  # Iterate over files in the output folder
        if upload_file.endswith('json'):  # Check if the file is a JSON file
            cloud_file = drive.CreateFile(
                {'parents': [{'id': config['folder_id']}], 'title': upload_file})  # Create a file in Google Drive
            with open(os.path.join(config['output_folder'], upload_file)) as file:  # Open the file for reading
                data = file.read()
                cloud_file.SetContentString(data)  # Set content of the file from the read data
                cloud_file.Upload()  # Upload the file to Google Drive


if __name__ == '__main__':
    calculate_humidity_and_temperature_delta()  # Call the function to calculate humidity and temperature delta
    upload()  # Call the function to upload files to Google Drive
