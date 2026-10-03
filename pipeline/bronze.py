import os

os.environ["HADOOP_HOME"] = r"C:\Users\gabriel.bassanelo\Desktop\hadoop"
os.environ["PATH"] = os.environ["HADOOP_HOME"] + r"\bin;" + os.environ["PATH"]

from pyspark.sql import (
    SparkSession,
)  ## Ligando o SparkSession, que é a porta de entrada para o Spark

spark = SparkSession.builder.appName("bronze").master("local[*]").getOrCreate()
print(spark.version)


print("SparkSession criada com sucesso!")


df_cursos = (
    spark.read.option(  ## Lendo o arquivo CSV com os dados do Censo Superior
        "header", True
    )  # 1ª linha do arquivo = nomes das colunas
    .option("sep", ";")  # colunas separadas por ponto e vírgula
    .option("encoding", "ISO-8859-1")  # padrão Latin-1, senão os acentos quebram
    .option("inferSchema", True)  # Spark adivinha o tipo de cada coluna
    .csv("data/MICRODADOS_CADASTRO_CURSOS_2024.CSV")
)  # caminho relativo

df_ies = (
    spark.read.option(  ## Lendo o arquivo CSV com os dados do Censo Superior
        "header", True
    )  # 1ª linha do arquivo = nomes das colunas
    .option("sep", ";")  # colunas separadas por ponto e vírgula
    .option("encoding", "ISO-8859-1")  # padrão Latin-1, senão os acentos quebram
    .option("inferSchema", True)  # Spark adivinha o tipo de cada coluna
    .csv("data/MICRODADOS_ED_SUP_IES_2024.CSV")
)


df_cursos.write.mode("overwrite").parquet("data/bronze/cursos")
print("Bronze cursos gravada")

df_ies.write.mode("overwrite").parquet("data/bronze/ies")
print("Bronze IES gravada")
