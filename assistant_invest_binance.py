import s²reamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from binance.client import Client

# Configuration de l'API Binance
api_key = 'JjI8LsCdNUwW21kZZc02hR2SQqNELhLIvii5uEtwWwisg599VOBZfizDoUvOsG5d'
api_secret = 'F9VFPLan763C7xGc9j69IIdqZGKm2R4bAQ5R34nA8lzHry6Mg8QKVubVFjPV78JK'
client_binance = Client(api_key, api_secret)

# Récupérer les données du portefeuille Binance
account_info = client_binance.get_account()
balances = account_info['balances']
holdings = {balance['asset']: float(balance['free']) for balance in balances if float(balance['free']) > 0}
prices_from_binance = client_binance.get_all_tickers()
prices_dict = {price['symbol']: float(price['price']) for price in prices_from_binance}

# Calculer la valeur en USD de chaque crypto-monnaie
values = {asset: holdings[asset] * prices_dict.get(f"{asset}USDT", 0) for asset in holdings}

# Convertir en DataFrame pour plus de simplicité
df = pd.DataFrame(list(values.items()), columns=['Crypto', 'Valeur (USD)'])

# Répartition du Portefeuille (Graphique en Secteurs)
st.title("Tableau de Bord du Portefeuille de Cryptomonnaies")
st.header("Répartition Actuelle du Portefeuille")
fig1, ax1² = plt.subplots()
ax1.pie(df['Valeur (USD)'], labels=df['Crypto'], autopct='%1.1f%%', startangle=90)
ax1.axis('equal')  # Pour un cercle parfait
st.pyplot(fig1)

# Evolution de la Valeur du Portefeuille au Cours du Temps
st.header("Évolution de la Valeur du Portefeuille")
# Simuler des données historiques (remplacer par des données réelles si disponible)
dates = pd.date_range(end=pd.Timestamp.today(), periods=30)
historical_values = df['Valeur (USD)'].sum() * (1 + 0.01 * (pd.Series(range(30)) - 15).cumsum() / 100)
historical_df = pd.DataFrame({'Date': dates, 'Valeur Totale (USD)': historical_values})
fig2, ax2 = plt.subplots()
ax2.plot(historical_df['Date'], historical_df['Valeur Totale (USD)'])
ax2.set_xlabel('Date')
ax2.set_ylabel('Valeur Totale (USD)')
st.pyplot(fig2)

# Performances des Différentes Cryptomonnaies (Graphique en Barres)
st.header("Performances des Différentes Cryptomonnaies")
# Simuler les pourcentages de gain/perte (remplacer par des données réelles)
df['Performance (%)'] = 100 * (df['Valeur (USD)'] / df['Valeur (USD)'].iloc[0] - 1)
fig3, ax3 = plt.subplots()
ax3.bar(df['Crypto'], df['Performance (%)'])
ax3.set_ylabel('Performance (%)')
st.pyplot(fig3)

