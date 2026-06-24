import pandas as pd
import re

class DataCleaner:
    def __init__(self, excel_path):
        self.excel_path = excel_path
        self.df = None
        self.df_cleaned = None
    
    def load_data(self):
        """Charge les données depuis le fichier Excel"""
        self.df = pd.read_excel(self.excel_path)
        return self
    
    def remove_duplicate_columns(self):
        """
        Supprime les colonnes dupliquées (en gardant la première occurrence).
        """
        column_names = self.df.columns.tolist()

        # Fonction pour extraire le nom de base d'une colonne (sans le suffixe .1, .2, etc.)
        def get_base_name(col_name):
            match = re.match(r'^(.+?)(?:\.(\d+))?$', str(col_name))
            if match:
                return match.group(1)
            return str(col_name)
        
        # Dictionnaire pour suivre les colonnes déjà vues
        base_names_seen = {}
        cols_to_keep = []

        for idx, col in enumerate(column_names):
            base_name = get_base_name(col)
            if base_name not in base_names_seen:
                base_names_seen[base_name] = idx
                cols_to_keep.append(idx)
        
        # Créer le DataFrame nettoyé en gardant uniquement les colonnes non dupliquées
        self.df_cleaned = self.df.iloc[:, cols_to_keep].copy()
        
        # Nettoyer les noms de colonnes (retirer les suffixes s'il en reste)
        cleaned_column_names = [get_base_name(col) for col in self.df_cleaned.columns]
        self.df_cleaned.columns = cleaned_column_names
        
        return self

    def remove_specific_columns(self):
        """
        Supprime les colonnes spécifiques à effacer.
        """
        columns_to_remove = [
            'Unnamed: 0_level_0 Rk', 'Unnamed: 7_level_0 Born', 'Unnamed: 37_level_0 Matches', 'Unnamed: 32_level_0 Matches',
            'Unnamed: 25_level_0 Matches', 'Unnamed: 8_level_0 90s', 'Unnamed: 31_level_0 PrgP', 'Unnamed: 24_level_0 xAG',
            'Unnamed: 23_level_0 Ast', 'Year',
        ]
        
        # Supprimer les colonnes spécifiées si elles existent
        self.df_cleaned.drop(columns=[col for col in columns_to_remove if col in self.df_cleaned.columns], inplace=True)
        
        return self

    def remove_all_duplicate_rows(self):
        """
        Supprime toutes les lignes dupliquées (en ne gardant aucune occurrence).
        """
        self.df_cleaned = self.df_cleaned[~self.df_cleaned.duplicated(keep=False)]
        return self

    def fill_empty_cells_with_zero(self):
        """
        Remplace toutes les cellules vides par 0.
        """
        self.df_cleaned.fillna(0, inplace=True)
        return self

    def remove_first_word_from_column(self, column_name):
        """
        Supprime le premier mot de chaque cellule dans la colonne spécifiée.
        """
        if column_name in self.df_cleaned.columns:
            # Appliquer une fonction pour chaque cellule dans la colonne
            self.df_cleaned[column_name] = self.df_cleaned[column_name].apply(lambda x: ' '.join(str(x).split()[1:]) if isinstance(x, str) else x)
        return self
    
    def remove_second_word_from_column(self, column_name):
        """
        Supprime le premier mot de chaque cellule dans la colonne spécifiée.
        """
        if column_name in self.df_cleaned.columns:
            # Appliquer une fonction pour chaque cellule dans la colonne
            self.df_cleaned[column_name] = self.df_cleaned[column_name].apply(lambda x: ''.join(str(x).split(',')[0]) if isinstance(x, str) else x)
        return self

    def rename_columns(self):
        """
        Renomme les colonnes selon le mappage fourni.
        """
        column_mapping = {
            'Unnamed: 1_level_0 Player': 'Player', 'Unnamed: 2_level_0 Nation': 'Nation', 'Unnamed: 3_level_0 Pos': 'Pos', 
            'Unnamed: 4_level_0 Squad': 'Team', 'Unnamed: 5_level_0 Comp': 'Comp', 'Unnamed: 6_level_0 Age': 'Age', 
            'Playing Time MP': 'MP', 'Playing Time Starts': 'Starts', 'Playing Time Min': 'Min', 'Playing Time 90s': '90s', 
            'Performance Gls': 'Gls', 'Performance Ast': 'Ast', 'Performance G+A': 'G+A', 'Performance G-PK': 'G-PK', 
            'Performance PK': 'PK', 'Performance PKatt': 'PKatt', 'Performance CrdY': 'CrdY', 'Performance CrdR': 'CrdR', 
            'Expected xG': 'xG', 'Expected npxG': 'npxG', 'Expected xAG': 'xAG', 'Expected npxG+xAG': 'npxG+xAG', 
            'Progression PrgC': 'PrgC', 'Progression PrgP': 'PrgP', 'Progression PrgR': 'PrgR', 'Per 90 Minutes Gls': 'Gls/90', 
            'Per 90 Minutes Ast': 'Ast/90', 'Per 90 Minutes G+A': 'G+A/90', 'Per 90 Minutes G-PK': 'G-PK/90', 
            'Per 90 Minutes G+A-PK': 'G+A-PK/90', 'Per 90 Minutes xG': 'xG/90', 'Per 90 Minutes xAG': 'xAG/90', 
            'Per 90 Minutes xG+xAG': 'xG+xAG/90', 'Per 90 Minutes npxG': 'npxG/90', 'Per 90 Minutes npxG+xAG': 'npxG+xAG/90', 
             'Total Cmp': 'Total Cmp', 'Total Att': 'Total Att', 'Total Cmp%': 'Total Cmp%', 'Total TotDist': 'TotDist', 
            'Total PrgDist': 'PrgDist', 'Short Cmp': 'Short Cmp', 'Short Att': 'Short Att', 'Short Cmp%': 'Short Cmp%', 
            'Medium Cmp': 'Med Cmp', 'Medium Att': 'Med Att', 'Medium Cmp%': 'Med Cmp%', 'Long Cmp': 'Long Cmp', 
            'Long Att': 'Long Att', 'Long Cmp%': 'Long Cmp%', 'Expected xA': 'xA', 'Expected A-xAG': 'A-xAG', 
            'Unnamed: 27_level_0 KP': 'KP', 'Unnamed: 28_level_0 1/3': '1/3', 'Unnamed: 29_level_0 PPA': 'PPA', 
            'Unnamed: 30_level_0 CrsPA': 'CrsPA', 'Tackles Tkl': 'Tkl', 'Tackles TklW': 'TklW', 'Tackles Def 3rd': 'Tkl Def 3rd', 
            'Tackles Mid 3rd': 'Tkl Mid 3rd', 'Tackles Att 3rd': 'Tkl Att 3rd', 'Challenges Tkl': 'Tkl Chllngs', 
            'Challenges Att': 'Att Chllngs', 'Challenges Tkl%': 'Tkl%', 'Challenges Lost': 'Chllngs Lost', 'Blocks Blocks': 'Blocks', 
            'Blocks Sh': 'Sh', 'Blocks Pass': 'Pass', 'Unnamed: 21_level_0 Int': 'Int', 'Unnamed: 22_level_0 Tkl+Int': 'Tkl+Int', 
            'Unnamed: 23_level_0 Clr': 'Clr', 'Unnamed: 24_level_0 Err': 'Err'
        }

        self.df_cleaned.rename(columns=column_mapping, inplace=True)
        
        return self

    def remove_rows_with_pos_gk(self):
        """
        Supprime les lignes où la colonne 'Pos' est égale à 'GK'.
        """
        self.df_cleaned = self.df_cleaned[self.df_cleaned['Pos'] != 'GK']
        return self
    
    def remove_rows_with_mp_below_6(self):
        """
        Supprime les lignes où la colonne 'MP' (Minutes Played) est inférieure à 6.
        La colonne 'MP' est d'abord convertie en numérique pour éviter les erreurs liées aux chaînes.
        """
        # Convertir la colonne 'MP' en numérique, forcer les erreurs à NaN (Not a Number)
        self.df_cleaned['MP'] = pd.to_numeric(self.df_cleaned['MP'], errors='coerce')
        
        # Supprimer les lignes où 'MP' est inférieur à 6 ou NaN
        self.df_cleaned = self.df_cleaned[self.df_cleaned['MP'] >= 15]
        
        return self


    def save_cleaned_data(self, output_path):
        """Sauvegarde les données nettoyées dans un fichier Excel"""
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            self.df_cleaned.to_excel(writer, sheet_name='Cleaned Data', index=False)
        
        return self

    def split_by_position(self, output_dir):
        """
        Divise le DataFrame en 3 fichiers Excel séparés selon le poste (DF, FW, MF).
        """
        positions = ['DF', 'FW', 'MF']
        
        for pos in positions:
            df_pos = self.df_cleaned[self.df_cleaned['Pos'] == pos]
            if not df_pos.empty:
                file_path = f"{output_dir}/{pos}_players.xlsx"
                with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                    df_pos.to_excel(writer, sheet_name=f"{pos} Players", index=False)
                print(f"Fichier pour {pos} enregistré à: {file_path}")
            else:
                print(f"Aucun joueur trouvé pour la position {pos}")
        
        return self

    def run_full_cleaning(self, output_path, split_output_dir):
        """Exécute le processus complet de nettoyage et de séparation des fichiers"""
        self.load_data()
        self.remove_duplicate_columns()
        self.remove_specific_columns()
        self.remove_all_duplicate_rows()  # Supprimer toutes les lignes dupliquées
        self.fill_empty_cells_with_zero()  # Remplacer les cellules vides par 0
        self.remove_first_word_from_column('Unnamed: 2_level_0 Nation')
        self.remove_first_word_from_column('Unnamed: 5_level_0 Comp')
        self.remove_second_word_from_column('Unnamed: 3_level_0 Pos')
        self.rename_columns()  # Renommer les colonnes
        self.remove_rows_with_pos_gk()  # Supprimer les lignes où la colonne 'Pos' est égale à 'GK'
        self.remove_rows_with_mp_below_6()  # Supprimer les lignes où 'MP' < 6
        self.save_cleaned_data(output_path)
        self.split_by_position(split_output_dir)  # Diviser en 3 fichiers par position
        return self.df_cleaned
