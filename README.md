# LOG650 G13 — Mannsverk Gård: Besøksprognoser med maskinlæring

Student: **Kim-Ove Hagerup**
Emne: LOG650 — Forskningsprosjekt: Logistikk og kunstig intelligens
Høgskolen i Molde, vår 2026

---

## Innhold

- `rapport_mannsverk_gard.docx` — endelig rapport (Word)
- `rapport_mannsverk_gard.pdf` — samme rapport som PDF
- `rapport_mannsverk_gard.md` — kildeversjon i Markdown
- `simulate_and_model.py` — komplett pipeline: simulering, modellering, evaluering
- `requirements.txt` — Python-avhengigheter
- `figures/` — alle figurer i rapporten
- `data/` — simulert datasett (genereres ved kjøring)
- `results/` — metrikker (genereres ved kjøring)

---

## Reproduksjon av resultater

```bash
# 1. Installer Python 3.10 eller senere
# 2. Installer avhengigheter
pip install -r requirements.txt

# 3. Kjør hele pipelinen
python simulate_and_model.py
```

Med frøverdi 42 (satt i `simulate_and_model.py`) skal samtlige tall og figurer i rapporten reproduseres eksakt.

---

## Hovedfunn

| Modell                       | MAE   | RMSE  |
|------------------------------|-------|-------|
| Sesongnaiv referansemodell   | 93,22 | 96,10 |
| Random Forest                | 66,16 | 70,93 |
| **Forbedring**               | **29,0 %** | **26,2 %** |

Random Forest reduserer både MAE og RMSE med ca. 25–30 % over sesongnaiv referansemodell på testperioden 2. halvår 2025. De viktigste forklaringsvariablene er eventindikatorer og besøk-året-før.

---

## Endelig leveranse 31. mai 2026

- [x] Rapport (DOCX + PDF)
- [x] Python-script for reproduksjon
- [x] Figurer
- [x] Referanseliste (APA 7)
- [ ] Muntlig presentasjon
