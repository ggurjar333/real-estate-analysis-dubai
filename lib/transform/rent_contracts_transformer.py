import pandas as pd
import pyarrow as pa

import pyarrow.parquet as pq

class RentContractsTransformer:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file

    def transform(self):
        # Read the CSV file
        df = pd.read_csv(self.input_file)

        # Separate string and numeric columns
        string_columns = df.select_dtypes(include=['object']).columns.tolist()
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

        # Reorder columns
        df = df[string_columns + numeric_columns]

        # Convert DataFrame to Apache Arrow Table
        table = pa.Table.from_pandas(df)

        # Write to Parquet file with heavy compression
        pq.write_table(table, self.output_file, compression='BROTLI')
        