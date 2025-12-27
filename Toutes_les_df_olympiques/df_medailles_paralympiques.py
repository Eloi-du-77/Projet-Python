import pandas as pd
import requests
from io import StringIO

#Parsing de Wikipédia pour les médailles paralympiques
def get_paralympic_medal_table(year, url):

    headers = {"User-Agent": "Mozilla/5.0"}
    html = requests.get(url, headers=headers).text
    tables = pd.read_html(StringIO(html))

    #sélection du tableau des médailles
    #il doit contenir Gold/Silver/Bronze et plus de 10 pays (pour ne pas prendre le mauvais tableau)
    good = None
    for t in tables:
        cols = [c.lower() for c in t.columns.astype(str)]
        if any("gold" in c for c in cols) and len(t) >= 10:
            good = t.copy()
            break

    if good is None:
        raise ValueError(f"Aucun tableau paralympique trouvé pour {year}")

    df = good

    #renommage des colonnes
    rename = {}
    for col in df.columns:
        lc = str(col).lower()
        if "nation" in lc or "npc" in lc or "team" in lc or "country" in lc:
             rename[col] = "pays"
        elif "gold" in lc:
            rename[col] = "or_paralympique"
        elif "silver" in lc:
            rename[col] = "argent_paralympique"
        elif "bronze" in lc:
            rename[col] = "bronze_paralympique"
        elif "total" in lc:
            rename[col] = "total_medailles_paralympiques"

    df = df.rename(columns=rename)
    df = df[["pays", "or_paralympique", "argent_paralympique", "bronze_paralympique", "total_medailles_paralympiques"]]
    df["annee"] = year
    return df


#url du tableau des médailles paralympique
para_urls = {
    2012: "https://en.wikipedia.org/wiki/2012_Summer_Paralympics_medal_table",
    2016: "https://en.wikipedia.org/wiki/2016_Summer_Paralympics_medal_table",
    2020: "https://en.wikipedia.org/wiki/2020_Summer_Paralympics_medal_table",
    2024: "https://en.wikipedia.org/wiki/2024_Summer_Paralympics_medal_table",
}

df_para = pd.concat(
    [get_paralympic_medal_table(y, u) for y, u in para_urls.items()],
    ignore_index=True
)

#Traduction des pays en français (aide de Claude AI pour le dictionnaire)
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
    "Refugee Paralympic Team": "Équipe olympique des réfugiés",
    "Paralympic Refugee Team": "Équipe olympique des réfugiés",
    "Independent Athletes": "Athlètes indépendants",
    "Independent Paralympic Athletes": "Athlètes olympiques indépendants",
    "Individual Neutral Athletes[A][B]": "Athlètes olympiques indépendants",
    "Individual Neutral Athletes[C]": "Athlètes olympiques indépendants",
    "Individual Neutral Athletes[D]": "Athlètes olympiques indépendants",
    "Authorised Neutral Athletes": "Athlètes neutres autorisés",
    "Neutral Paralympic Athletes": "Athlètes neutres autorisés",
    "Paralympic Athletes from Russia": "Russie",
    "RPC": "Russie",

    #En 2012, les pays sont suivis de leur code en 3 lettres, on l'enlève

    "ChinaCHN": "Chine",
    "RussiaRUS": "Russie",
    "Great BritainGBR": "Royaume-Uni",
    "UkraineUKR": "Ukraine",
    "AustraliaAUS": "Australie",
    "United StatesUSA": "États-Unis",
    "BrazilBRA": "Brésil",
    "GermanyGER": "Allemagne",
    "PolandPOL": "Pologne",
    "NetherlandsNED": "Pays-Bas",
    "IranIRI": "Iran",
    "South KoreaKOR": "Corée du Sud",
    "ItalyITA": "Italie",
    "TunisiaTUN": "Tunisie",
    "CubaCUB": "Cuba",
    "FranceFRA": "France",
    "SpainESP": "Espagne",
    "South AfricaRSA": "Afrique du Sud",
    "IrelandIRL": "Irlande",
    "CanadaCAN": "Canada",
    "New ZealandNZL": "Nouvelle-Zélande",
    "NigeriaNGR": "Nigéria",
    "MexicoMEX": "Mexique",
    "JapanJPN": "Japon",
    "BelarusBLR": "Biélorussie",
    "AlgeriaALG": "Algérie",
    "AzerbaijanAZE": "Azerbaïdjan",
    "EgyptEGY": "Égypte",
    "SwedenSWE": "Suède",
    "AustriaAUT": "Autriche",
    "ThailandTHA": "Thaïlande",
    "FinlandFIN": "Finlande",
    "SwitzerlandSUI": "Suisse",
    "Hong KongHKG": "Hong Kong",
    "NorwayNOR": "Norvège",
    "BelgiumBEL": "Belgique",
    "MoroccoMAR": "Maroc",
    "HungaryHUN": "Hongrie",
    "SerbiaSRB": "Serbie",
    "KenyaKEN": "Kenya",
    "SlovakiaSVK": "Slovaquie",
    "Czech RepublicCZE": "République tchèque",
    "TurkeyTUR": "Turquie",
    "GreeceGRE": "Grèce",
    "IsraelISR": "Israël",
    "United Arab EmiratesUAE": "Émirats arabes unis",
    "LatviaLAT": "Lettonie",
    "NamibiaNAM": "Namibie",
    "RomaniaROU": "Roumanie",
    "DenmarkDEN": "Danemark",
    "AngolaANG": "Angola",
    "Bosnia and HerzegovinaBIH": "Bosnie-Herzégovine",
    "ChileCHI": "Chili",
    "FijiFIJ": "Fidji",
    "IcelandISL": "Islande",
    "JamaicaJAM": "Jamaïque",
    "MacedoniaMKD": "Macédoine du Nord",
    "CroatiaCRO": "Croatie",
    "BulgariaBUL": "Bulgarie",
    "IraqIRQ": "Irak",
    "ColombiaCOL": "Colombie",
    "ArgentinaARG": "Argentine",
    "Chinese TaipeiTPE": "Taïwan",
    "PortugalPOR": "Portugal",
    "MalaysiaMAS": "Malaisie",
    "SingaporeSIN": "Singapour",
    "CyprusCYP": "Chypre",
    "EthiopiaETH": "Éthiopie",
    "IndiaIND": "Inde",
    "Saudi ArabiaKSA": "Arabie saoudite",
    "SloveniaSLO": "Slovénie",
    "UzbekistanUZB": "Ouzbékistan",
    "VenezuelaVEN": "Venezuela",
    "IndonesiaINA": "Indonésie",
    "Sri LankaSRI": "Sri Lanka"
}

#Traduction et suppression de caractères ajoutés par la conversion sur Python
df_para["pays"] = (
    df_para["pays"].str.replace(r"[^A-Za-z ,\-']", "", regex=True).str.strip()
)
df_para["pays"] = df_para["pays"].map(countries_en_fr_cio)

#Ajout manuel des athlètes russes et biélorusse (tous deux ont concouru sous banière neutre)
df_para.loc[len(df_para)] = ['Russie', 20, 21, 23, 64, '2024']
df_para.loc[len(df_para)] = ['Biélorussie', 6, 1, 0, 7, '2024']


if __name__ == '__main__':
    df_para.to_pickle("df_medailles_paralympiques.pkl")
