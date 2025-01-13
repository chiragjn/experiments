import argparse
import time

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, rand, expr


def parse_args():
    parser = argparse.ArgumentParser(description="Dynamic Executor Showcase")
    parser.add_argument("--num_rows", type=int, default=1000000, help="Number of rows in the DataFrame")
    parser.add_argument("--num_cols", type=int, default=10, help="Number of columns in the DataFrame")
    return parser.parse_args()


def main(args):
    # Initialize Spark session with dynamic allocation enabled
    spark = (
        SparkSession.builder
        .appName("Dynamic Executor Showcase")
        .getOrCreate()
    )

    # Generate a large DataFrame with random values
    num_rows = args.num_rows
    num_cols = args.num_cols
    df = spark.range(num_rows).withColumn("id", expr("monotonically_increasing_id()")).select("id", *[rand().alias(f"col_{i}") for i in range(num_cols)])

    # Long computation #1: Compute column-wise averages
    print("Starting computation 1: column-wise averages")
    start_time = time.time()
    avg_df = df.select(*[expr(f"avg(col_{i})").alias(f"avg_col_{i}") for i in range(num_cols)])
    avg_df.show()
    print(f"Computation 1 completed in {time.time() - start_time:.2f} seconds")

    # Long computation #2: Find rows where sum of columns exceeds a threshold
    print("Starting computation 2: filtering rows")
    start_time = time.time()
    threshold = num_cols / 2
    filtered_df = df.filter(sum([col(f"col_{i}") for i in range(num_cols)]) > threshold)
    print(f"Filtered rows count: {filtered_df.count()}")
    print(f"Computation 2 completed in {time.time() - start_time:.2f} seconds")

    # Long computation #3: Group by mod 10 of an index column and count
    print("Starting computation 3: group by and count")
    start_time = time.time()
    grouped_df = df.withColumn("mod_index", (col("id") % 10)).groupBy("mod_index").count()
    grouped_df.show()
    print(f"Computation 3 completed in {time.time() - start_time:.2f} seconds")
    spark.stop()


if __name__ == "__main__":
    main(parse_args())

