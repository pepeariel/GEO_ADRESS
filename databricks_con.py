import os
from databricks import sql
from dotenv import load_dotenv, find_dotenv
import pandas as pd

# Load the enviroment variabels
load_dotenv(find_dotenv())

# Create the connection with Datalake
def CreateDataLakeCon(query):
    with sql.connect(server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME"),
                     http_path       = os.getenv("DATABRICKS_HTTP_PATH"),
                     access_token    = os.getenv("DATABRICKS_TOKEN")) as con:
        with con.cursor() as cursor:
            df = pd.read_sql(query, con) # Leitura da tabela em formato DataFrame
    return df

query = """ SELECT t1.*
            FROM 
                (SELECT REPLACE( CONCAT(NOME_LOCAL_COLETA, ",", SIGLA_UF_COLETA), " ", "" ) AS Local_coleta, 
                            REPLACE( CONCAT(NOME_LOCAL_ENTREGA, ",", SIGLA_UF_ENTREGA), " ", "" ) AS Local_entrega,
                            REPLACE( TRIM( CONCAT(NOME_LOCAL_COLETA,"/", SIGLA_UF_COLETA, "X", NOME_LOCAL_ENTREGA, "/", SIGLA_UF_ENTREGA) ) ," ", "") AS Rota
                FROM ouro_transportes.fato_cte
                WHERE CANCELADA = "Não" AND DATA_EMISSAO >= "2020-01-01") AS t1
            GROUP BY Local_coleta, Local_entrega, Rota	
            """