# Opciós alapstratégiák gyakorlása – Streamlit app

Ez az oktatási célú Streamlit app a négy alap opciós pozíció gyakorlására készült:

- long call
- short call
- long put
- short put

## Futtatás helyben

1. Telepítés:

```bash
pip install -r requirements.txt
```

2. App indítása:

```bash
streamlit run app.py
```

## Funkciók

- Interaktív payoff/profit grafikon
- Kötési ár, prémium és lejáratkori árfolyam állítása
- Automatikusan generált gyakorlófeladatok
- Azonnali ellenőrzés és visszajelzés
- Pontszám követése munkameneten belül
- Rövid összefoglaló táblázat a négy alapstratégiáról

## Oktatási továbbfejlesztési ötletek

- Moodle / Teams linkként megosztás
- Hallgatói azonosító bekérése
- Pontszám CSV-be mentése
- Több nehézségi szint
- Összetett stratégiák: covered call, protective put, straddle, strangle, bull/bear spread
