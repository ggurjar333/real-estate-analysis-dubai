import polars as pl

class RentContractsTransformer:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file

    def transform(self):
        # Read the CSV file
        df = pl.read_csv(self.input_file, null_values="null")
        print(df.head(5))

        # Separate string and numeric columns
        string_columns = [col for col, dtype in zip(df.columns, df.dtypes) if dtype == pl.Utf8]
        numeric_columns = [col for col, dtype in zip(df.columns, df.dtypes) if dtype in [pl.Int32, pl.Float64]]

        # Reorder columns
        df = df.select(string_columns + numeric_columns)
        print(df.head(10))

        # Write to Parquet file with heavy compression
        df.write_parquet(self.output_file, compression='brotli')
