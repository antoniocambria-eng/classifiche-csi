import os
import json
import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials

# 1. Definizione degli URL
URL_2015 = "https://live.centrosportivoitaliano.it/26/Calcio-a-11/Emilia-Romagna/Modena/C36151/?j=NEU9REhFJjRGPVBOWSY0Rz1HSkVJRSY0SD1GTEhESUwmNEk9VHY0MTByIE8mNEw9REhFJjQyPWU="
URL_2014 = "https://live.centrosportivoitaliano.it/26/Calcio-a-11/Emilia-Romagna/Modena/C36151/?j=NEU9REhFJjRGPVBOWSY0Rz1HSkVJRSY0SD1GTEhESUkmNEk9VHY0MTByIFAmNEw9REhFJjQyPWU="

# 2. Scraper della tabella dal sito CSI
def estrai_classifica_csi(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Cerca la prima tabella presente nella pagina
    table = soup.find("table")
    if not table:
        raise ValueError(f"Nessuna tabella trovata nell'URL: {url}")

    dati = []
    
    # Intestazioni (th)
    headers_list = []
    for th in table.find_all("th"):
        headers_list.append(th.get_text(strip=True))
    if headers_list:
        dati.append(headers_list)

    # Righe della classifica (tr)
    for row in table.find_all("tr"):
        cols = [td.get_text(strip=True) for td in row.find_all("td")]
        if cols:
            dati.append(cols)

    return dati

# 3. Autenticazione con Google Sheets
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

CREDS_FILE = "credentials.json"

if not os.path.exists(CREDS_FILE):
    raise FileNotFoundError("Il file credentials.json non esiste. Assicurati che il passo precedente lo crei correttamente.")

creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# 4. Apertura del Foglio Google
# Assicurati che il nome del file su Google Drive coincida perfettamente
spreadsheet = client.open("Classifiche CSI")

# 5. Estrazione e Aggiornamento Classifica 2015
print("Estrazione classifica 2015...")
dati_2015 = estrai_classifica_csi(URL_2015)
sheet_2015 = spreadsheet.worksheet("2015")
sheet_2015.clear()
sheet_2015.update("A1", dati_2015)
print("Classifica 2015 aggiornata con successo!")

# 6. Estrazione e Aggiornamento Classifica 2014
print("Estrazione classifica 2014...")
dati_2014 = estrai_classifica_csi(URL_2014)
sheet_2014 = spreadsheet.worksheet("2014")
sheet_2014.clear()
sheet_2014.update("A1", dati_2014)
print("Classifica 2014 aggiornata con successo!")

print("Tutti i fogli sono stati aggiornati correttamente!")
