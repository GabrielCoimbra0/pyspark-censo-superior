# 1. Configuração do Windows (winutils)
import os

os.environ["HADOOP_HOME"] = r"C:\Users\gabriel.bassanelo\Desktop\hadoop"
os.environ["PATH"] = os.environ["HADOOP_HOME"] + r"\bin;" + os.environ["PATH"]

# 2. Ligar o Spark
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("gold").master("local[*]").getOrCreate()

# importar as funcões do PySpark SQL
import pyspark.sql.functions as F

df_silver = spark.read.parquet("data/silver/cursos")

df_gold_uf = df_silver.groupBy("SG_UF").agg(F.sum("QT_ING").alias("total_ingressantes"))

df_gold_uf.write.mode("overwrite").parquet("data/gold/ingressantes_uf")
print("Gold UF gravada")


df_gold_rede = df_silver.groupBy("DS_REDE").agg(
    F.sum("QT_ING").alias("total_ingressantes"),
    F.count_distinct("CO_CURSO").alias("qtd_cursos"),
)

df_gold_rede.write.mode("overwrite").parquet("data/gold/resumo_rede")
spark.stop()
print("Gold Rede gravada")
