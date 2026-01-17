from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from datetime import datetime
import os

def create_spark_session():
    return SparkSession.builder \
        .appName("NYC_Taxi_Bronze_Ingestion") \
        .config("spark.sql.sources.partitionOverwriteMode", "dynamic") \
        .getOrCreate()

def ingest_bronze():
    spark = create_spark_session()
    
    # Caminhos
    raw_path = "./data/raw"
    bronze_path = "./data/bronze"
    
    print(f"[{datetime.now()}] Iniciando ingestão Bronze...")

    # 1. Ingestão do Taxi Zone Lookup (CSV)
    df_zones = spark.read.option("header", "true").option("inferSchema", "true").csv(f"{raw_path}/taxi_zone_lookup.csv")
    df_zones = df_zones.withColumn("ingestion_at", F.current_timestamp())
    
    df_zones.write.mode("overwrite").parquet(f"{bronze_path}/taxi_zones")
    print("- Taxi Zones: OK")

    # 2. Ingestão do Yellow Taxi Trip Data
    # Lemos os arquivos originais
    df_trips = spark.read.parquet(f"{raw_path}/yellow_tripdata_2024-01.parquet")
    
    # Adicionando metadados de controle
    df_trips = df_trips.withColumn("ingestion_at", F.current_timestamp()) \
                       .withColumn("source_file", F.input_file_name())
    
    # Escrita na Bronze (Sobrescreve se já existir para este mês/carga)
    df_trips.write.mode("overwrite").parquet(f"{bronze_path}/yellow_trips")
    print("- Yellow Trips: OK")

    print(f"[{datetime.now()}] Camada Bronze finalizada com sucesso!")
    spark.stop()

if __name__ == "__main__":
    ingest_bronze()