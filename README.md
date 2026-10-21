# LabSR
Laborator Sisteme de Recomandare

# Best-Selling Manga Dataset

## 1. Descriere Generală
Acest set de date conține informații despre cele mai bine vândute serii de manga (benzi desenate japoneze) din toate timpurile, cumulând volumele tipărite și vânzările estimate la nivel mondial. Setul oferă o perspectivă clară asupra succesului comercial, longevității și profilului demografic al fiecărei francize.

* **Sursă Kaggle:** [Best-Selling Manga Dataset](https://www.kaggle.com/datasets/drahulsingh/best-selling-manga)
* **Format fișier:** CSV (`best-selling-manga.csv`)
* **Domeniu:** Recomandare de conținut media / Entertainment / Literatură grafică

---

## 2. Structura Datelor și Atribute

Tabelul conține detalii esențiale despre fiecare serie, mapate după cum urmează:

| Coloană CSV | Tip de Date Original | Corespondență Recombee | Tip Recombee | Descriere |
| :--- | :--- | :--- | :--- | :--- |
| **Manga series** | String / Text | `title` | `string` | Numele oficial al seriei manga (ex. *One Piece*, *Naruto*). |
| **Author(s)** | String / Text | `author` | `string` | Numele autorului / ilustratorului (mangaka). |
| **Publisher** | String / Text | `publisher` | `string` | Editura responsabilă de publicare (ex. *Shueisha*, *Kodansha*). |
| **Demographic** | String / Categorie | `demographic` | `string` | Categoria de public țintă (ex. *Shōnen*, *Seinen*, *Shōjo*, *Josei*). |
| **No. of collected volumes** | Int / Text numeric | `volumes` | `int` | Numărul total de volume (tankōbon) publicate. |
| **Approximate sales in million(s)** | Float / Double | `sales_in_millions` | `double` | Numărul estimat de copii vândute, exprimat în milioane de unități. |
| **Serialized** | String (Interval ani) | — | — | Perioada în care seria a fost serializată (ex. *1997–present*). |

---

## 3. Relevanță pentru Sistemul de Recomandare

Dataset-ul este optimizat pentru recomandări de tip **Content-Based Filtering** și filtrare hibridă în **Recombee**:

* **Profilare demografică (`demographic`):** Permite recomandarea de titluri similare bazate pe preferințele de gen sau vârstă ale cititorului (ex. cititorii pasionați de *Shōnen* vor primi recomandări similare din aceeași sferă tematică).
* **Filtrare după autor și editură (`author`, `publisher`):** Recomandă alte serii realizate de același autor sau publicate sub amprenta aceleiași case editoriale.
* **Popularitate și Scală (`sales_in_millions`, `volumes`):** Valorile numerice permit sortarea după popularitate globală sau recomandarea seriilor în funcție de angajamentul cititorului (serii scurte/ușor de parcurs vs. serii monumentale de peste 50 de volume).

---

## 4. Preprocesare și Curățare (Data Cleaning)

Înainte de popularea bazei de date Recombee, datele brute necesită câteva ajustări:
1. **Curățare numerică pentru `volumes`:** Eliminarea adnotărilor textuale (de exemplu mențiunile de tip *ongoing* sau parantezele) pentru a asigura conversia fără erori la tipul `int`.
2. **Conversia vânzărilor:** Asigurarea conversiei câmpului `Approximate sales in million(s)` într-o valoare numerică continuă (`float`/`double`).
3. **Tratarea valorilor nule:** Completarea valorilor lipsă din câmpurile opționale (ex. demografice nespecificate completate cu `"Unknown"`).

---

## 5. Instrucțiuni de Utilizare

1. Descărcați fișierul `best-selling-manga.csv` de pe Kaggle.
2. Plasați fișierul în rădăcina proiectului, alături de scripturile de configurare.
3. Rulați scriptul de definire a proprietăților:
   ```bash
   python setup_schema.py
