# import Asclepius dependencies
from asclepius.instelling import GGZ, ZKH
from asclepius.medewerker import Medewerker

# import other dependencies
from selenium import webdriver
from typing import Union
from time import sleep

class PortaalDriver:
    driver = 'C:\Program Files (x86)\chromedriver.exe'
    
    def __init__(self, gebruiker: Medewerker):
        self.gebruiker = gebruiker
        self.driver = PortaalDriver.driver
        self.portaal = None
        return None
    
    def open_portaal(self):
        self.portaal = webdriver.Chrome(self.driver)
        return None
    
    def inloggen(self, instelling: Union[GGZ, ZKH]):
        # open portaal
        self.portaal = webdriver.Chrome(self.driver)
        
        # haal de loginpagina op
        self.portaal.get(instelling.login)
        sleep(2)
        
        # vind invoer op de pagina
        username = self.portaal.find_element_by_name('username')
        password = self.portaal.find_element_by_name('password')
        submit = self.portaal.find_element_by_name('submit')
        
        # verstuur de informatie van de gebruiker
        username.send_keys(self.gebruiker.gebruikersnaam)
        password.send_keys(self.gebruiker.wachtwoord)
        submit.click()
        sleep(2)
        return

    # Download Excel Functies

    def download_da_excel(self, instelling: Union[GGZ, ZKH], test: bool = False):
        if test:
            da_link = instelling.daily_audit_test
            da_download_link = instelling.da_test_excel_download
        else:
            da_link = instelling.daily_audit
            da_download_link = instelling.da_excel_download
        
        self.portaal.get(da_link)
        sleep(2)
        if (not test) and (instelling.huidige_omgeving == "productie"):
            quickremove = self.portaal.find_element_by_class_name('quickRemove')
            quickremove_list = quickremove.find_elements_by_tag_name("li")
            for quickremove_item in quickremove_list:
                if quickremove_item.text == " Behandeld: Ja" or quickremove_item.text == " Behandeld: Nee":
                    delete_behandeld = quickremove_item.find_element_by_class_name('delete')
                    delete_behandeld.click()
                    sleep(3)
                    break
        self.portaal.get(da_download_link)
        sleep(5)
        return None

    def download_bi_excel(self, instelling: Union[GGZ, ZKH]):
        self.portaal.get(instelling.bi_prestatiekaart)
        sleep(2)
        self.portaal.get(instelling.bi_excel_download)
        sleep(5)
        return None

    def download_zpm_excel(self, instelling: Union[GGZ, ZKH]):
        self.portaal.get(instelling.zpm_prestatiekaart)
        sleep(2)
        self.portaal.get(instelling.zpm_excel_download)
        sleep(5)
        return None

    # Webscraper Portaal Functies

    def webscraper_da_portaal(self, instelling: Union[GGZ, ZKH]):
        # inloggen op het portaal
        self.inloggen(instelling)

        # download excel controle/norm in productie
        self.download_da_excel(instelling, False)
        self.gebruiker.webscraper_hernoem_bestand(instelling, 'da', False)
        
        sleep(1)
        
            # download excel controle/norm in test
        self.download_da_excel(instelling, True)
        self.gebruiker.webscraper_hernoem_bestand(instelling, 'da', True)

        # sluit het portaal af
        self.portaal.close()
        return None

    def webscraper_bi_portaal(self, instelling: Union[GGZ, ZKH]):
        # inloggen op het portaal
        self.inloggen(instelling)
        
            # download excel BI prestatiekaart
        self.download_bi_excel(instelling)
        self.gebruiker.webscraper_hernoem_bestand(instelling, 'bi')
        

        # sluit het portaal af
        self.portaal.close()
        return None

    def webscraper_zpm_portaal(self, instelling: Union[GGZ, ZKH]):
        # inloggen op het portaal
        self.inloggen(instelling)

        # download excel ZPM prestatiekaart
        self.download_zpm_excel(instelling)
        self.gebruiker.webscraper_hernoem_bestand(instelling, 'zpm')

        # sluit het portaal af
        self.portaal.close()
        return None

    # Webscraper Functies

    def webscraper_da(self, instelling: Union[GGZ, ZKH]):
        """Download de DA Excels van de opgegeven instelling (ZKH | GGZ)."""

        # download excels uit acceptatie omgeving
        instelling.kies_omgeving('acceptatie')
        self.webscraper_da_portaal(instelling)

        # download excels uit productie omgeving
        instelling.kies_omgeving('productie')
        self.webscraper_da_portaal(instelling)
        return None
    
    def webscraper_bi(self, instelling: Union[GGZ, ZKH]):
        """Download de BI Excels van de opgegeven instelling (ZKH | GGZ)."""

        # download excels uit acceptatie omgeving
        instelling.kies_omgeving('acceptatie')
        self.webscraper_bi_portaal(instelling)

        # download excels uit productie omgeving
        instelling.kies_omgeving('productie')
        self.webscraper_bi_portaal(instelling)
        return None

    def webscraper_zpm(self, instelling: Union[GGZ, ZKH]):
        """Download de ZPM Excels van de opgegeven instelling (ZKH | GGZ)."""

        # download excels uit acceptatie omgeving
        instelling.kies_omgeving('acceptatie')
        self.webscraper_zpm_portaal(instelling)

        # download excels uit productie omgeving
        instelling.kies_omgeving('productie')
        self.webscraper_zpm_portaal(instelling)
        return None