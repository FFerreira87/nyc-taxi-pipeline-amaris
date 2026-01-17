from pyspark.sql import SparkSession

try:
    spark = SparkSession.builder.appName("TestLocal").getOrCreate()
    print("✅ Spark Session iniciada com sucesso!")
    print(f"Versão do Spark: {spark.version}")
    spark.stop()
except Exception as e:
    print("❌ Erro ao iniciar o Spark. Verifique se o JAVA_HOME está configurado.")
    print(e)