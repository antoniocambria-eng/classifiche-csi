import gspread
import requests
from google.oauth2.service_account import Credentials

# Configurazione delle credenziali e accesso a Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS_FILE = "credentials.json"

creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# ID del tuo foglio di calcolo
SPREADSHEET_ID = "1gtVEsFiozYI467yjxrf7N3TYH8gjsECk40D-nJ6zkvc"
spreadsheet = client.open_by_key(SPREADSHEET_ID)
sheet = spreadsheet.sheet1

def aggiorna_classifica_2015():
    print("Aggiornamento Classifica 2015 in corso...")
    dati_2015 = [
        ["#", "Squadra", "Pt", "PG", "V", "N", "P", "GF", "GS", "DR"],
        [1, "Pol. Atletico Sala Bologna", 12, 4, 4, 0, 0, 21, 7, 14],
        [2, "Atletic River Blu", 9, 3, 3, 0, 0, 13, 3, 10],
        [3, "Monari Nasi San Damaso", 4, 3, 1, 1, 1, 7, 9, -2],
        [4, "Pol. Saliceta", 4, 4, 1, 1, 2, 4, 8, -4],
        [5, "Fc Spilamberto Verde", 2, 3, 0, 2, 1, 6, 8, -2],
        [6, "Pol. Cognentese", 2, 3, 0, 2, 1, 4, 6, -2],
        [7, "S.E.L.E.S. Castelfranco", 1, 3, 0, 1, 2, 4, 8, -4],
        [8, "Atletic C.D.R. Mutina", 1, 3, 0, 1, 2, 0, 10, -10]
    ]
    sheet.update("H3:Q11", dati_2015)
    print("Classifica 2015 aggiornata con successo!")

def aggiorna_classifica_2014():
    print("Aggiornamento Classifica 2014 in corso...")
    dati_2014 = [
        ["#", "Squadra", "Pt", "PG", "V", "N", "P", "GF", "GS", "DR"],
        [1, "F.C. Spilamberto", 9, 3, 3, 0, 0, 18, 1, 17],
        [2, "Monari Nasi San Damaso", 6, 4, 2, 0, 2, 18, 20, -2],
        [3, "Pol. Atletico Sala Anzola Bianca", 4, 3, 1, 1, 1, 20, 7, 13],
        [4, "Serramazzoni", 4, 2, 1, 1, 0, 8, 6, 2],
        [5, "Solignano 2014", 3, 2, 1, 0, 1, 6, 7, -1],
        [6, "Amici Carlo Acutis", 3, 3, 1, 0, 2, 3, 23, -20],
        [7, "Visport", 0, 3, 0, 0, 3, 3, 12, -9]
    ]
    sheet.update("H15:Q22", dati_2014)
    print("Classifica 2014 aggiornata con successo!")

if __name__ == "__main__":
    aggiorna_classifica_2015()
    aggiorna_classifica_2014()
