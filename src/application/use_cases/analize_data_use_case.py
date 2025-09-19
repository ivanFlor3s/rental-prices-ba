import pandas as pd
from datetime import datetime

from src.domain.entities.mean_stack_chart import ChartFilters, MeanData, Metadata, SurfacePriceData
from src.infrastructure.logging.config import logger
from src.infrastructure.db.session import engine


class DataAnalizer:

    def __init__(self):
        self.sql_sentence_mean = """SELECT d.*, n.name AS barrio FROM departments d 
                      JOIN neighborhoods n ON n.id = d.neighborhood_id
                      WHERE d.currency_price = 'ARS'"""
        
        self.sql_sentence_surface = """SELECT d.*, n.name AS barrio FROM departments d 
                        JOIN neighborhoods n ON n.id = d.neighborhood_id
                        WHERE d.currency_price = 'ARS' AND d.surface_total IS NOT NULL AND d.surface_total > 0"""
        
 
    def _create_dataframe_from_query(self, sql_sentence: str) -> pd.DataFrame:
        df = pd.read_sql(sql_sentence, engine)
        return df

    def analize_data_for_mean(self, filters: ChartFilters = ChartFilters(rooms=None)) -> dict:
        if(filters.rooms is not None):
            sql_sentence = self.sql_sentence_mean + f" AND d.rooms = {filters.rooms}"
        df = self._create_dataframe_from_query(sql_sentence)

        # Limpiar datos (quitar nulos y convertir a numérico si hace falta)
        df["expenses"] = pd.to_numeric(df["expenses"], errors="coerce")
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df = df.dropna(subset=["expenses", "price", "barrio"])


        metadata = Metadata(
            generatedAt=datetime.now(),
            totalDepartments=len(df),
            totalNeighborhoods=df['barrio'].nunique(),
            analysisType="mean prices",
        )
        analysis_data = self._generate_expenses_by_neighborhood_data(df)

        return {"data": analysis_data, "metadata": metadata}



    def _generate_expenses_by_neighborhood_data(df) -> list[MeanData]:
        """Genera datos para gráfico de barras: Promedio de expensas por barrio."""
        expenses_by_barrio = df.groupby("barrio")["expenses"].agg(['mean', 'count']).round(2)
        expenses_by_barrio = expenses_by_barrio.sort_values('mean')
        
        return [
            MeanData(
                neighborhoodId=int(df[df['barrio'] == barrio]['neighborhood_id'].values[0]),
                neighborhoodName=barrio,
                averageExpense=int(row['mean']),
                averagePrice=int(df[df['barrio'] == barrio]['price'].mean()),
                sample=int(row['count'])
            )
            for barrio, row in expenses_by_barrio.iterrows()
        ]

    def analize_data_for_surface_price(self) -> dict:

        df = self._create_dataframe_from_query(self.sql_sentence_surface)

        # Limpiar datos (quitar nulos y convertir a numérico si hace falta)
        df["surface_total"] = pd.to_numeric(df["surface_total"], errors="coerce")
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df = df.dropna(subset=["surface_total", "price", "barrio"])

        metadata = Metadata(
            generatedAt=datetime.now(),
            totalDepartments=len(df),
            totalNeighborhoods=df['barrio'].nunique(),
            analysisType="surface",
        )
        analysis_data = self._generate_price_surface_data(df)

        return {"data": analysis_data, "metadata": metadata}

    def _generate_price_surface_data(self, df):
        price_m2_by_barrio = df.groupby(["barrio", "neighborhood_id"]).apply(
            lambda x: (x["price"] / x["surface_total"]).mean()
        ).reset_index(name="price_m2")
        

        return [ SurfacePriceData(
            neighborhoodId=int(row["neighborhood_id"]),
            neighborhoodName=row["barrio"],
            averagePriceMM=int(row["price_m2"])
            ) 
            for _, row in price_m2_by_barrio.iterrows() 
        ]



