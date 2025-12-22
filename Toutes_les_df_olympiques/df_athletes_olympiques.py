import pandas as pd
import requests
from io import StringIO

#Parsing du tableau avec le nombre d'athlètes par pays sur Wikipédia
def get_medal_table(year, url):

    headers = {"User-Agent": "Mozilla/5.0"}
    html = requests.get(url, headers=headers).text

    tables = pd.read_html(StringIO(html))

    #sélectionner le tableau avec le nombre d'athletes par pays (c'est le seul tableau de la page avec plus de 100 lignes)
    good = None
    for t in tables:
        if len(t) >= 100:
            good = t.copy()
            break

    if good is None:
        raise ValueError(f"Aucun bon tableau trouvé pour {year}")

    df = good

    #Renommer les colonnes
    rename = {}
    for col in df.columns:
        lc = str(col).lower()
        if "nation" in lc or "noc" in lc or "team" in lc or "country" in lc:
            rename[col] = "pays"
        elif "athletes" in lc:
            rename[col] = "athletes_olympiques"
    df = df.rename(columns=rename)
    df = df[["pays", "athletes_olympiques"]]
    df["annee"] = year
    return df


urls = {
    2012: "https://en.wikipedia.org/wiki/2012_Summer_Olympics",
    2016: "https://en.wikipedia.org/wiki/2016_Summer_Olympics",
    2020: "https://en.wikipedia.org/wiki/2020_Summer_Olympics",
    2024: "https://en.wikipedia.org/wiki/2024_Summer_Olympics",
}

df_athletes = pd.concat([get_medal_table(y, u) for y, u in urls.items()],
                   ignore_index=True)

#Enlever les nations absentes

df_athletes = df_athletes[df_athletes["athletes_olympiques"] > 0]

#Traduire les noms de pays

