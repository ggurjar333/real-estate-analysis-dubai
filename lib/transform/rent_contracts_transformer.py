from pyspark.sql import SparkSession
from pyspark.sql.functions import col

class RentContractsTransformer:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file
        self.spark = SparkSession.builder.appName("RentContractsTransformer").getOrCreate()

    def transform(self):
        # Read the CSV file
        df = self.spark.read.csv(self.input_file, header=True, inferSchema=True, nullValue='null')
        df.show(5)

        # Separate string and numeric columns
        string_columns = [field.name for field in df.schema.fields if field.dataType == 'StringType']
        numeric_columns = [field.name for field in df.schema.fields if field.dataType in ['IntegerType', 'DoubleType']]

        # Reorder columns
        df = df.select(string_columns + numeric_columns)
        df.show(10)

        # Write to Parquet file with heavy compression
        df.write.parquet(self.output_file, compression='brotli')

# Example usage
# transformer = RentContractsTransformer('input.csv', 'output.parquet')
# transformer.transform()
