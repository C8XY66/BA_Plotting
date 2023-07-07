import os
import pandas as pd
import sqlite3
import argparse
import glob

parser = argparse.ArgumentParser()
parser.add_argument("--DIR", type=str, default=None, help="directory containing sqlite database files")
args = parser.parse_args()

# Placeholder for storing all dataframes
all_dataframes = []

# Get all db files in the directory
for db_file in glob.glob(os.path.join(args.DIR, "*.db")):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)

    # Query all data from the table 'results'
    df = pd.read_sql_query("SELECT test_acc_fold from results", conn)

    # Extract database name without extension
    db_name = os.path.basename(db_file)
    db_name_no_ext = os.path.splitext(db_name)[0]

    # Split the database name into 'model', 'dataset' and 'experiment'
    model, dataset, experiment, _, _ = db_name_no_ext.split("_")

    # Shorten the experiment name
    experiment = 'wNF' if experiment == 'WithNF' else 'woNF'

    # Append experiment to the model name
    model = model + '_' + experiment

    # Add 'Model' and 'Dataset' columns
    df['Model'] = model
    df['Dataset'] = dataset

    # Append the dataframe to the list
    all_dataframes.append(df)

    # Close connection
    conn.close()

# Concatenate all dataframes
all_df = pd.concat(all_dataframes)

# Write the data to an Excel file
all_df.to_excel(os.path.join(args.DIR, 'raw_data_box_plot.xlsx'), index=False)
