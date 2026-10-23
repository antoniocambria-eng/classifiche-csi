import os
import json
import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials

# 1. URL ufficiali delle due classifiche CSI
URL_2015 = "https://live.centrosportivoitaliano.it/26/Calcio-a-11/Emilia-Romagna/Modena/C36151/?j=NEU9REhFJjRGPVBOWSY0Rz1HSkVJRSY0SD1GTEhESUwmNEk9VHY0MTByIE8mNEw9REhFJjQyPWU="
URL_2014 = "https://live.centrosportivoitaliano.it/26/Calcio-a-11/Emilia-Romagna/Modena/C36151/?j=NEU9REhFJjRGPVBOWSY0Rz1HSkVJRSY0SD1GTEhESUkmNEk9VHY0MTByIFAmNEw9REhFJjQyPWU="

def estrai_classifica_csi(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    if not table:
        raise ValueError(f"Nessuna tabella trovata all'URL: {url}")

    dati = []
    
    # Intestazioni della tabella
    headers_list = [th.get_text(strip=True) for th in table.find_all("th")]
    if headers_list:
        dati.append(headers_list)

    # Righe di dati
    for row in table.find_all("tr"):
        cols = [td.get_text(strip=True) for td in row.find_all("td")]
        if cols:
            dati.append(cols)

    return dati

# 2. Autenticazione con Google Sheets
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

CREDS_FILE = "credentials.json"
if not os.path.exists(CREDS_FILE):
    raise FileNotFoundError("File credentials.json non trovato.")

creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# 3. Apertura del foglio "Campionati" e della scheda "Date"
spreadsheet = client.open("Campionati")
sheet = spreadsheet.worksheet("Date")

# 4. Estrazione dei dati
print("Estrazione classifica 2015...")
dati_2015 = estrai_classifica_csi(URL_2015)

print("Estrazione classifica 2014...")
dati_2014 = estrai_classifica_csi(URL_2014)

# 5. Preparazione del blocco unico per la colonna H
# Pulisce l'area della colonna H e vicine prima di riscrivere
sheet.batch_clear(["H1:Z100"])

# Blocco 2015
blocco_2015 = [["CLASSIFICA 2015"]] + dati_2015

# Calcolo riga d'inizio per la classifica 2014 (lascia 2 righe vuote dopo la 2015)
riga_inizio_2014 = len(blocco_2015) + 3

blocco_2014 = [["CLASSIFICA 2014"]] + dati_2014

# 6. Scrittura sul foglio Google
sheet.update(f"H1", blocco_2015)
sheet.update(f"H{riga_inizio_2014}", blocco_2014)

print("Classifiche 2015 e 2014 aggiornate con successo a destra nella scheda Date!")
