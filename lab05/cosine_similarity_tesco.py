import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Încărcarea dataset-ului JSON de pe Moodle
# (funcționează atât pentru JSON listă de obiecte, cât și JSON Lines)
try:
    df = pd.read_json("tesco_sample.json")
except ValueError:
    df = pd.read_json("tesco_sample.json", lines=True)

# Ne asigurăm că există coloana 'description' și eliminăm rândurile fără descriere
df = df.dropna(subset=["description"]).reset_index(drop=True)

# Identificăm automat coloana de nume/titlu al produsului (name / title)
name_col = next((c for c in ["name", "title", "product_name"] if c in df.columns), None)
if name_col is None:
    df["product_label"] = [f"Produs_{i+1}" for i in range(len(df))]
    name_col = "product_label"

# 2. Preprocesarea textului (eliminare tag-uri HTML, lowercase, caractere speciale)
def clean_html_and_text(text):
    text = str(text)
    # Eliminarea tag-urilor HTML (<p>, <br>, <li> etc.) conform cerinței din lab
    text = re.sub(r"<[^>]+>", " ", text)
    # Conversie la litere mici
    text = text.lower()
    # Eliminarea numerelor și a caracterelor speciale
    text = re.sub(r"[^a-z\s]", " ", text)
    # Eliminarea spațiilor multiple
    text = re.sub(r"\s+", " ", text).strip()
    return text

df["clean_description"] = df["description"].apply(clean_html_and_text)

# Eliminăm eventualele descrieri rămase goale după curățare
df = df[df["clean_description"] != ""].reset_index(drop=True)

# 3. Vectorizare TF-IDF (eliminare stop words în engleză)
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(df["clean_description"])

print(f"Număr produse procesate: {len(df)}")
print(f"Dimensiunea matricei TF-IDF: {tfidf_matrix.shape}")
print(f"Număr cuvinte unice în vocabular: {len(tfidf.vocabulary_)}")

# 4. Calculul matricei de Cosine Similarity
cos_sim_matrix = cosine_similarity(tfidf_matrix)

sim_df = pd.DataFrame(
    cos_sim_matrix,
    index=df[name_col],
    columns=df[name_col]
)
print("\nPrimele 5x5 elemente din matricea de similaritate:")
print(sim_df.iloc[:5, :5].round(4))

# 5. Găsirea celor mai similare două produse (ignorând diagonala principală și duplicatele exacte 1.0000)
cos_sim_no_diag = cos_sim_matrix.copy()
np.fill_diagonal(cos_sim_no_diag, 0)

pairs = []
for i in range(len(df)):
    for j in range(i + 1, len(df)):
        score = cos_sim_no_diag[i, j]
        # Filtrăm scorurile < 0.999 ca să evităm produse identice duplicate în dataset
        if score < 0.999:
            pairs.append((score, i, j))

pairs.sort(reverse=True, key=lambda x: x[0])

print("\nTop 5 cele mai similare perechi de produse (pentru README.txt):")
for rank, (score, i, j) in enumerate(pairs[:5], start=1):
    p1 = df.loc[i, name_col]
    p2 = df.loc[j, name_col]
    desc1 = df.loc[i, "clean_description"][:100]
    desc2 = df.loc[j, "clean_description"][:100]
    print(f"{rank}. {p1} <-> {p2} | Scor: {score:.4f}")
    print(f"   Desc 1: {desc1}...")
    print(f"   Desc 2: {desc2}...\n")

# 6. Opțional: Heatmap pentru primele 10 produse
plt.figure(figsize=(10, 8))
sns.heatmap(sim_df.iloc[:10, :10], annot=True, cmap="YlGnBu", fmt=".2f")
plt.title("Matricea Cosine Similarity (Primele 10 produse Tesco)")
plt.tight_layout()
plt.savefig("cosine_similarity_tesco_heatmap.png")
plt.show()