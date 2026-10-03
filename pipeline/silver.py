# 1. Configuração do Windows (winutils)
import os

os.environ["HADOOP_HOME"] = r"C:\Users\gabriel.bassanelo\Desktop\hadoop"
os.environ["PATH"] = os.environ["HADOOP_HOME"] + r"\bin;" + os.environ["PATH"]

# 2. Ligar o Spark
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("silver").master("local[*]").getOrCreate()

# importar as funcões do PySpark SQL
import pyspark.sql.functions as F

# 3. Ler a camada Bronze
df_cursos = spark.read.parquet("data/bronze/cursos")
df_ies = spark.read.parquet("data/bronze/ies")

# 4. Join: trazer o nome da IES para os cursos
df_ies_sel = df_ies.select("CO_IES", "NO_IES")

df_silver = df_cursos.join(
    df_ies_sel,
    on="CO_IES",
    how="left",  # mantém todos os cursos
)

print("Silver: join concluído")

# cria os cases para as colunas DS_REDE e DS_MODALIDADE
df_silver = df_silver.withColumn(
    "DS_REDE",
    F.when(df_silver.TP_REDE == 1, "Pública")
    .when(df_silver.TP_REDE == 2, "Privada")
    .otherwise("Não informado"),
)
df_silver = df_silver.withColumn(
    "DS_MODALIDADE",
    F.when(df_silver.TP_MODALIDADE_ENSINO == 1, "Presencial")
    .when(df_silver.TP_MODALIDADE_ENSINO == 2, "EaD")
    .otherwise("Não informado"),
)

print(df_silver.count())


df_silver.write.mode("overwrite").parquet("data/silver/cursos")
print("silver gravada!")
spark.stop()
