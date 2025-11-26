from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import pandas as pd

server = "192.168.38.28,1433"
database = "SistemaGestao"
user = "jpaulo"
password = "loucoste9850053"
driver = "ODBC Driver 17 for SQL Server"

driver_encoded = quote_plus(driver)
DATABASE_URL = f"mssql+pyodbc://{user}:{password}@{server}/{database}?driver={driver_encoded}"

engine = create_engine(DATABASE_URL, fast_executemany=True)

query = "SELECT * FROM Users" 
user = pd.read_sql(query, engine)
print(user)



