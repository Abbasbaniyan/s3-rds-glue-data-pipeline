import os
import boto3
import pandas as pd
from sqlalchemy import create_engine


# AWS Configuration
AWS_REGION = os.getenv("AWS_REGION", "eu-north-1")

# S3 Configuration
S3_BUCKET = os.getenv("S3_BUCKET")
S3_KEY = os.getenv("S3_KEY")

# RDS Configuration
RDS_ENDPOINT = os.getenv("RDS_ENDPOINT")
RDS_USERNAME = os.getenv("RDS_USERNAME")
RDS_PASSWORD = os.getenv("RDS_PASSWORD")
RDS_DB_NAME = os.getenv("RDS_DB_NAME")
RDS_TABLE_NAME = os.getenv("RDS_TABLE_NAME")

# Glue Configuration
GLUE_DATABASE = os.getenv("GLUE_DATABASE")
GLUE_TABLE = os.getenv("GLUE_TABLE")
GLUE_S3_LOCATION = os.getenv("GLUE_S3_LOCATION")


def create_glue_table(df):

    print("RDS failed. Starting AWS Glue fallback...")

    glue = boto3.client(
        "glue",
        region_name=AWS_REGION
    )

    # Convert pandas data types to Glue-compatible types
    columns = []

    for column in df.columns:

        dtype = str(df[column].dtype)

        if "int" in dtype:
            glue_type = "bigint"

        elif "float" in dtype:
            glue_type = "double"

        elif "bool" in dtype:
            glue_type = "boolean"

        else:
            glue_type = "string"

        columns.append({
            "Name": column.lower().replace(" ", "_"),
            "Type": glue_type
        })

    # Create Glue Database
    try:

        glue.create_database(
            DatabaseInput={
                "Name": GLUE_DATABASE,
                "Description": "Database created for S3 RDS fallback pipeline"
            }
        )

        print(f"Glue database created: {GLUE_DATABASE}")

    except glue.exceptions.AlreadyExistsException:

        print(
            f"Glue database already exists: {GLUE_DATABASE}"
        )

    # Create Glue Table
    try:

        glue.create_table(
            DatabaseName=GLUE_DATABASE,
            TableInput={
                "Name": GLUE_TABLE,
                "Description": "Dataset registered after RDS ingestion failure",
                "TableType": "EXTERNAL_TABLE",
                "Parameters": {
                    "classification": "csv",
                    "typeOfData": "file"
                },
                "StorageDescriptor": {
                    "Columns": columns,
                    "Location": GLUE_S3_LOCATION,
                    "InputFormat":
                        "org.apache.hadoop.mapred.TextInputFormat",
                    "OutputFormat":
                        "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
                    "SerdeInfo": {
                        "SerializationLibrary":
                            "org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe",
                        "Parameters": {
                            "field.delim": ","
                        }
                    }
                }
            }
        )

        print("SUCCESS: Glue table created successfully.")

    except glue.exceptions.AlreadyExistsException:

        print(
            f"Glue table already exists: {GLUE_TABLE}"
        )

        print("SUCCESS: Glue fallback completed.")

    print(
        f"Glue table: {GLUE_DATABASE}.{GLUE_TABLE}"
    )


def main():

    print(
        "Starting S3 → RDS → Glue ingestion pipeline..."
    )

    # -----------------------------
    # 1. Read CSV from S3
    # -----------------------------

    s3 = boto3.client(
        "s3",
        region_name=AWS_REGION
    )

    print(
        f"Reading CSV from s3://{S3_BUCKET}/{S3_KEY}"
    )

    response = s3.get_object(
        Bucket=S3_BUCKET,
        Key=S3_KEY
    )

    df = pd.read_csv(
        response["Body"]
    )

    print(
        f"CSV loaded successfully. Records: {len(df)}"
    )

    # -----------------------------
    # 2. Try RDS
    # -----------------------------

    try:

        print("Connecting to RDS...")

        database_url = (
            f"mysql+pymysql://"
            f"{RDS_USERNAME}:{RDS_PASSWORD}"
            f"@{RDS_ENDPOINT}:3306/"
            f"{RDS_DB_NAME}"
        )

        engine = create_engine(
            database_url,
            connect_args={
                "connect_timeout": 10
            }
        )

        print(
            f"Uploading data to RDS table: {RDS_TABLE_NAME}"
        )

        df.to_sql(
            RDS_TABLE_NAME,
            con=engine,
            if_exists="replace",
            index=False
        )

        print(
            "SUCCESS: Data uploaded to RDS successfully."
        )

    except Exception as e:

        print("ERROR: RDS upload failed.")

        print(
            f"Reason: {e}"
        )

        create_glue_table(df)


if __name__ == "__main__":
    main()