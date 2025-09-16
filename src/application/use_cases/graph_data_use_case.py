
import pandas as pd
import matplotlib.pyplot as plt
from src.infrastructure.db.session import engine

def generate_matplotlib_charts():
    df = pd.read_sql("""SELECT d.*, n.name AS barrio FROM departments d 
                        JOIN neighborhoods n ON n.id = d.neighborhood_id
                    """,engine)

    df["expenses"] = pd.to_numeric(df["expenses"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["expenses", "price", "barrio"])

    """Genera los gráficos originales con matplotlib."""
    plt.figure(figsize=(10, 6))
    df.groupby("barrio")["expenses"].mean().sort_values().plot(kind="bar")
    plt.title("Promedio de expensas por barrio")
    plt.ylabel("Expensas ($)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(8, 5))
    df["expenses"].plot(kind="hist", bins=30, edgecolor="black")
    plt.title("Distribución de expensas")
    plt.xlabel("Expensas ($)")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(8, 5))
    plt.scatter(df["price"], df["expenses"], alpha=0.5)
    plt.title("Precio vs Expensas")
    plt.xlabel("Precio ($)")
    plt.ylabel("Expensas ($)")
    plt.tight_layout()
    plt.show()
