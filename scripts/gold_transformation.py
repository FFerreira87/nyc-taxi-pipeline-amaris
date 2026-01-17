from pyspark.sql import SparkSession
from pyspark.sql import functions as F

def transform_gold():
    spark = SparkSession.builder.appName("NYC_Taxi_Gold_Load").getOrCreate()
    
    silver_path = "./data/silver/yellow_trips_silver"
    gold_path = "./data/gold"

    # Lendo dados da Silver
    df_silver = spark.read.parquet(silver_path)

    # --- CRIAÇÃO DA DIM_ZONES ---
    # Pegamos as colunas únicas de localização
    dim_zones = df_silver.select(
        F.col("PULocationID").alias("zone_id"),
        F.col("pickup_borough").alias("borough"),
        F.col("pickup_zone").alias("zone")
    ).distinct()

    # --- CRIAÇÃO DA FACT_TRIPS ---
    # Selecionamos métricas e chaves, e criamos a coluna de partição
    fact_trips = df_silver.select(
        "VendorID",
        F.to_date("tpep_pickup_datetime").alias("pickup_date"),
        "tpep_pickup_datetime",
        "tpep_dropoff_datetime",
        "passenger_count",
        "trip_distance",
        "RatecodeID",
        "PULocationID",
        "DOLocationID",
        "payment_type",
        "fare_amount",
        "tip_amount",
        "total_amount",
        "trip_duration_minutes"
    )

    # Salvando a Dimensão
    dim_zones.write.mode("overwrite").parquet(f"{gold_path}/dim_zones")

    # Salvando a Fato com Particionamento (Requisito do Teste)
    # Na nuvem (BigQuery), o Terraform configuraria o clustering, 
    # mas aqui no Spark definimos o particionamento na escrita.
    fact_trips.write.mode("overwrite") \
        .partitionBy("pickup_date") \
        .parquet(f"{gold_path}/fact_trips")

    print("Camada Gold processada com sucesso!")
    spark.stop()

if __name__ == "__main__":
    transform_gold()