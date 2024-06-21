"""Main module with DB operations."""

import os
from dotenv import load_dotenv
from queries import SQL_PROCESSING, SQL_SOLUTION_1, SQL_SOLUTION_2, SQL_SOLUTION_3
from db import DatabaseConnection
import pandas as pd

def main() -> None:
    """Main function to handle the database operations and execute SQL queries."""
    load_dotenv()
    
    # Load DB credentials from environment variables
    db_credentials = {
        'host': os.getenv('DB_HOST'),
        'port': int(os.getenv('DB_PORT')),
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
    }


    with DatabaseConnection(**db_credentials) as db:
        # Create and prepare tables
        db.execute_query(SQL_PROCESSING)
        
        # Solution 1
        solution_1_df = db.query_to_dataframe(SQL_SOLUTION_1)
        solution_1_df.to_csv('data/solution_1.csv', index=False)
        
        # Solution 2
        solution_2_df = db.query_to_dataframe(SQL_SOLUTION_2)
        solution_2_df.to_csv('data/solution_2.csv', index=False)
        
        # Left join solutions 1 and 2 on login and save to CSV
        merged_df = pd.merge(solution_1_df, solution_2_df, on='login', how='outer')
        merged_df.to_csv('data/solution_merged.csv', index=False)
        
        # Solution 3
        solution_3_df = db.query_to_dataframe(SQL_SOLUTION_3)
        solution_3_df.to_csv('data/solution_3.csv', index=False)

if __name__ == '__main__':
    main()