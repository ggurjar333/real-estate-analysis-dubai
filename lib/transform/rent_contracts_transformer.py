from datetime import date
import logging
import polars as pl

# Configure logging
logging.basicConfig(level=logging.INFO)

class RentContractsTransformer:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file

    def transform(self):
        try:
            # Read the CSV as a LazyFrame with any necessary schema overrides.
            lf = pl.scan_csv(
                self.input_file,
                null_values=["null"],
                schema_overrides={"ejari_property_sub_type_id": pl.Int64}
            )
            # Resolve the schema once to get column names and types.
            schema = lf.collect_schema()
            column_names = schema.names()
            column_types = schema.dtypes()

            # Select columns by type without triggering performance warnings.
            string_columns = [
                col for col, dtype in zip(column_names, column_types) 
                if dtype == pl.Utf8
            ]
            numeric_columns = [
                col for col, dtype in zip(column_names, column_types) 
                if dtype in [pl.Int32, pl.Float64]
            ]

            column_names = [string_columns + numeric_columns]

            # Reorder columns: first strings, then numerics.
            lf = lf.select(column_names)

            # Write the LazyFrame to Parquet.
            # Note: This uses the old streaming engine, which is deprecated.
            lf.sink_parquet(self.output_file, compression="zstd", compression_level=22)
        except Exception as e:
            logging.exception("An error occurred during transformation.")
