import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Încărcarea dataset-ului
df = pd.read_csv("best-selling-manga.csv")

# Combinăm coloanele textuale într-un profil descriptiv pentru fiecare serie manga
df["description"] = (
    df["Manga series"].astype(str) + " " +
    df["Author(s)"].astype(str) + " " +
    df["Publisher"].astype(str) + " " +
    df["Demographic"].astype(str)
)

# 2. Preprocesarea textului (conform tutorialului: lowercase, eliminare caractere speciale/numere)
def preprocess_text(text):
    text = text.lower()
    # Păstrăm doar litere și spații (eliminăm cifrele și semnele de punctuație)
    text = re.sub(r"[^a-z\s]", " ", text)
    # Eliminăm spațiile multiple
    text = re.sub(r"\s+", " ", text).strip()
    return text

df["clean_description"] = df["description"].apply(preprocess_text)

# 3. Vectorizare TF-IDF (eliminăm și stop words din engleză)
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(df["clean_description"])

print(f"Dimensiunea matricei TF-IDF: {tfidf_matrix.shape}")
print(f"Număr cuvinte unice în vocabular: {len(tfidf.vocabulary_)}")

# 4. Calculul matricei de Cosine Similarity
cos_sim_matrix = cosine_similarity(tfidf_matrix)

# Convertim matricea într-un DataFrame etichetat pentru vizualizare ușoară
sim_df = pd.DataFrame(
    cos_sim_matrix,
    index=df["Manga series"],
    columns=df["Manga series"]
)
print("\nPrimele 5x5 elemente din matricea de similaritate:")
print(sim_df.iloc[:5, :5].round(4))

# 5. Identificarea celor mai asemănătoare perechi (ignorând diagonala principală)
cos_sim_no_diag = cos_sim_matrix.copy()
np.fill_diagonal(cos_sim_no_diag, 0)

pairs = []
for i in range(len(df)):
    for j in range(i + 1, len(df)):
        pairs.append((cos_sim_no_diag[i, j], i, j))

pairs.sort(reverse=True, key=lambda x: x[0])

print("\nTop 5 cele mai similare perechi de manga:")
for score, i, j in pairs[:5]:
    m1 = df.loc[i, "Manga series"]
    m2 = df.loc[j, "Manga series"]
    print(f"- {m1} <-> {m2} | Scor Cosine Similarity: {score:.4f}")

# 6. Opțional: Heatmap pentru primele 10 serii din dataset
plt.figure(figsize=(10, 8))
sns.heatmap(sim_df.iloc[:10, :10], annot=True, cmap="YlGnBu", fmt=".2f")
plt.title("Matricea Cosine Similarity (Top 10 Best-Selling Manga)")
plt.tight_layout()
plt.savefig("cosine_similarity_heatmap.png")
plt.show()