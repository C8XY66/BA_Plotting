import os
import pandas as pd
import sqlite3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--PATH", type=str, default=None, help="path to sqlite database file")
args = parser.parse_args()

# Connect to the SQLite database
conn = sqlite3.connect(args.PATH)

# Query all data from the table 'results'
df = pd.read_sql_query("SELECT * from results", conn)

# Sort the DataFrame by 'rep' and then 'fold'
df = df.sort_values(by=['rep', 'fold'])

# Calculate averages and standard deviations for each rep
reps = df['rep'].unique()
for rep in reps:
    rep_df = df[df['rep'] == rep]
    avg_test_rep = rep_df['test_acc_fold'].mean()
    std_dev_test_rep = rep_df['test_acc_fold'].std(ddof=1)
    avg_val_rep = rep_df['best_val_acc'].mean()
    std_dev_val_rep = rep_df['best_val_acc'].std(ddof=1)

    # Update the last row of each rep with the calculated values
    df.loc[(df['rep'] == rep) & (df['fold'] == rep_df['fold'].max()), 'avg_test_rep'] = avg_test_rep
    df.loc[(df['rep'] == rep) & (df['fold'] == rep_df['fold'].max()), 'std_dev_test_rep'] = std_dev_test_rep

    df.loc[(df['rep'] == rep) & (df['fold'] == rep_df['fold'].max()), 'avg_val_rep'] = avg_val_rep
    df.loc[(df['rep'] == rep) & (df['fold'] == rep_df['fold'].max()), 'std_dev_val_rep'] = std_dev_val_rep

# Calculate overall averages and standard deviations
avg_test_overall = df['test_acc_fold'].mean()
std_dev_test_overall = df['test_acc_fold'].std(ddof=1)
avg_val_overall = df['best_val_acc'].mean()
std_dev_val_overall = df['best_val_acc'].std(ddof=1)

# Set the overall averages and standard deviations for last fold of last rep
df.loc[(df['rep'] == reps.max()) & (df['fold'] == df[df['rep'] == reps.max()]['fold'].max()), 'avg_test_overall'] = avg_test_overall
df.loc[(df['rep'] == reps.max()) & (df['fold'] == df[df['rep'] == reps.max()]['fold'].max()), 'std_dev_test_overall'] = std_dev_test_overall
df.loc[(df['rep'] == reps.max()) & (df['fold'] == df[df['rep'] == reps.max()]['fold'].max()), 'avg_val_overall'] = avg_val_overall
df.loc[(df['rep'] == reps.max()) & (df['fold'] == df[df['rep'] == reps.max()]['fold'].max()), 'std_dev_val_overall'] = std_dev_val_overall

# Get the directory of the database file
db_dir = os.path.dirname(args.PATH)

# Create the Excel file path
db_name = os.path.basename(args.PATH)
db_name_no_ext = os.path.splitext(db_name)[0]
excel_file_name = db_name_no_ext + '.xlsx'
excel_path = os.path.join(db_dir, excel_file_name)

# Write the data to an Excel file
df.to_excel(excel_path, index=False)

# Close connection
conn.close()
