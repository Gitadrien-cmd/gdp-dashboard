import time
import requests
import pandas as pd
import gspread
from binance.client import Client
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import matplotlib.pyplot as plt

# --- 1. Configurations de l'API Binance ---
api_key = 'JjI8LsCdNUwW21kZZc02hR2SQqNELhLIvii5uEtwWwisg599VOBZfizDoUvOsG5d'
api_secret = 'F9VFPLan763C7xGc9j69IIdqZGKm2R4bAQ5R34nA8lzHry6Mg8QKVubVFjPV78JK'
client_binance = Client(api_key, api_secret)

# --- 2. Authentification avec l'API de Google Sheets ---
creds_file = "H:/mad max k32/Documents/python-invest/invest-431911.json"
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
client_gs = gspread.authorize(creds)

# --- 3. Paramètres de conversion et d'optimisation ---
eur_to_usd = 1.10  # Taux de conversion fixe pour l'exemple (à ajuster selon les besoins)

# --- 4. Récupérer les données du portefeuille Binance ---
account_info = client_binance.get_account()
balances = account_info['balances']

# Filtrer les cryptomonnaies ayant un solde non nul
holdings = {balance['asset']: float(balance['free']) for balance in balances if float(balance['free']) > 0}

# Obtenir les prix actuels des cryptomonnaies en USD
prices = client_binance.get_all_tickers()
prices_dict = {price['symbol']: float(price['price']) for price in prices}

# Calculer la valeur en EUR de chaque cryptomonnaie détenue
values = {asset: holdings[asset] * prices_dict.get(f"{asset}USDT", 0) / eur_to_usd for asset in holdings}

# --- 5. Mise à jour des données dans Google Sheets ---
sheet = client_gs.open("feuilledecalculwallet").sheet1

# Préparer les données pour la mise à jour
lignes = [[asset, holdings[asset], values[asset]] for asset in holdings]
lignes.append(["Total", "", sum(values.values())])

# Effacer les données existantes (facultatif)
sheet.clear()

# Insérer les nouvelles données dans Google Sheets
sheet.update("A1", [["Crypto", "Quantité", "Valeur (EUR)"]] + lignes)
print("Mise à jour de la feuille de calcul terminée.")

# --- 6. Visualisation avec Streamlit ---
st.title("Tableau de Bord du Portefeuille de Cryptomonnaies")

# --- Répartition du Portefeuille ---
st.header("Répartition Actuelle du Portefeuille")
fig1, ax1 = plt.subplots()
# Grouper les petites valeurs sous "Autres"
autres = 0.0
labels = []
sizes = []
for asset, value in values.items():
    if value / sum(values.values()) < 0.05:
        autres += value
    else:
        labels.append(asset)
        sizes.append(value)
if autres > 0:
    labels.append('Autres')
    sizes.append(autres)
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
st.pyplot(fig1)

# --- Évolution de la Valeur du Portefeuille au Fil du Temps ---
st.header("Évolution de la Valeur du Portefeuille")
# Pour cet exemple, nous générons des données factices
dates = pd.date_range(start="2023-01-01", periods=30, freq='D')
historical_values = [sum(values.values()) * (1 + 0.01 * (i - 15)**2) for i in range(30)]
historical_df = pd.DataFrame({"Date": dates, "Valeur Totale (EUR)": historical_values})
fig2, ax2 = plt.subplots()
ax2.plot(historical_df["Date"], historical_df["Valeur Totale (EUR)"])
st.pyplot(fig2)

# --- Performances des Différentes Cryptomonnaies ---
st.header("Performances des Différentes Cryptomonnaies")
initial_investments = {asset: value / 1.2 for asset, value in values.items()}  # Exemples d'investissements initiaux
performance = {}
for asset in values:
    if asset in initial_investments and initial_investments[asset] > 0:
        performance[asset] = (values[asset] - initial_investments[asset]) / initial_investments[asset] * 100
    else:
        performance[asset] = 0  # Si l'investissement initial est zéro ou non défini, on ne calcule pas la performance

performance_df = pd.DataFrame(list(performance.items()), columns=["Crypto", "Performance (%)"])
fig3, ax3 = plt.subplots()
ax3.bar(performance_df["Crypto"], performance_df["Performance (%)"])
st.pyplot(fig3)

# Affichage final dans la console
print(f"Valeur totale actuelle (EUR) : {sum(values.values()):.2f}")
print("Script terminé.")