countries_en_fr_cio = {
    # --- Nations & territoires CIO ---
    "Afghanistan": "Afghanistan",
    "Albania": "Albanie",
    "Algeria": "Algérie",
    "American Samoa": "Samoa américaines",
    "Andorra": "Andorre",
    "Angola": "Angola",
    "Antigua and Barbuda": "Antigua-et-Barbuda",
    "Argentina": "Argentine",
    "Armenia": "Arménie",
    "Aruba": "Aruba",
    "Australia": "Australie",
    "Austria": "Autriche",
    "Azerbaijan": "Azerbaïdjan",
    "Bahamas": "Bahamas",
    "Bahrain": "Bahreïn",
    "Bangladesh": "Bangladesh",
    "Barbados": "Barbade",
    "Belarus": "Biélorussie",
    "Belgium": "Belgique",
    "Belize": "Belize",
    "Benin": "Bénin",
    "Bermuda": "Bermudes",
    "Bhutan": "Bhoutan",
    "Bolivia": "Bolivie",
    "Bosnia and Herzegovina": "Bosnie-Herzégovine",
    "Botswana": "Botswana",
    "Brazil": "Brésil",
    "British Virgin Islands": "Îles Vierges britanniques",
    "Brunei": "Brunei",
    "Bulgaria": "Bulgarie",
    "Burkina Faso": "Burkina Faso",
    "Burundi": "Burundi",
    "Cambodia": "Cambodge",
    "Cameroon": "Cameroun",
    "Canada": "Canada",
    "Cape Verde": "Cap-Vert",
    "Cayman Islands": "Îles Caïmans",
    "Central African Republic": "République centrafricaine",
    "Chad": "Tchad",
    "Chile": "Chili",
    "China": "Chine",
    "Chinese Taipei": "Taïwan",
    "Colombia": "Colombie",
    "Comoros": "Comores",
    "Congo": "Congo",
    "Cook Islands": "Îles Cook",
    "Costa Rica": "Costa Rica",
    "Croatia": "Croatie",
    "Cuba": "Cuba",
    "Cyprus": "Chypre",
    "Czech Republic": "République tchèque",
    "Denmark": "Danemark",
    "Djibouti": "Djibouti",
    "Dominica": "Dominique",
    "Dominican Republic": "République dominicaine",
    "Ecuador": "Équateur",
    "Egypt": "Égypte",
    "El Salvador": "Salvador",
    "Equatorial Guinea": "Guinée équatoriale",
    "Eritrea": "Érythrée",
    "Estonia": "Estonie",
    "Eswatini": "Eswatini",
    "Ethiopia": "Éthiopie",
    "Fiji": "Fidji",
    "Finland": "Finlande",
    "France": "France",
    "Gabon": "Gabon",
    "Gambia": "Gambie",
    "Georgia": "Géorgie",
    "Germany": "Allemagne",
    "Ghana": "Ghana",
    "Great Britain": "Royaume-Uni",
    "Greece": "Grèce",
    "Grenada": "Grenade",
    "Guam": "Guam",
    "Guatemala": "Guatemala",
    "Guinea": "Guinée",
    "Guinea-Bissau": "Guinée-Bissau",
    "Guyana": "Guyana",
    "Haiti": "Haïti",
    "Honduras": "Honduras",
    "Hong Kong, China": "Hong Kong",
    "Hungary": "Hongrie",
    "Iceland": "Islande",
    "India": "Inde",
    "Indonesia": "Indonésie",
    "Iran": "Iran",
    "Iraq": "Irak",
    "Ireland": "Irlande",
    "Israel": "Israël",
    "Italy": "Italie",
    "Ivory Coast": "Côte d’Ivoire",
    "Jamaica": "Jamaïque",
    "Japan": "Japon",
    "Jordan": "Jordanie",
    "Kazakhstan": "Kazakhstan",
    "Kenya": "Kenya",
    "Kiribati": "Kiribati",
    "Kosovo": "Kosovo",
    "Kuwait": "Koweït",
    "Kyrgyzstan": "Kirghizistan",
    "Laos": "Laos",
    "Latvia": "Lettonie",
    "Lebanon": "Liban",
    "Lesotho": "Lesotho",
    "Liberia": "Libéria",
    "Libya": "Libye",
    "Liechtenstein": "Liechtenstein",
    "Lithuania": "Lituanie",
    "Luxembourg": "Luxembourg",
    "Madagascar": "Madagascar",
    "Malawi": "Malawi",
    "Malaysia": "Malaisie",
    "Maldives": "Maldives",
    "Mali": "Mali",
    "Malta": "Malte",
    "Marshall Islands": "Îles Marshall",
    "Mauritania": "Mauritanie",
    "Mauritius": "Maurice",
    "Mexico": "Mexique",
    "Micronesia": "Micronésie",
    "Moldova": "Moldavie",
    "Monaco": "Monaco",
    "Mongolia": "Mongolie",
    "Montenegro": "Monténégro",
    "Morocco": "Maroc",
    "Mozambique": "Mozambique",
    "Myanmar": "Myanmar",
    "Namibia": "Namibie",
    "Nauru": "Nauru",
    "Nepal": "Népal",
    "Netherlands": "Pays-Bas",
    "New Zealand": "Nouvelle-Zélande",
    "Nicaragua": "Nicaragua",
    "Niger": "Niger",
    "Nigeria": "Nigéria",
    "North Korea": "Corée du Nord",
    "North Macedonia": "Macédoine du Nord",
    "Norway": "Norvège",
    "Oman": "Oman",
    "Pakistan": "Pakistan",
    "Palau": "Palaos",
    "Palestine": "Palestine",
    "Panama": "Panama",
    "Papua New Guinea": "Papouasie-Nouvelle-Guinée",
    "Paraguay": "Paraguay",
    "Peru": "Pérou",
    "Philippines": "Philippines",
    "Poland": "Pologne",
    "Portugal": "Portugal",
    "Puerto Rico": "Porto Rico",
    "Qatar": "Qatar",
    "Romania": "Roumanie",
    "Russia": "Russie",
    "Rwanda": "Rwanda",
    "Saudi Arabia": "Arabie saoudite",
    "Senegal": "Sénégal",
    "Serbia": "Serbie",
    "Singapore": "Singapour",
    "Slovakia": "Slovaquie",
    "Slovenia": "Slovénie",
    "South Africa": "Afrique du Sud",
    "South Korea": "Corée du Sud",
    "South Sudan": "Soudan du Sud",
    "Spain": "Espagne",
    "Sri Lanka": "Sri Lanka",
    "Sudan": "Soudan",
    "Sweden": "Suède",
    "Switzerland": "Suisse",
    "Thailand": "Thaïlande",
    "Tunisia": "Tunisie",
    "Turkey": "Turquie",
    "Ukraine": "Ukraine",
    "United States": "États-Unis",
    "Uruguay": "Uruguay",
    "Uzbekistan" : "Ouzbékistan",
    "Vietnam": "Viêt Nam",
    "Zambia": "Zambie",
    "Zimbabwe": "Zimbabwe",
    "Uganda": "Ouganda",
    "Tajikistan": "Tadjikistan",
    "Saint Lucia": "Sainte-Lucie",
    "Hong Kong": "Hong Kong",
    "Venezuela": "Venezuela",
    "Turkmenistan": "Turkménistan",
    "Syria": "Syrie",
    "San Marino": "Saint-Marin",
    "United Arab Emirates": "Émirats arabes unis",
    "Trinidad and Tobago": "Trinité-et-Tobago",

    # --- Réfugiés / indépendants / neutres ---
    "Refugee Olympic Team": "Équipe olympique des réfugiés",
    "Olympic Refugee Team": "Équipe olympique des réfugiés",
    "Independent Athletes": "Athlètes indépendants",
    "Independent Olympic Athletes": "Athlètes olympiques indépendants",
    "Individual Neutral Athletes": "Athlètes olympiques indépendants",
    "Individual Neutral Athletes[A][B]": "Athlètes olympiques indépendants",
    "Individual Neutral Athletes[C]": "Athlètes olympiques indépendants",
    "Individual Neutral Athletes[D]": "Athlètes olympiques indépendants",
    "Authorised Neutral Athletes": "Athlètes neutres autorisés",
    "Olympic Athletes from Russia": "Russie",
    "ROC": "Russie",

    #Equipes ayant des défauts de traitement / ignorées par chatGPT

    "Macedonia": "Macédoine du Nord",
    "Swaziland": "Eswatini",
    "The Gambia": "Gambie",
    "The Gambie": "Gambie",  
    "Virgin Islands": "Îles Vierges américaines",
    "Federated States of Micronesia": "Micronésie",
    "Republic of the Congo": "Congo",
    "So Tom and Prncipe": "São Tomé-et-Príncipe",
    "Japan Host": "Japon",
    "Samoa": "Samoa",
    "Tanzania": "Tanzanie",
    "Democratic Republic of the Congo": "République démocratique du Congo",
    "Vanuatu": "Vanuatu",
    "Suriname": "Suriname",
    "Togo": "Togo",
    "Timor-Leste": "Timor oriental",
    "Saint Vincent and the Grenadines": "Saint-Vincent-et-les-Grenadines",
    "Sierra Leone": "Sierra Leone",
    "Tonga": "Tonga",
    "Yemen": "Yémen",
    "Saint Kitts and Nevis": "Saint-Christophe-et-Niévès",
    "Seychelles": "Seychelles",
    "Solomon Islands": "Îles Salomon",
    "Tuvalu": "Tuvalu",
    "Somalia": "Somalie"
}

#Traduction + Suppression de certains caractères apparus après le parsing
df_athletes["pays"] = (
    df_athletes["pays"].str.replace(r"[^A-Za-z ,\-']", "", regex=True).str.strip()
)
df_athletes["pays"] = df_athletes["pays"].map(countries_en_fr_cio)

#Ajout manuel des athlètes russes et biélorusses (tous deux ont concouru sous bannière neutre)
df_athletes.loc[len(df_athletes)] = ['Russie', 15, '2024']
df_athletes.loc[len(df_athletes)] = ['Biélorussie', 17, '2024']

df_athletes.to_pickle("df_athletes_olympiques.pkl")