
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

INPUT_PATH = "hdfs:///user/maria_dev/datasets/clean/penguins_clean.csv"
OUTPUT_PATH = "hdfs:///user/maria_dev/spark/output/penguins"


def main():
    spark = SparkSession.builder.appName("PenguinsSparkApp").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    try:
        # 1. Read the cleaned CSV and show its schema
        df = (spark.read
              .option("header", "true")
              .option("inferSchema", "true")
              .csv(INPUT_PATH))
        print("=== Schema ===")
        df.printSchema()
        print("Total rows: %d" % df.count())

        # 2. Select relevant columns
        selected = df.select("species", "island", "sex",
                             "bill_length_mm", "bill_depth_mm",
                             "flipper_length_mm", "body_mass_kg", "year")

        # Remove invalid records: flipper length <= 0 (or null)
        valid = selected.filter(col("flipper_length_mm").isNotNull() &
                                (col("flipper_length_mm") > 0))
        print("Rows removed (flipper_length_mm <= 0): %d"
              % (selected.count() - valid.count()))

        # Simple filter + sort: heavier penguins (>= 4 kg), heaviest first
        result = (valid
                  .filter(col("body_mass_kg") >= 4.0)
                  .orderBy(col("body_mass_kg").desc()))

        result.cache()
        print("Rows in result: %d" % result.count())
        result.show(10, truncate=False)

        # 3. Save as JSON, partitioned by species
        (result.write
         .mode("overwrite")
         .partitionBy("species")
         .json(OUTPUT_PATH))
        print("Output written to %s" % OUTPUT_PATH)

        result.unpersist()
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
