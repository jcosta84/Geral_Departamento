import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from streamlit import connection
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, session
from streamlit_option_menu import option_menu
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import io
import json
from urllib.parse import quote_plus
import plotly.express as px
from datetime import datetime
from io import StringIO


#ler arquivo config.json
with open("config/config.json") as f:
    config = json.load(f)

#criar ligação a base de dados
server =   config["BD_SERVER"]
database = config["BD_NAME"]
user = config["BD_USER"]
password = config["BD_PASSWORD"]
driver = config["BD_DRIVER"]


print("Conectando com usuário:", config["BD_USER"])

#para situação de espaços no driver
#driver_encoded = quote_plus(driver)

#engine = create_engine(
    #f"mssql+pyodbc://{user}:{password}@{server}/{database}?driver={driver_encoded}",
    #fast_executemany=True
#)

#Session = sessionmaker(bind=engine)
#session = Session()
#SessionLocal = sessionmaker(bind=engine)


#query = "SELECT * FROM usurarios"
#utilizador = pd.read_sql(query, engine)

#print(utilizador)