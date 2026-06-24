# ======================================================
# 📦 IMPORTS
# ======================================================
import streamlit as st
import pandas as pd
import os
import joblib

# ======================================================
# 📂 PATHS — relatifs au dossier du script
# ======================================================
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MODEL_ROOT = os.path.join(BASE_DIR, "ML_Notebooks")
DATA_ROOT  = os.path.join(BASE_DIR, "data", "selection")

# ======================================================
# ⚙️ CONFIG
# ======================================================
CONFIG = {
    "FW": {
        "data": os.path.join(DATA_ROOT, "features_FW_selected.xlsx"),
        "targets": ["Gls - xG", "G-PK", "KP/90", "Ast/90", "Gls/90"],
        "models": {
            "Gls - xG": "best_FW_Gls_-_xG.pkl",
            "G-PK":     "best_FW_G-PK.pkl",
            "KP/90":    "best_FW_KP_90.pkl",
            "Ast/90":   "best_FW_Ast_90.pkl",
            "Gls/90":   "best_FW_Gls_90.pkl",
        }
    },
    "MF": {
        "data": os.path.join(DATA_ROOT, "features_MF_selected.xlsx"),
        "targets": ["Total Cmp%", "PrgC/90", "PrgP/90", "Chllngs Lost/90", "KP/90"],
        "models": {
            "Total Cmp%":      "best_MF_Total_Cmp%.pkl",
            "PrgC/90":         "best_MF_PrgC_90.pkl",
            "PrgP/90":         "best_MF_PrgP_90.pkl",
            "Chllngs Lost/90": "best_MF_Chllngs_Lost_90.pkl",
            "KP/90":           "best_MF_KP_90.pkl",
        }
    },
    "DF": {
        "data": os.path.join(DATA_ROOT, "features_DF_selected.xlsx"),
        "targets": ["Tkl/90", "Int/90", "Blocks/90", "Clr/90", "Gls/90"],
        "models": {
            "Tkl/90":    "best_DF_Tkl_90.pkl",
            "Int/90":    "best_DF_Int_90.pkl",
            "Blocks/90": "best_DF_Blocks_90.pkl",
            "Clr/90":    "best_DF_Clr_90.pkl",
            "Gls/90":    "best_DF_Gls_90.pkl",
        }
    }
}

# ======================================================
# 📊 DATASET
# ======================================================
class Dataset:
    def __init__(self, path):
        self.df = pd.read_excel(path)

    def available_players(self):
        return sorted(self.df["Player"].unique())

    def last_row(self, player):
        return self.df[self.df["Player"] == player].iloc[-1:]

    def features_only(self, targets):
        return self.df.drop(columns=targets + ["Player"])

# ======================================================
# 🧠 LOAD MODELS
# ======================================================
def load_models(model_map):
    models = {}
    for target, fname in model_map.items():
        path = os.path.join(MODEL_ROOT, fname)
        models[target] = joblib.load(path)
    return models

# ======================================================
# 🔮 PREDICTIONS
# ======================================================
def predict_existing_player(dataset, models, targets, player):
    row = dataset.last_row(player)
    X = row.drop(columns=targets + ["Player"])

    # Réordonner les colonnes selon ce qu'attend le scaler
    first_target = targets[0]
    expected_cols = list(models[first_target]["scaler"].feature_names_in_)
    X = X[expected_cols]

    results = []
    for target in targets:
        obj = models[target]
        pred = obj["model"].predict(obj["scaler"].transform(X))[0]
        real = row[target].values[0]
        results.append({
            "Target":    target,
            "Real":      round(real, 3),
            "Predicted": round(pred, 3),
            "Error":     round(pred - real, 3),
            "Model":     obj["model_name"]
        })

    return pd.DataFrame(results)

def predict_new_player(X_new, models, targets):
    # Réordonner les colonnes selon ce qu'attend le scaler
    first_target = targets[0]
    expected_cols = list(models[first_target]["scaler"].feature_names_in_)
    X_new = X_new[expected_cols]

    rows = []
    for target in targets:
        obj = models[target]
        pred = obj["model"].predict(obj["scaler"].transform(X_new))[0]
        rows.append({
            "Target":    target,
            "Predicted": round(pred, 3),
            "Model":     obj["model_name"]
        })

    return pd.DataFrame(rows)

# ======================================================
# 🎨 STREAMLIT UI
# ======================================================
st.set_page_config("⚽ Football Predictor", layout="wide")
st.title("⚽ Football Performance Predictor")

POSTE = st.sidebar.selectbox("📌 Choisir le poste", ["FW", "MF", "DF"])
cfg = CONFIG[POSTE]

dataset = Dataset(cfg["data"])
models  = load_models(cfg["models"])

# ======================================================
# 👤 EXISTING PLAYER
# ======================================================
st.header("👤 Joueur existant")

player = st.selectbox("Choisir un joueur", dataset.available_players())

if st.button("🔮 Prédire performances"):
    df_res = predict_existing_player(dataset, models, cfg["targets"], player)
    st.dataframe(df_res, use_container_width=True)

# ======================================================
# ➕ NEW PLAYER
# ======================================================
st.header("➕ Nouveau joueur")

X_template = dataset.features_only(cfg["targets"]).iloc[[0]]
# Réordonner le template selon les features attendues par le modèle
first_target = cfg["targets"][0]
expected_cols = list(models[first_target]["scaler"].feature_names_in_)
X_template = X_template[expected_cols]

inputs = {}
for col in X_template.columns:
    inputs[col] = st.number_input(col, float(X_template[col].iloc[0]))

if st.button("🚀 Prédire nouveau joueur"):
    X_new = pd.DataFrame([inputs])
    df_new = predict_new_player(X_new, models, cfg["targets"])
    st.dataframe(df_new, use_container_width=True)
