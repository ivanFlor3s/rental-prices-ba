from bs4 import BeautifulSoup
from src.domain.scrappers.scrapper_base import BaseScrapper
from src.infrastructure.logging.config import logger
from src.domain.entities.dapartment import Department, DeptDetails
from src.utils.get_number import get_number
from src.utils.text_matcher import text_match_score
import cloudscraper

class ZonaPropScrapper(BaseScrapper):

    scraper = cloudscraper.create_scraper() 
    soup = None
    def __init__(self, url: str, neighborhood: str):
        super().__init__(url)
        self.neighborhood = neighborhood

    def process_page(self):
        """Procesa la página web y extrae la información relevante"""
        self.soup = self.get_soup()
        if not self.check_valid_search():
            logger.error("La búsqueda no es válida, no se encontró el barrio en la página")
            return []
        departments_info = self.get_departments()
        return departments_info

    def get_soup(self):
        """Obtiene el objeto BeautifulSoup de la página web"""
        response = self.scraper.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        return soup
    
    def check_valid_search(self) -> bool:
        """Verifica si la búsqueda es válida, en zona prop asumimos 
        que ocurre cuando el barrio por el que buscamos se setea en el input del buscador
        Ademas coincide con el nombre de la busqueda en la URL"""
        
        search_component = self.soup.find('div', id='search-location-input')
        if not search_component:
            logger.error("No se encontró el componente de búsqueda en la página")
            return False
        search_text = search_component.find('li','createPills-module__tag').find('p').text.strip() if search_component.find('li','createPills-module__tag') else None
        if not search_text:
            logger.error("No se encontró el texto de búsqueda en la página")
            return False
        
        if text_match_score(search_text, self.neighborhood) < 0.7:
            logger.error(f"El barrio buscado '{self.neighborhood}' no coincide con el texto de búsqueda encontrado '{search_text}'")
            return False

        return True

    def get_departments(self) -> list[Department] :
        """Extrae los departamentos de la página web"""
        department_cards = self.soup.find_all('div', 'postingsList-module__card-container')
        departments: list[Department] = []
        for card in department_cards:
            dep: Department = Department(
                title= self.get_title(card),
                url=self.get_department_url(card),
                price=self.get_department_price(card)[0],
                expenses= self.get_department_expenses(card),
                is_usd=self.get_department_price(card)[1],
                location=self.get_department_location(card),
                details=self.get_department_details(card)
            )
            departments.append(dep)

        return departments
    
    def get_department_expenses(self, card) -> int:
        """Extrae los gastos del departamento de una tarjeta"""
        expenses_element = card.find(class_='postingPrices-module__expenses-property-listing')
        expenses_text = expenses_element.text.strip() if expenses_element else "0"
        expenses = get_number(expenses_text)
        return expenses

    def get_department_details(self, card) -> DeptDetails:
        """Extrae los detalles del departamento de una tarjeta"""
        details_element = card.find('h3', class_='postingMainFeatures-module__posting-main-features-block')
        if not details_element:
            details_element = card.find('h3')
            
        details = []
        if details_element:
            details = details_element.find_all('span', class_='postingMainFeatures-module__posting-main-features-span')
        
        result: DeptDetails = DeptDetails(
            bedrooms=0,
            bathrooms=0,
            area=0.0,
            ambientes=0,
            garages=0
        )

        for detail in details:
            detail_text = detail.text.strip()
            if 'dorm' in detail_text:
                result.bedrooms = get_number(detail_text)
            elif 'amb' in detail_text:
                result.ambientes = get_number(detail_text)
            elif 'ba' in detail_text:
                result.bathrooms = get_number(detail_text)
            elif 'coch' in detail_text:
                result.garages = get_number(detail_text)
            elif 'tot' in detail_text:
                result.area = get_number(detail_text)

        return result

    def get_department_location(self, card) -> str:
        """Extrae la ubicación del departamento de una tarjeta"""
        location_element = card.find(class_='postingLocations-module__location-text')
        return location_element.text.strip() if location_element else ""
    
    def get_title(self,card) -> str:
        title_element = card.find(class_='postingLocations-module__location-address-in-listing')
        return title_element.text.strip() if title_element else "No title found"

    def get_department_price(self, card) -> tuple[int, bool]:
        """Extrae el precio del departamento de una tarjeta"""
        price_element = card.find(class_='postingPrices-module__price')
        price_text = price_element.text.strip() if price_element else "0"
        is_usd = 'USD' in price_text or '$U' in price_text or 'U$S' in price_text
        price = get_number(price_text)
        return price, is_usd
  
    def get_department_url(self, card) -> str:
        """Extrae la URL del departamento de una tarjeta"""
        container = card.find(class_='postingCardLayout-module__posting-card-layout')
        return "https://www.zonaprop.com.ar" + container['data-to-posting'] if container and container.has_attr('data-to-posting') else ""
    
  