import requests

test_zip = "4000"
api_url = f"https://immovlan.be/en/api/core/autocomplete?query={test_zip}&countryId=318"

# Aggiungiamo l'identità del browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(api_url, headers=headers)

# Verifichiamo se la risposta è andata a buon fine (200)
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Errore {response.status_code}: Il sito ci ha bloccato o l'URL è cambiato.")
