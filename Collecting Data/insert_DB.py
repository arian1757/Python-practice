import psycopg2
from psycopg2.extras import execute_values
from sqlalchemy import create_engine

class SaveToDB:
    def __init__(self):
        self.last_timestamp = 0
        self.connection = None
        self.connection_string=""
        self.engine=None

    def check_df(self, df):
        # Find the index of the first row where timestamp is greater than last_timestamp
        first_index_to_save = df[df['timestamp'] > self.last_timestamp].index.min()
        df = df.loc[first_index_to_save:].copy()

        # Update last_timestamp to the maximum timestamp in the selected rows
        self.last_timestamp = df['timestamp'].max()

        return df
    
    def initialize_database(self):
        db_params = {
            'dbname': 'hft',
            'user': 'postgres',
            'password': 'your_password',
            'host': 'localhost',
            'port': '5432'
        }
        
        try:
            # Establish a connection to the PostgreSQL database
            self.connection = psycopg2.connect(**db_params)

            self.connection_string = f"postgresql+psycopg2://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['dbname']}"
            self.engine = create_engine(self.connection_string)
            print("Connection to the database established successfully.")

        except Exception as e:
            print("Error:", e)

    def save_to_database(self, table_name, df):
        df = self.check_df(df)

        try:
            # Use the to_sql method to insert DataFrame into SQL table
            df.to_sql(name=table_name, con=self.engine, if_exists='append', index=False)

            # Commit the transaction
            self.connection.commit()

            print(f"{len(df)} rows inserted successfully!")

        except Exception as e:
            print("Error:", e)

    def close_database(self):
        if self.connection is not None:
            self.connection.close()
            print("Connection to the database closed.")
