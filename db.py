"""Module with DB connections."""

from typing import Any
import psycopg2
import pandas as pd

class DatabaseConnection:
    """Class to handle PostgreSQL database connections."""

    def __init__(self, host: str, port: int, dbname: str, user: str, password: str):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.conn = None
        self.cursor = None

    def __enter__(self) -> Any:
        """Establish the database connection when entering the context."""
        self.conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            dbname=self.dbname,
            user=self.user,
            password=self.password
        )
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        """Close the database connection when exiting the context."""
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

    def execute_query(self, query: str) -> None:
        """Execute a single SQL query."""
        self.cursor.execute(query)
        self.conn.commit()

    def query_to_dataframe(self, query: str) -> pd.DataFrame:
        """Execute a query and return the result as a pandas DataFrame."""
        return pd.read_sql(query, self.conn)