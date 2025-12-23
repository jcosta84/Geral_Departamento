from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from database.db import engine  # Usar engine, não SessionLocal
import re

def app():
# --- Configuração da página ---
    st.set_page_config(page_title="Pagina Inicial", layout="wide")

    