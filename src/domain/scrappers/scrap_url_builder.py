class ZonaPropUrlBuilder:
    BASE_URL = "https://www.zonaprop.com.ar"

    def __init__(self):
        self.operation = None         # "alquiler" | "venta"
        self.neighborhood = None      # ej. "caballito"
        self.extras = []              # lista: ["con-balcon", "apto-profesional"]
        self.rooms_min = None         # ej. 2
        self.rooms_max = None         # ej. 3
        self.price_min = None         # ej. 80000
        self.price_max = None         # ej. 400000
        self.currency = None          # pesos
    
     # Métodos de configuración
    def set_operation(self, operation: str):
        if operation not in ["alquiler", "venta"]:
            raise ValueError("Operation must be 'alquiler' or 'venta'")
        self.operation = operation.lower()
        return self

    def set_neighborhood(self, neighborhood: str):
        self.neighborhood = neighborhood.lower()
        return self

    def add_extra(self, extra: str):
        self.extras.append(extra.lower())
        return self

    def set_rooms_range(self, min_rooms: int, max_rooms: int):
        self.rooms_min = min_rooms
        self.rooms_max = max_rooms
        return self

    def set_price_range(self, min_price: int, max_price: int, currency: str = "pesos"):
        self.price_min = min_price
        self.price_max = max_price
        self.currency = currency.lower()
        return self
    
    def set_only_min_price(self, min_price: int, currency: str = "pesos"):
        self.price_min = min_price
        self.currency = currency.lower()
        self.price_max = None
        return self
    
    def set_only_max_price(self, max_price: int, currency: str = "pesos"):
        self.price_max = max_price
        self.currency = currency.lower()
        self.price_min = None
        return self

     # Método para construir la URL final

    def build(self) -> str:
        """Construye la URL final basada en los parámetros configurados."""
        # https://www.zonaprop.com.ar/departamentos-alquiler-caballito-con-balcon-desde-2-hasta-3-ambientes-80000-400000-pesos.html
        # Validaciones mínimas
        if not self.operation or not self.neighborhood:
            raise ValueError("Operation y Neighborhood must be set")

        parts = [
            f"departamentos-{self.operation}",
            self.neighborhood
        ]
        
        # Extras
        if self.extras:
            extras_with_con_prefix = [f"con-{extra}" for extra in self.extras]
            parts.extend(extras_with_con_prefix)

        # Rango de ambientes
        if self.rooms_min is not None and self.rooms_max is not None:
            parts.append(f"desde-{self.rooms_min}-hasta-{self.rooms_max}-ambientes")

        # Rango de precios
        if self.price_min is not None and self.price_max is not None:
            parts.append(f"{self.price_min}-{self.price_max}-{self.currency}")
        elif self.price_min is not None:
            parts.append(f"mas-{self.price_min}-{self.currency}")
        elif self.price_max is not None:
            parts.append(f"menos-{self.price_max}-{self.currency}")

        path = "-".join(parts) + ".html"
        return f"{self.BASE_URL}/{path}"