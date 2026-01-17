from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType

def create_spark_session():
    return SparkSession.builder \
        .appName("NYC_Taxi_Silver_Transformation") \
        .getOrCreate()

def transform_silver():
    spark = create_spark_session()
    
    bronze_path = "./data/bronze"
    silver_path = "./data/silver"

    print("Lendo dados da camada Bronze...")
    df_trips = spark.read.parquet(f"{bronze_path}/yellow_trips")
    df_zones = spark.read.parquet(f"{bronze_path}/taxi_zones")

    # 1. Limpeza e Filtros (Data Quality)
    # Removemos viagens sem passageiros, com distância zero ou valores negativos
    df_cleaned = df_trips.filter(
        (F.col("passenger_count") > 0) & 
        (F.col("trip_distance") > 0) & 
        (F.col("total_amount") > 0)
    ).dropDuplicates()

    # 2. Join com Zone Lookup (Enhricement)
    # Usamos broadcast join para otimizar, pois a tabela de zonas é minúscula
    zones_broadcast = F.broadcast(df_zones.select(
        F.col("LocationID"),
        F.col("Borough").alias("borough"),
        F.col("Zone").alias("zone")
    ))

    # Join para Pickup (Source)
    df_silver = df_cleaned.join(
        zones_broadcast, 
        df_cleaned.PULocationID == zones_broadcast.LocationID, 
        "left"
    ).withColumnRenamed("borough", "pickup_borough").withColumnRenamed("zone", "pickup_zone").drop("LocationID")

    # Join para Dropoff (Target)
    df_silver = df_silver.join(
        zones_broadcast, 
        df_silver.DOLocationID == zones_broadcast.LocationID, 
        "left"
    ).withColumnRenamed("borough", "dropoff_borough").withColumnRenamed("zone", "dropoff_zone").drop("LocationID")

    # 3. Transformações Adicionais
    # Criando colunas de tempo e calculando a duração da viagem em minutos
    df_silver = df_silver.withColumn(
        "trip_duration_minutes", 
        (F.unix_timestamp("tpep_dropoff_datetime") - F.unix_timestamp("tpep_pickup_datetime")) / 60
    )

    # 4. Salvando na Silver    
    df_silver.write.mode("overwrite").parquet(f"{silver_path}/yellow_trips_silver")
    
    print(f"Camada Silver finalizada. Registros processados: {df_silver.count()}")
    spark.stop()

if __name__ == "__main__":
    transform_silver()