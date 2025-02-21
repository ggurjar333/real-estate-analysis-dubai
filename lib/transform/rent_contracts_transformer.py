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

            # Write the LazyFrame to Parquet.
            # Note: This uses the old streaming engine, which is deprecated.
            lf.sink_parquet(self.output_file, compression="zstd", compression_level=22)
        except Exception as e:
            logging.exception("An error occurred during transformation.")
