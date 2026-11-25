Laborator 05 - Recomandări content-based folosind Cosine Similarity
====================================================================

1. Dataset utilizat:
Fișierul `tesco_sample.json`, care conține produse din catalogul supermarket-urilor Tesco, având un câmp dedicat `description` cu descrieri detaliate în format text și marcaje HTML.

2. Preprocesare și implementare:
- S-au eliminat produsele fără descriere și s-au curățat tag-urile HTML (<p>, <br>, <li> etc.) folosind expresii regulate (`re.sub(r"<[^>]+>", " ", text)`).
- Textul a fost convertit la litere mici (lowercase), iar cifrele și caracterele speciale au fost eliminate.
- S-a aplicat `TfidfVectorizer(stop_words="english")` din `scikit-learn` pentru a transforma descrierile în vectori numerici TF-IDF (rezultând un vocabular de 3691 de cuvinte unice).
- S-a calculat matricea de similaritate folosind `cosine_similarity`.

3. Exemplu de pereche similară identificată:
- Produs 1: Dragon Universal All Purpose Filler 330G
- Produs 2: Dragon Universal All Purpose Filler 1.5 Kilograms
- Scor Cosine Similarity: 0.9950

Justificare:
Această asociere are sens pe deplin: cele două produse reprezintă același tip de chit universal pentru reparații interioare („Dragon Universal All Purpose Filler”), diferența constând doar în gramajul ambalajului (330g vs. 1.5 kg). Datorită descrierilor aproape identice privind proprietățile și modul de utilizare („sands down to a smooth paintable white finish, a handy solution for small home repairs, high adhesion...”), scorul de similaritate cosinus este foarte ridicat (0.9950).

Un alt exemplu relevant observat în matricea de similaritate este perechea formată din „Bondi Sands Aero Self Tanning Foam 225Ml” și „Bondi Sands 1 Hour Express Foam 225Ml” (scor 0.91), ambele fiind spume autobronzante din aceeași gamă de produse cosmetice.