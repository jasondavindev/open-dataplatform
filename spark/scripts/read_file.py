from pyspark.sql import SparkSession
import argparse

sparkSession = SparkSession.builder.appName(
    "read-file").getOrCreate()


def read(args):
    df_load = sparkSession.read.csv(f"{args.namenode}/{args.file}")
    df_load.show()


parser = argparse.ArgumentParser(description="Open and read file")
parser.add_argument('--file', required=True, type=lambda x: str(x))
parser.add_argument('--namenode', required=True, type=lambda x: str(x))
args = parser.parse_args()

read(args)
