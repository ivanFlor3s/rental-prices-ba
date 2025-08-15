import pandas as pd
import matplotlib.pyplot as plt

from src.infrastructure.logging.config import logger
from src.infrastructure.db.session import engine

def analize_data():
    """Analiza los datos de departamentos guardados en la base de datos."""
    df = pd.read_sql("""SELECT d.*, n.name AS barrio FROM departments d 
                        JOIN neighborhoods n ON n.id = d.neighborhood_id
                    """
                    ,engine)
    


    # 3️⃣ Limpiar datos (quitar nulos y convertir a numérico si hace falta)
    df["expenses"] = pd.to_numeric(df["expenses"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["expenses", "price", "barrio"])

    # 4️⃣ Gráfico: Promedio de expensas por barrio
    plt.figure(figsize=(10, 6))
    df.groupby("barrio")["expenses"].mean().sort_values().plot(kind="bar")
    plt.title("Promedio de expensas por barrio")
    plt.ylabel("Expensas ($)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

    # 5️⃣ Histograma de expensas
    plt.figure(figsize=(8, 5))
    df["expenses"].plot(kind="hist", bins=30, edgecolor="black")
    plt.title("Distribución de expensas")
    plt.xlabel("Expensas ($)")
    plt.tight_layout()
    plt.show()

    # 6️⃣ Scatter: Precio vs Expensas
    plt.figure(figsize=(8, 5))
    plt.scatter(df["price"], df["expenses"], alpha=0.5)
    plt.title("Precio vs Expensas")
    plt.xlabel("Precio ($)")
    plt.ylabel("Expensas ($)")
    plt.tight_layout()
    plt.show()

    pass