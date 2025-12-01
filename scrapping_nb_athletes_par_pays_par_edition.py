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
        2012: "https://en.wikipedia.org/wiki/France_at_the_2012_Summer_Paralympics",
        2016: "https://en.wikipedia.org/wiki/France_at_the_2016_Summer_Paralympics",
        2020: "https://en.wikipedia.org/wiki/France_at_the_2020_Summer_Paralympics",
        2024: "https://en.wikipedia.org/wiki/France_at_the_2024_Summer_Paralympics",
    },
    "Allemagne": {
        2012: "https://en.wikipedia.org/wiki/Germany_at_the_2012_Summer_Paralympics",
        2016: "https://en.wikipedia.org/wiki/Germany_at_the_2016_Summer_Paralympics",
        2020: "https://en.wikipedia.org/wiki/Germany_at_the_2020_Summer_Paralympics",
        2024: "https://en.wikipedia.org/wiki/Germany_at_the_2024_Summer_Paralympics",
    },
    "Ukraine": {
        2012: "https://en.wikipedia.org/wiki/Ukraine_at_the_2012_Summer_Paralympics",
        2016: "https://en.wikipedia.org/wiki/Ukraine_at_the_2016_Summer_Paralympics",
        2020: "https://en.wikipedia.org/wiki/Ukraine_at_the_2020_Summer_Paralympics",
        2024: "https://en.wikipedia.org/wiki/Ukraine_at_the_2024_Summer_Paralympics",
    },
    "Japon": {
        2012: "https://en.wikipedia.org/wiki/Japan_at_the_2012_Summer_Paralympics",
        2016: "https://en.wikipedia.org/wiki/Japan_at_the_2016_Summer_Paralympics",
        2020: "https://en.wikipedia.org/wiki/Japan_at_the_2020_Summer_Paralympics",
        2024: "https://en.wikipedia.org/wiki/Japan_at_the_2024_Summer_Paralympics",
    },
    "Royaume-Uni": {
        2012: "https://en.wikipedia.org/wiki/Great_Britain_at_the_2012_Summer_Paralympics",
        2016: "https://en.wikipedia.org/wiki/Great_Britain_at_the_2016_Summer_Paralympics",
        2020: "https://en.wikipedia.org/wiki/Great_Britain_at_the_2020_Summer_Paralympics",
        2024: "https://en.wikipedia.org/wiki/Great_Britain_at_the_2024_Summer_Paralympics",
    },
    "Norvège": {
        2012: "https://en.wikipedia.org/wiki/Norway_at_the_2012_Summer_Paralympics",
        2016: "https://en.wikipedia.org/wiki/Norway_at_the_2016_Summer_Paralympics",
        2020: "https://en.wikipedia.org/wiki/Norway_at_the_2020_Summer_Paralympics",
        2024: "https://en.wikipedia.org/wiki/Norway_at_the_2024_Summer_Paralympics",
    },
    "Turquie": {
        2012: "https://en.wikipedia.org/wiki/Turkey_at_the_2012_Summer_Paralympics",
        2016: "https://en.wikipedia.org/wiki/Turkey_at_the_2016_Summer_Paralympics",
        2020: "https://en.wikipedia.org/wiki/Turkey_at_the_2020_Summer_Paralympics",
        2024: "https://en.wikipedia.org/wiki/Turkey_at_the_2024_Summer_Paralympics",
    },
    "Chine": {
        2012: "https://en.wikipedia.org/wiki/China_at_the_2012_Summer_Paralympics",
        2016: "https://en.wikipedia.org/wiki/China_at_the_2016_Summer_Paralympics",
        2020: "https://en.wikipedia.org/wiki/China_at_the_2020_Summer_Paralympics",
        2024: "https://en.wikipedia.org/wiki/China_at_the_2024_Summer_Paralympics",
    },
    "Etats-Unis": {
        2012: "https://en.wikipedia.org/wiki/United_States_at_the_2012_Summer_Paralympics",
        2016: "https://en.wikipedia.org/wiki/United_States_at_the_2016_Summer_Paralympics",
        2020: "https://en.wikipedia.org/wiki/United_States_at_the_2020_Summer_Paralympics",
        2024: "https://en.wikipedia.org/wiki/United_States_at_the_2024_Summer_Paralympics",
    },
    "Pays-Bas": {
        2012: "https://en.wikipedia.org/wiki/Netherlands_at_the_2012_Summer_Paralympics",
        2016: "https://en.wikipedia.org/wiki/Netherlands_at_the_2016_Summer_Paralympics",
        2020: "https://en.wikipedia.org/wiki/Netherlands_at_the_2020_Summer_Paralympics",
        2024: "https://en.wikipedia.org/wiki/Netherlands_at_the_2024_Summer_Paralympics",
    }
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
        if header:
            header_text = header.text.strip().lower()
            if any(key in header_text for key in ["athlètes", "athletes", "competitors", "competitor"]):

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

df_nb_athletes = pd.DataFrame(index=pays_liste, columns=annees)

for pays in urls:
    for annee, valeur in urls[pays].items():

        print(f"{pays} - {annee} :", end=" ")

        # --- Cas 1 : entier déjà fourni ---
        if isinstance(valeur, int):
            df_nb_athletes.loc[pays, annee] = valeur
            print(f"OK (valeur directe → {valeur})")
            continue
        
        # --- Cas 2 : URL à scraper ---
        elif isinstance(valeur, str) and valeur.startswith("http"):
            try:
                nb = extract_athletes(valeur)
                df_nb_athletes.loc[pays, annee] = nb
                print(f"Scrapé → {nb}")
            except Exception as e:
                df_nb_athletes.loc[pays, annee] = None
                print(f"Erreur scraping : {e}")
            continue
        
        # --- Cas 3 : format inconnu ---
        else:
            df_nb_athletes.loc[pays, annee] = None
            print("Valeur non reconnue")

# ---------------------------------------
# 4) Résultat final
# ---------------------------------------
print("\n===== TABLEAU FINAL =====")
print(df_nb_athletes)

df_nb_athletes.to_csv("nb_athletes_par_pays_par_edition.csv")