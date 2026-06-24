from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from io import StringIO
from bs4 import BeautifulSoup
import pandas as pd

class WebScraper:
    def __init__(self, driver_path):
        # Initialisation du chemin du WebDriver
        self.driver_path = driver_path
        self.service = Service(executable_path=self.driver_path)

    def scrape_data(self, year, url, table_id):
        # Fonction pour scraper les données pour une saison spécifique
        driver = webdriver.Edge(service=self.service)
        
        # Ouvrir la page avec Selenium
        driver.get(url)
        
        # Attendre que la table soit présente avant de continuer
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, table_id)))
        except Exception as e:
            print(f"Erreur de chargement de la page pour l'année {year}: {e}")
            driver.quit()
            return pd.DataFrame()  # Retourner un DataFrame vide en cas d'erreur
        
        # Récupérer le contenu HTML de la page après le chargement dynamique
        source = driver.page_source
        
        # Analyser le HTML avec BeautifulSoup
        soup = BeautifulSoup(source, 'html.parser')
        
        # Trouver la table spécifique en utilisant son ID
        table = soup.find('table', {'id': table_id})
        
        if table is None:
            print(f"Table introuvable pour l'année {year}")
            driver.quit()
            return pd.DataFrame()  # Retourner un DataFrame vide si la table n'est pas trouvée
        
        # Convertir la table en DataFrame Pandas
        html_table = str(table)
        df = pd.read_html(StringIO(html_table))[0]
        
        # Aplatir les colonnes si nécessaire
        df.columns = [' '.join(col).strip() if isinstance(col, tuple) else col for col in df.columns]
        
        # Ajouter une colonne 'Year' pour distinguer les saisons
        df['Year'] = year
        
        # Fermer le navigateur
        driver.quit()
        
        return df

    def get_season_data(self, year):
        # Fonction pour récupérer et coller les données pour l'année spécifiée
        urls = {
            "base": f'https://fbref.com/en/comps/Big5/{year}/stats/players/{year}-Big-5-European-Leagues-Stats',
            "passing": f'https://fbref.com/en/comps/Big5/{year}/passing/players/{year}-Big-5-European-Leagues-Stats',
            "defense": f'https://fbref.com/en/comps/Big5/{year}/defense/players/{year}-Big-5-European-Leagues-Stats'
        }
        
        # Scraper les trois tableaux pour l'année donnée
        base_df = self.scrape_data(year, urls["base"], "stats_standard")
        passing_df = self.scrape_data(year, urls["passing"], "stats_passing")
        defense_df = self.scrape_data(year, urls["defense"], "stats_defense")
        
        # Vérifier si tous les DataFrames sont valides
        if base_df.empty or passing_df.empty or defense_df.empty:
            print(f"Erreur: Impossible de récupérer les données pour l'année {year}.")
            return pd.DataFrame()
        
        # Fusionner les DataFrames
        base_passing_df = pd.concat([base_df, passing_df], axis=1)
        final_df = pd.concat([base_passing_df, defense_df], axis=1)
        
        return final_df

    def collect_data(self, years):
        # Fonction pour scraper et collecter les données pour plusieurs années
        all_data = []
        
        for year in years:
            season_data = self.get_season_data(year)
            if not season_data.empty:
                all_data.append(season_data)

        # Concaténer tous les DataFrames dans un seul DataFrame
        if all_data:
            final_df = pd.concat(all_data, ignore_index=True)
            return final_df
        else:
            print("Aucune donnée trouvée pour les années spécifiées.")
            return pd.DataFrame()

    def save_to_excel(self, df, filename):
        # Fonction pour enregistrer les données collectées dans un fichier Excel
        if not df.empty:
            with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='All Seasons', index=False)
            print(f"Données enregistrées dans {filename}")
        else:
            print("Le DataFrame est vide, impossible de sauvegarder.")
