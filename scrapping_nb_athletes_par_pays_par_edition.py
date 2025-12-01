import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# -----------------------------
# 1) Tableau d’URLs à remplir
# -----------------------------
# Exemple de structure à compléter :
urls = {
    "France": {
        2012: "https://fr.wikipedia.org/wiki/France_aux_Jeux_paralympiques_d%27%C3%A9t%C3%A9_de_2012",
        2016: "https://fr.wikipedia.org/wiki/France_aux_Jeux_paralympiques_d%27%C3%A9t%C3%A9_de_2016",
        2020: "https://fr.wikipedia.org/wiki/France_aux_Jeux_paralympiques_d%27%C3%A9t%C3%A9_de_2020",
        2024: "https://fr.wikipedia.org/wiki/France_aux_Jeux_paralympiques_d%27%C3%A9t%C3%A9_de_2024",
    },
    "Allemagne": {
        2012: "URL_ALLEMAGNE_2012",
        2016: "URL_ALLEMAGNE_2016",
        2020: "URL_ALLEMAGNE_2020",
        2024: "URL_ALLEMAGNE_2024",
    },
    # ...
    # Ajoute ici les 8 autres pays
}

# -----------------------------
# 2) Fonction pour scraper un URL Wikipédia
# -----------------------------
headers = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

def extract_athletes(url):
    """Renvoie le nombre d’athlètes depuis une page Wikipédia."""
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    infobox = soup.find("table", {"class": "infobox"})
    if infobox is None:
        return None

    for row in infobox.find_all("tr"):
        header = row.find("th")
        if header and "Athlètes" in header.text:
            value_cell = row.find("td")
            if value_cell:
                match = re.search(r"\d+", value_cell.text)
                if match:
                    return int(match.group(0))
    return None

# -----------------------------
# 3) Construction du DataFrame
# -----------------------------
annees = [2012, 2016, 2020, 2024]
pays_liste = list(urls.keys())

df = pd.DataFrame(index=pays_liste, columns=annees)

for pays in urls:
    for annee in urls[pays]:
        url = urls[pays][annee]
        print(f"Scraping {pays} - {annee}...")
        nb = extract_athletes(url)
        df.loc[pays, annee] = nb

# -----------------------------
# 4) Résultat final
# -----------------------------
print("\n===== TABLEAU FINAL =====")
print(df)

# Export CSV si besoin
df.to_csv("nb_athletes_paralympiques.csv")
