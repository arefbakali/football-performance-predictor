import pandas as pd
import numpy as np
 

class FeatureEngineeringFW:
    def __init__(self, file_path):
        # Charger le fichier Excel
        self.df = pd.read_excel(file_path)
        self.df_cleaned = self.df.copy()  # Faire une copie du DataFrame original
    
    def add_offensive_features(self):
        # Ajouter des colonnes spécifiques aux attaquants
        self.df_cleaned['Gls/90'] = self.df_cleaned['Gls'] / self.df_cleaned['90s']
        self.df_cleaned['xG/90'] = self.df_cleaned['xG'] / self.df_cleaned['90s']
        self.df_cleaned['Gls - xG'] = self.df_cleaned['Gls'] - self.df_cleaned['xG']
        self.df_cleaned['Sh/90'] = self.df_cleaned['Sh'] / self.df_cleaned['90s']
        self.df_cleaned['KP/90'] = self.df_cleaned['KP'] / self.df_cleaned['90s']
        self.df_cleaned['xAG/90'] = self.df_cleaned['xAG'] / self.df_cleaned['90s']
    
    
    def add_league_weight(self):
        # Ajouter le poids de chaque ligue (selon sa compétitivité)
        league_weights = {
            'Premier League': 1.5,
            'La Liga': 1.4,
            'Serie A': 1.2,
            'Ligue 1': 1.1,
            'Bundesliga': 1.3
        }
        self.df_cleaned['Ligue_Weight'] = self.df_cleaned['Comp'].map(league_weights)
       
    def save_to_excel(self, output_path):
        # Sauvegarder les données traitées dans un nouveau fichier Excel
        self.df_cleaned.to_excel(output_path, index=False)
    
    def process_data(self, output_path):
        # Exécuter toutes les étapes de feature engineering
        self.add_offensive_features()
        self.add_league_weight()

        
        # Sauvegarder le fichier avec les nouvelles features
        self.save_to_excel(output_path)
        
        return self.df_cleaned

# Utilisation de la classe avec le chemin spécifié
input_file_path = r'C:\Users\Aref Bakali\OneDrive\Bureau\Projet Python\data\cleaned\FW_players.xlsx'  # Remplacer par ton chemin local
output_file_path = r'C:\Users\Aref Bakali\OneDrive\Bureau\Projet Python\data\features\features_FW.xlsx'  # Fichier de sortie
fe = FeatureEngineeringFW(input_file_path)
processed_df = fe.process_data(output_file_path)

# Afficher un message de confirmation
print(f"Le fichier traité a été sauvegardé sous : {output_file_path}")