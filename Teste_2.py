from urllib.parse import quote_plus
from sqlalchemy import create_engine
import pandas as pd

HOST = "100.116.112.107"
PORT = 3306
DATABASE = "AQStore"
USER = "jcosta"
PASSWORD = quote_plus("Loucoste@9309323")

engine = create_engine(
    f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

try:
    query = "SELECT * FROM usuarios"
    user = pd.read_sql(query, engine)
    print(user)

except Exception as e:
    print("Erro na ligação:")
    print(e)