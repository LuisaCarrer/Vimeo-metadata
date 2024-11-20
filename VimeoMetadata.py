from loguru import logger
import os
import requests
import json
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

### Configuration
VIMEO_TOKEN = os.getenv("VIMEO_TOKEN")
FOLDER_NAMES = ["brunhuber", "ward", "lemon", "blackwell", "whitaker"]

HEADERS = {
    "Accept": "application/vnd.vimeo.*+json;version=3.4",
    "Authorization": f"bearer {VIMEO_TOKEN}",
}


def fetch_vimeo_data(uri):
    """
    Fetch video metadata using Vimeo API about all videos
    """
    json_combined_data = []
    while uri:
        url = f"https://api.vimeo.com{uri}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            logger.error(f"Failed to fetch data: {response.status_code}")
            break

        ## Use metadata to get next url to access
        json_response = response.json()
        uri = json_response['paging'].get('next')

        ## Combine json metadata
        output_data = json_response['data']
        json_combined_data.extend(output_data)

    return json_combined_data


def clean_metadata(
    df,  # Panda Dataframe
    columns_to_drop = [],  # Optional list of columns to drop
    rows_to_drop = None  # Optional function to drop rows
) -> pd.DataFrame:
    """
    Drop specified columns and/or rows of a Panda table containing converted JSON metadata.

    Args:
        df: Panda DataFrame.
        columns_to_drop: List of column names to be dropped (default is an empty list).
        rows_to_drop: A function that takes a DataFrame and returns a boolean mask or row indices to drop.
    Returns:
        The DataFrame after dropping specified columns and/or rows.
    """

    # Drop rows if a row condition (function) is provided
    if rows_to_drop:
        df = df[~df.apply(rows_to_drop, axis=1)]  # Apply row condition to filter rows

    # Drop specified columns
    df.drop(columns=columns_to_drop, inplace=True)

    return df


def save_data(df, filename, columns_rename_dict = None, path = None ):
    """
    Save panda dataframe in .csv after renaming columns using dict

    Args:
        df: Panda Dataframe to be saved.
        filename: String for file name
        columns_rename_dict: Dictionary for renaming columns.
        path: Additional directory for output path
    Returns:
        The DataFrame after dropping specified columns and/or rows.
    """
    if columns_rename_dict:
        df.rename(columns=columns_rename_dict, inplace = True)

    if path:
        # Create the directory if it doesn't exist
        if not os.path.exists(path):
            os.makedirs(path)

        # generate name
        filename = os.path.join(path,filename)

    # Save panda metadata in .csv using file_path as name
    df.to_csv(filename, index=False)


if __name__ == "__main__":

    logger.info("Starting Vimeo metadata extraction...")

    initial_uri = "/me/videos?include_subfolders=true&fields=uri,name,embed.html,parent_folder.name,parent_folder.uri&sort=alphabetical&per_page=100"
    json_metadata = fetch_vimeo_data(initial_uri)

    # Normalize JSON data into a DataFrame
    panda_metadata = pd.json_normalize(json_metadata, sep='_')
    df = clean_metadata(panda_metadata,
                        columns_to_drop= [x for x in panda_metadata.columns if "parent" in x],
                        rows_to_drop = lambda row:row["parent_folder_name"] not in FOLDER_NAMES)

    # Save Panda table in .csv
    save_data(df, "VimeoIDs.csv", {"uri":"ID", "embed_html":"embed"}, "output")

    logger.info("Process completed.")




