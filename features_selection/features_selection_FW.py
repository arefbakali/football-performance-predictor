import pandas as pd

class FeatureSelectionFW:
    def __init__(self, input_file_path, output_file_path):
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.df = None
    
    def load_data(self):
        """Charge les données depuis le fichier Excel"""
        self.df = pd.read_excel(self.input_file_path)
        print(f"✓ Données chargées avec succès: {self.df.shape[0]} lignes, {self.df.shape[1]} colonnes")
        return self
    
    def select_features(self):
        """Sélectionne uniquement les colonnes spécifiées pour les joueurs FW"""
        selected_columns = [
            'Player','MP', 'Starts', 'Min', '90s', 'Gls', 'Ast', 'G+A', 'G-PK', 'PK', 'PKatt', 'CrdY', 'CrdR',
            'xG', 'npxG', 'xAG', 'npxG+xAG', 'PrgC', 'PrgP', 'PrgR', 'Gls/90', 'Ast/90', 'G+A/90', 'G-PK/90',
            'G+A-PK/90', 'xG/90', 'xAG/90', 'xG+xAG/90', 'npxG/90', 'npxG+xAG/90', 'Total Cmp', 'Total Att',
            'Total Cmp%', 'TotDist', 'PrgDist', 'Short Cmp', 'Short Att', 'Short Cmp%', 'Med Cmp', 'Med Att',
            'Med Cmp%', 'Long Cmp', 'Long Att', 'Long Cmp%', 'xA', 'A-xAG', 'KP', '1/3', 'PPA', 'CrsPA',  
            'Gls - xG', 'Sh/90', 'KP/90', 'Ligue_Weight'
        ]
        
        # Vérifier si les colonnes spécifiées existent dans le DataFrame
        columns_to_keep = [col for col in selected_columns if col in self.df.columns]
        
        # Filtrer le DataFrame en ne gardant que les colonnes sélectionnées
        self.df = self.df[columns_to_keep]
        print(f"✓ Sélection des caractéristiques terminée: {self.df.shape[0]} lignes, {self.df.shape[1]} colonnes")
        return self
    
    def save_selected_features(self):
        """Sauvegarde les données sélectionnées dans un fichier Excel"""
        with pd.ExcelWriter(self.output_file_path, engine='xlsxwriter') as writer:
            self.df.to_excel(writer, sheet_name='Selected Features', index=False)
        print(f"✓ Fichier sauvegardé avec succès à {self.output_file_path}")
        return self
    
    def run_feature_selection(self):
        """Exécute l'ensemble du processus de sélection des caractéristiques"""
        self.load_data()
        self.select_features()
        self.save_selected_features()
        return self.df

# Chemin d'entrée et de sortie
input_file_path = r"C:\Users\Aref Bakali\OneDrive\Bureau\Projet Python\data\features\features_FW.xlsx"
output_file_path = r"C:\Users\Aref Bakali\OneDrive\Bureau\Projet Python\data\selection\features_FW_selected.xlsx"

# Exécution de la sélection des caractéristiques
feature_selection = FeatureSelectionFW(input_file_path, output_file_path)
feature_selection.run_feature_selection()
