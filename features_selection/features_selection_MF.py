import os
import pandas as pd

class FeatureSelectionMF:
    def __init__(self, input_file_path, output_dir):
        self.input_file_path = input_file_path
        self.output_dir = output_dir
        self.output_file_path = os.path.join(output_dir, "features_MF_selected.xlsx")
        self.df = None

    def load_data(self):
        """Charge les données depuis le fichier Excel"""
        self.df = pd.read_excel(self.input_file_path)
        return self

    def select_features(self):
        """Garde uniquement les colonnes pertinentes pour les milieux (MF)"""
        selected_columns = [
            
            'Player','Total Cmp', 'Total Att', 'Total Cmp%',
            'Short Cmp', 'Short Att', 'Short Cmp%',
            'Med Cmp', 'Med Att', 'Med Cmp%',
            'Long Cmp', 'Long Att', 'Long Cmp%',
            'TotDist', 'PrgDist',
            'PrgC', 'PrgP', 'PrgR',
            'KP', '1/3', 'PPA', 'CrsPA',
            'xA', 'xAG', 'A-xAG',
            'Ast', 'G+A', 'G+A/90',
            'Att Chllngs', 'Tkl Chllngs', 'Chllngs Lost', 'Tkl%',
            'Ligue_Weight', 'Pass/90',	'KP/90','PrgC/90','PrgP/90','Chllngs Lost/90','Ligue_Weight'

        ]

        # Ne garder que les colonnes existantes
        columns_to_keep = [col for col in selected_columns if col in self.df.columns]
        self.df = self.df[columns_to_keep]

        return self

    def save_selected_features(self):
        """Sauvegarde le DataFrame filtré"""
        os.makedirs(self.output_dir, exist_ok=True)

        with pd.ExcelWriter(self.output_file_path, engine="xlsxwriter") as writer:
            self.df.to_excel(writer, sheet_name="MF_Features", index=False)

        return self

    def run_feature_selection(self):
        """Pipeline complet"""
        self.load_data()
        self.select_features()
        self.save_selected_features()
        return self.df
input_file = r"C:\Users\Aref Bakali\OneDrive\Bureau\Projet Python\data\features\features_MF.xlsx"
output_dir = r"C:\Users\Aref Bakali\OneDrive\Bureau\Projet Python\data\selection"

selector = FeatureSelectionMF(input_file, output_dir)
df_mf_selected = selector.run_feature_selection()

print("Feature selection MF terminée :", df_mf_selected.shape)
