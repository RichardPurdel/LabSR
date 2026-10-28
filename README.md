# LabSR - Laborator Sisteme de Recomandare

Acest repository conține implementările pentru laboratoarele de Sisteme de Recomandare folosind platforma și SDK-ul oficial **Recombee** (Python).

---

# Best-Selling Manga Dataset

## 1. Descriere Generală
Acest set de date conține informații despre cele mai bine vândute serii de manga (benzi desenate japoneze) din toate timpurile, cumulând volumele tipărite și vânzările estimate la nivel mondial. Setul oferă o perspectivă clară asupra succesului comercial, longevității și profilului demografic al fiecărei francize.

- **Sursă Kaggle:** [Best-Selling Manga Dataset](https://www.kaggle.com/datasets/drahulsingh/best-selling-manga)
- **Format fișier:** CSV (`best-selling-manga.csv`)
- **Număr de intrări:** 187 de produse (serii manga)
- **Domeniu:** Recomandare de conținut media / Entertainment / Literatură grafică

---

## 2. Structura Datelor și Maparea Proprietăților (Laborator 2)

Tabelul conține atributele preluate din fișierul CSV și mapate în catalogul Recombee prin scriptul `recombee_properties.py`:

| Coloană CSV | Tip Original | Proprietate Recombee | Tip Recombee | Descriere |
| :--- | :--- | :--- | :--- | :--- |
| **Manga series** | String / Text | `title` | `string` | Numele oficial al seriei manga (ex. *One Piece*, *Naruto*). |
| **Author(s)** | String / Text | `author` | `string` | Numele autorului / ilustratorului (mangaka). |
| **Publisher** | String / Text | `publisher` | `string` | Editura responsabilă de publicare (ex. *Shueisha*, *Kodansha*). |
| **Demographic** | String / Categorie | `demographic` | `string` | Categoria de public țintă (ex. *Shōnen*, *Seinen*, *Shōjo*). |
| **No. of collected volumes** | Int / Text numeric | `volumes` | `int` | Numărul total de volume publicate. |
| **Approximate sales in million(s)** | Float / Double | `sales_in_millions` | `double` | Copii vândute estimate, exprimate în milioane de unități. |

---

## 3. Relevanță pentru Sistemul de Recomandare

Dataset-ul este optimizat pentru recomandări de tip **Content-Based Filtering** și algoritmi hibrizi în **Recombee**:

- **Profilare demografică (`demographic`):** Permite recomandarea de titluri similare bazate pe publicul țintă al cititorului (ex. cititorii pasionați de *Shōnen* vor primi recomandări similare din aceeași sferă).
- **Filtrare după autor și editură (`author`, `publisher`):** Recomandă alte serii realizate de același mangaka sau publicate sub amprenta aceleiași case editoriale.
- **Popularitate și Scală (`sales_in_millions`, `volumes`):** Permite sortarea după succesul comercial global sau recomandarea în funcție de nivelul de angajament al cititorului (serii scurte/rapide vs. serii monumentale de peste 50 de volume).

---

## 4. Trimiterea Item-urilor în Recombee (Laborator 3)

Popularea efectivă a bazei de date Recombee cu item-urile din CSV este realizată prin scriptul `recombee_items.py`.

### Detalii de implementare și optimizări:
1. **Identificator unic (`itemId`):** Pentru fiecare înregistrare s-a generat un ID de tipul `manga_{index + 1}` (de la `manga_1` la `manga_187`). Această abordare evită erorile cauzate de caracterele speciale din titlurile seriilor (ex. `/`, `×`, semne de punctuație) care nu sunt permise în căile URL ale API-ului REST.
2. **Curățare și validare de tipuri:** Valorile numerice (`volumes` și `sales_in_millions`) sunt procesate cu `pd.to_numeric(..., errors='coerce')` pentru a garanta tipuri de date curate (`int`, `float`) fără erori cauzate de valori nule sau adnotări textuale.
3. **Optimizare prin Batch:** Trimiterea datelor nu se face prin request-uri HTTP individuale, ci este optimizată prin cereri de tip `Batch` (loturi de câte 100 de cereri `SetItemValues` cu parametrul `cascade_create=True`), respectând cerințele de performanță.

### Rezultat încărcare:
Toate cele **187 de serii manga** au fost încărcate cu succes în platforma Recombee și sunt vizibile în **Recombee Admin UI** -> secțiunea **Items**, având toate cele 6 proprietăți completate corect.

---

## 5. Instrucțiuni de Rulare

### Cerințe preliminare
Instalați pachetele necesare:
```bash
pip install pandas recombee-api-client