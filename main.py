import os
import pandas as pd
from scraper.PlayersScraper import WebScraper
from cleaning.clean_players import DataCleaner

def main():
    driver_path = 'C:/WebDriver/msedgedriver.exe'
    raw_data_path = os.path.join('data', 'raw')
    cleaned_data_path = os.path.join('data', 'cleaned')
    split_data_path = os.path.join('data', 'cleaned')  # Nouveau dossier pour les fichiers séparés par position
    raw_file_path = os.path.join(raw_data_path, 'player_stats_combined_all_years.xlsx')
    cleaned_file_path = os.path.join(cleaned_data_path, 'player_stats_cleaned_all_years.xlsx')
    
    os.makedirs(raw_data_path, exist_ok=True)
    os.makedirs(cleaned_data_path, exist_ok=True)
    os.makedirs(split_data_path, exist_ok=True)  # Créer le dossier pour les fichiers divisés
    
    # Étape 1: Scraping des données
    if os.path.exists(raw_file_path):
        print(f"Le fichier brut existe déjà: {raw_file_path}")
        try:
            final_df = pd.read_excel(raw_file_path, sheet_name='All Seasons')
            print(f"✓ Données chargées avec succès: {final_df.shape[0]} lignes, {final_df.shape[1]} colonnes")
        except Exception as e:
            print(f"✗ Erreur lors du chargement: {e}")
            final_df = None
    else:
        print("Le fichier brut n'existe pas encore. Lancement du scraping...")
        final_df = None
    
    # Si les données n'ont pas été chargées, lancer le scraping
    if final_df is None:
        try:
            print(f"\nInitialisation du WebScraper avec le driver: {driver_path}")
            scraper = WebScraper(driver_path=driver_path)
            
            years = ['2022-2023', '2023-2024', '2024-2025']
            print(f"Années à scraper: {', '.join(years)}")
            
            print("\nDébut du scraping...")
            final_df = scraper.collect_data(years)
            
            if not final_df.empty:
                print(f"✓ Scraping terminé avec succès! {final_df.shape[0]} lignes collectées.")
                scraper.save_to_excel(final_df, raw_file_path)
                print("✓ Données brutes sauvegardées avec succès!")
            else:
                print("✗ ERREUR: Aucune donnée récupérée.")
                return None
        
        except Exception as e:
            print(f"✗ ERREUR lors du scraping: {e}")
            return None
    
    # Étape 2: Nettoyage des données
    print("Suppression des colonnes dupliquées...")
    try:
        cleaner = DataCleaner(raw_file_path)
        df_cleaned = cleaner.run_full_cleaning(cleaned_file_path, split_data_path)  # Passer le répertoire pour les fichiers séparés
        print(f"✓ Nettoyage terminé avec succès: {df_cleaned.shape[0]} lignes, {df_cleaned.shape[1]} colonnes.")
    except Exception as e:
        print(f"✗ ERREUR lors du nettoyage: {e}")
        return None
    
    return df_cleaned

if __name__ == "__main__":
    try:
        df_final = main()
        if df_final is not None:
            print(f"✓ Programme terminé avec succès! {df_final.shape[0]} lignes, {df_final.shape[1]} colonnes.")
        else:
            print("⚠️ Le programme s'est terminé avec des erreurs.")
    except Exception as e:
        print(f"✗ ERREUR CRITIQUE: {e}")
