import pandas as pd
from datetime import datetime

from src.infrastructure.logging.config import logger
from src.infrastructure.db.session import engine

def analize_data():
    """
    Analiza los datos de departamentos guardados en la base de datos.
    
    Returns:
        dict: Datos de análisis en formato JSON
    """
    sql_sentence = """SELECT d.*, n.name AS barrio FROM departments d 
                      JOIN neighborhoods n ON n.id = d.neighborhood_id"""
    df = pd.read_sql(sql_sentence, engine)

    # Limpiar datos (quitar nulos y convertir a numérico si hace falta)
    df["expenses"] = pd.to_numeric(df["expenses"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["expenses", "price", "barrio"])

    analysis_data = {
        "metadata": {
            "generated_at": datetime.now(),
            "total_departments": len(df),
            "total_neighborhoods": df['barrio'].nunique(),
            "analysis_type": "rental_properties_ba"
        },
        "charts": {
            "prices_expenses_by_neighborhood": _generate_expenses_by_neighborhood_data(df),
            # "expenses_distribution": _generate_expenses_distribution_data(df),
            # "price_vs_expenses_scatter": _generate_price_vs_expenses_data(df),
            # "summary_stats": _generate_summary_stats(df)
        }
    }
    return analysis_data
    


def _generate_expenses_by_neighborhood_data(df):
    """Genera datos para gráfico de barras: Promedio de expensas por barrio."""
    expenses_by_barrio = df.groupby("barrio")["expenses"].agg(['mean', 'count']).round(2)
    expenses_by_barrio = expenses_by_barrio.sort_values('mean')
    
    return {
        "chart_type": "StackedBar",
        "title": "Promedio de expensas por barrio",
        "y_axis_label": "Barrio",
        "x_axis_label": "Amount($)",
        "data": [
            {
                "neighborhoodId": int(df[df['barrio'] == barrio]['neighborhood_id'].values[0]),
                "neighborhood": barrio,
                "average_expenses": float(row['mean']),
                "average_price": float(df[df['barrio'] == barrio]['price'].mean()),
                "count": int(row['count'])
            }
            for barrio, row in expenses_by_barrio.iterrows()
        ]
    }


def _generate_expenses_distribution_data(df):
    """Genera datos para histograma: Distribución de expensas."""
    # Crear bins para el histograma
    expenses_data = df["expenses"].dropna()
    hist, bins = pd.cut(expenses_data, bins=30, retbins=True)
    hist_counts = hist.value_counts().sort_index()
    
    return {
        "chart_type": "histogram",
        "title": "Distribución de expensas",
        "x_axis_label": "Expensas ($)",
        "y_axis_label": "Frecuencia",
        "bins": 30,
        "data": [
            {
                "bin_start": float(interval.left),
                "bin_end": float(interval.right),
                "bin_center": float(interval.mid),
                "count": int(count)
            }
            for interval, count in hist_counts.items()
        ],
        "stats": {
            "mean": float(expenses_data.mean()),
            "median": float(expenses_data.median()),
            "min": float(expenses_data.min()),
            "max": float(expenses_data.max()),
            "std": float(expenses_data.std())
        }
    }


def _generate_price_vs_expenses_data(df):
    """Genera datos para scatter plot: Precio vs Expensas."""
    scatter_data = df[["price", "expenses", "barrio"]].dropna()
    
    return {
        "chart_type": "scatter",
        "title": "Precio vs Expensas",
        "x_axis_label": "Precio ($)",
        "y_axis_label": "Expensas ($)",
        "data": [
            {
                "price": float(row["price"]),
                "expenses": float(row["expenses"]),
                "neighborhood": row["barrio"]
            }
            for _, row in scatter_data.iterrows()
        ],
        "correlation": float(scatter_data["price"].corr(scatter_data["expenses"]))
    }


def _generate_summary_stats(df):
    """Genera estadísticas resumen generales."""
    return {
        "chart_type": "summary",
        "title": "Estadísticas Generales",
        "data": {
            "total_properties": len(df),
            "neighborhoods_count": df['barrio'].nunique(),
            "price_stats": {
                "mean": float(df["price"].mean()),
                "median": float(df["price"].median()),
                "min": float(df["price"].min()),
                "max": float(df["price"].max()),
                "std": float(df["price"].std())
            },
            "expenses_stats": {
                "mean": float(df["expenses"].mean()),
                "median": float(df["expenses"].median()),
                "min": float(df["expenses"].min()),
                "max": float(df["expenses"].max()),
                "std": float(df["expenses"].std())
            },
            "top_neighborhoods_by_count": df['barrio'].value_counts().head(5).to_dict(),
            "top_neighborhoods_by_avg_price": df.groupby('barrio')['price'].mean().nlargest(5).round(2).to_dict()
        }
    }


