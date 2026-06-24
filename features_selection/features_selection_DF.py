import os
import pandas as pd

class FeatureSelectionDF:
    def __init__(self, input_file_path, output_dir):
        self.input_file_path = input_file_path
        self.output_dir = output_dir
        self.output_file_path = os.path.join(output_dir, "features_DF_selected.xlsx")
        self.df = None

    def load_data(self):
        """Charge les données depuis le fichier Excel"""
        self.df = pd.read_excel(self.input_file_path)
        return self

    def select_features(self):
        """Garde uniquement les colonnes pertinentes pour les défenseurs (DF)"""
        selected_columns = [
            'Player','Tkl', 'TklW', 'Int', 'Tkl+Int',
            'Blocks', 'Clr',
            'Tkl Def 3rd', 'Tkl Mid 3rd', 'Tkl Att 3rd',
            'Tkl Chllngs', 'Att Chllngs', 'Tkl%', 'Chllngs Lost',
            'Err', 'Sh', 'Pass',
            'Gls', 'xG', 'npxG',
            'Total Cmp', 'Total Att', 'Total Cmp%',
            'PrgDist',
            'Ligue_Weight',    "Tkl/90",
    "Int/90",
    "Blocks/90",
    "Clr/90",
    "Gls/90"
        ]

        # Ne garder que les colonnes réellement présentes
        columns_to_keep = [col for col in selected_columns if col in self.df.columns]
        self.df = self.df[columns_to_keep]

        return self

    def save_selected_features(self):
        """Sauvegarde le DataFrame filtré"""
        os.makedirs(self.output_dir, exist_ok=True)

        with pd.ExcelWriter(self.output_file_path, engine="xlsxwriter") as writer:
            self.df.to_excel(writer, sheet_name="DF_Features", index=False)

        return self

    def run_feature_selection(self):
        """Pipeline complet de sélection des features DF"""
        self.load_data()
        self.select_features()
        self.save_selected_features()
        return self.df
input_file = r"C:\Users\Aref Bakali\OneDrive\Bureau\Projet Python\data\features\features_DF.xlsx"
output_dir = r"C:\Users\Aref Bakali\OneDrive\Bureau\Projet Python\data\selection"

selector = FeatureSelectionDF(input_file, output_dir)
df_df_selected = selector.run_feature_selection()

print("Feature selection DF terminée :", df_df_selected.shape)
