from bs4 import BeautifulSoup
from src.domain.scrappers.scrapper_base import BaseScrapper
from src.infrastructure.logging.config import logger
from src.domain.entities.dapartment import Department, DeptDetails
from src.utils.get_number import get_number
import cloudscraper

class ZonaPropScrapper(BaseScrapper):

    scraper = cloudscraper.create_scraper() 
    soup = None
    def __init__(self, url: str):
        super().__init__(url)

    def process_page(self):
        """Procesa la página web y extrae la información relevante"""
        self.soup = self.get_soup()
        departments_info = self.get_departments()
        return departments_info

    def get_soup(self):
        """Obtiene el objeto BeautifulSoup de la página web"""
        response = self.scraper.get(self.url)
        logger.info("estado de la respuesta: %s", response.status_code)
        soup = BeautifulSoup(response.text, 'html.parser')

        return soup

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
        expenses_element = card.find('div', 'postingPrices-module__expenses postingPrices-module__expenses-property-listing')
        expenses_text = expenses_element.text.strip() if expenses_element else "0"
        expenses = get_number(expenses_text)
        return expenses

    def get_department_details(self, card) -> DeptDetails:
        """Extrae los detalles del departamento de una tarjeta"""
        details_element = card.find('h3')
        details = details_element.find_all('span', 'postingMainFeatures-module__posting-main-features-span postingMainFeatures-module__posting-main-features-listing')
        
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
        location_element = card.find('h2', 'postingLocations-module__location-text')
        return location_element.text.strip() if location_element else ""
    
    def get_title(self,card) -> str:
        title_element = card.find('div', 'postingLocations-module__location-address-in-listing')
        return title_element.text.strip() if title_element else "No title found"

    def get_department_price(self, card) -> tuple[int, bool]:
        """Extrae el precio del departamento de una tarjeta"""
        price_element = card.find('div', 'postingPrices-module__price')
        price_text = price_element.text.strip() if price_element else "0"
        is_usd = 'USD' in price_text or '$U' in price_text or 'U$S' in price_text
        price = get_number(price_text)
        return price, is_usd
  
    def get_department_url(self, card) -> str:
        """Extrae la URL del departamento de una tarjeta"""
        container = card.find('div','postingCardLayout-module__posting-card-layout')
        return "https://www.zonaprop.com.ar" + container['data-to-posting'] if container else ""
    
  