import pandas as pd
import requests
from io import StringIO
import re

#Parsing du tableau du nombre d'athletes depuis Wikipédia pour les Jeux 2O12, 2016 et 2020
def get_number_athletes(year, url):

    headers = {"User-Agent": "Mozilla/5.0"}
    html = requests.get(url, headers=headers).text
    html = re.sub(r'(colspan|rowspan)="(\d+);"', r'\1="\2"', html)

    tables = pd.read_html(StringIO(html))
    #Sélection du tableau le plus grand de la page de sorte qu'il ne prenne pas l'infobox
    good = None
    for t in tables:
        if len(t) >= 100:
            good = t.copy()
            break

    if good is None:
        raise ValueError(f"Aucun bon tableau trouvé pour {year}")

    df = good

    #Renommer les colonnes en français
    rename = {}
    for col in df.columns:
        lc = str(col).lower()
        if "npc" in lc or "noc" in lc or "team" in lc or "0" in lc or "country" in lc :  #en 2020, les colonnes sont appelées 0 et 1
            rename[col] = "pays"
        if "athletes" in lc or "1" in lc:
            rename[col] = "athletes_paralympiques"

    df = df.rename(columns=rename)
    df = df[["pays", "athletes_paralympiques"]]
    df["annee"] = year
    return df

#La mise en page pour les Jeux de 2024 est un peu différente donc la fonction aussi 
def get_number_athletes_2024(year, url):

    headers = {"User-Agent": "Mozilla/5.0"}
    html = requests.get(url, headers=headers).text
    html = re.sub(r'(colspan|rowspan)="(\d+);"', r'\1="\2"', html)

    tables = pd.read_html(StringIO(html))
    #sélection du tableau de sorte à ce qu'il ne prenne pas l'infobox
    good = None
    for t in tables:
        print(t, t.columns)
        if len(t) == 1 and t.columns[0] != "Venue": #sinon, Python prend le tableau des équipements sportifs
            good = t.copy()

    if good is None:
        raise ValueError(f"Aucun bon tableau trouvé pour {year}")

    df = good



urls1 = {
    2012: "https://en.wikipedia.org/wiki/2012_Summer_Paralympics",
    2016: "https://en.wikipedia.org/wiki/2016_Summer_Paralympics",
    2020: "https://en.wikipedia.org/wiki/2020_Summer_Paralympics",}
    
urls2 = {2024: "https://en.wikipedia.org/wiki/2024_Summer_Paralympics",} #la page wikipedia 2024 a une mise en page différente

df_para = pd.concat([get_number_athletes(y, u) for y, u in urls1.items()]+[get_number_athletes(y, u) for y, u in urls2.items()],
                   ignore_index=True)


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
    "Refugee Paralympic Team": "Équipe paralympique des réfugiés",
    "Paralympic Refugee Team": "Équipe paralympique des réfugiés",
    "Independent Athletes": "Athlètes indépendants",
    "Independent Paralympic Athletes": "Athlètes paralympiques indépendants",
    "Individual Neutral Athletes": "Athlètes paralympiques indépendants",
    "Neutral Paralympic Athletes": "Athlètes paralympiques indépendants",
    "Individual Neutral Athletes[A][B]": "Athlètes paralympiques indépendants",
    "Individual Neutral Athletes[C]": "Athlètes paralympiques indépendants",
    "Individual Neutral Athletes[D]": "Athlètes paralympiques indépendants",
    "Authorised Neutral Athletes": "Athlètes neutres autorisés",
    "Paralympic Athletes from Russia": "Russie",
    "Individual Paralympic Athletes": "Athlètes paralympiques indépendants",
    "RPC": "Russie",
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
    "Japan host": "Japon",
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
    "Somalia": "Somalie",
    "Macau" : "Macao",
    "Faroe Islands": "Îles Féroé",
}

#Traduction + Suppression de certains caractères apparus après le parsing
df_para["pays"] = (
    df_para["pays"].str.replace(r"[^A-Za-z ,\-']", "", regex=True).str.strip()
)
df_para["pays"] = df_para["pays"].map(countries_en_fr_cio)

#Ajout manuel des athlètes russes et biélorusses (tous deux ont concouru sous bannière neutre)
df_para.loc[len(df_para)] = ['Russie', 88, '2024']
df_para.loc[len(df_para)] = ['Biélorussie', 8, '2024']

df_para.to_pickle("df_athletes_paralympiques.pkl")