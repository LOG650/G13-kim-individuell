# FASE 2 – PLANLEGGING

## 1. Forskningsdesign

Prosjektet gjennomføres som en kvantitativ studie basert på historiske tidsseriedata for lagervolum. Formålet er å undersøke om en maskinlæringsbasert prognosemodell kan redusere prognosefeil sammenlignet med en enkel referansemodell.

Studien har et komparativt design, hvor to modeller testes mot hverandre under like betingelser. Begge modellene trenes på samme historiske datasett og evalueres på identisk testperiode.

Analysen gjennomføres som en tidsserieanalyse der den temporale strukturen i dataene bevares. Observasjonene behandles kronologisk, og fremtidige verdier predikeres utelukkende basert på tidligere informasjon.

Dette designet sikrer:

- Repliserbarhet
- Sammenlignbarhet mellom modeller
- Metodisk transparens
- Unngåelse av datalekkasjer (data leakage)

---

## 2. Evalueringsoppsett

### 2.1 Train/Test-splitt

Datasettet deles i:

- Treningssett (første ca. 80 % av observasjonene)
- Testsett (siste ~20 %)

Splittingen gjøres kronologisk, ikke tilfeldig, for å ivareta tidsserieegenskaper.

Testsettet representerer fremtidige observasjoner som modellen ikke har sett under trening.

---

### 2.2 Prognosestrategi

To evalueringsstrategier vurderes:

1. Statisk prognose:
  Modellen trenes én gang og evalueres på hele testperioden.

2. Rullerende prognose:
  Modellen oppdateres fortløpende etter hvert som nye observasjoner blir tilgjengelige.

Endelig valg dokumenteres og begrunnes før implementering.

---

### 2.3 Feilmål

Prognosepresisjon måles ved hjelp av standard feilmål for tidsserier:

- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- Eventuelt MAPE (Mean Absolute Percentage Error)

MAE gir et direkte mål på gjennomsnittlig avvik i volum.
RMSE straffer store feil sterkere og gir innsikt i modellens stabilitet.
MAPE vurderes dersom volumene ikke inneholder nullverdier.

Primært vil MAE benyttes som hovedmetrisk for sammenligningen, mens RMSE og eventuelt MAPE brukes som supplerende mål.

---

### 2.4 Sammenligningskriterium

Modellene sammenlignes på:

- Gjennomsnittlig prognosefeil
- Stabilitet over tid
- Sensitivitet for sesongvariasjoner
- Praktisk relevans for operativ planlegging

En forbedring anses som relevant dersom den er:

- Statistisk signifikant (der det er mulig å teste)
- Praktisk meningsfull i logistisk kontekst
## 3. Datakrav og struktur

### 3.1 Datatype

Prosjektet forutsetter historiske tidsseriedata for lagervolum registrert med fast intervall (ukentlig eller månedlig).

Observasjonene må være:

- Kronologisk ordnet
- Konsistente over tid
- Uten overlappende perioder
- Registrert med entydig tidsstempel

---

### 3.2 Minimumskrav til datagrunnlag

For å sikre metodisk robusthet stilles følgende minimumskrav:

- Minimum 2–3 års historiske observasjoner
- Tilstrekkelig variasjon i volum
- Helst sesongmønster eller trendkomponent
- Ingen systematiske hull i dataserien

Dersom åpne datasett benyttes, skal kilden dokumenteres og datasettets egenskaper beskrives.

---

### 3.3 Variabelstruktur

Datasettet forventes å inneholde minimum følgende variabler:

| Variabel | Beskrivelse |
|----------|-------------|
| dato     | Tidsstempel (uke/måned) |
| lagervolum | Observasjon av volum |
| sesongindikator (valgfri) | F.eks. måned eller kvartal |
| eksterne faktorer (valgfri) | Kampanjer, hendelser, etc. |

Forklaringsvariabler benyttes kun dersom de kan dokumenteres som realistiske og tilgjengelige i operativ kontekst.

---

### 3.4 Databehandling

Før modelltrening gjennomføres følgende steg:

1. Kontroll av manglende verdier
2. Identifisering av ekstreme observasjoner
3. Eventuell transformasjon (log, differensiering)
4. Feature engineering (sesongvariabler, glidende gjennomsnitt, etc.)

Alle transformasjoner dokumenteres for å sikre repliserbarhet.

---

### 3.5 Simulerte data (ved behov)

Dersom reelle eller åpne datasett ikke benyttes, vil realistiske simulerte tidsserier genereres.

Simulerte data skal:

- Inneholde trend og/eller sesongkomponent
- Inkludere stokastisk variasjon
- Dokumenteres metodisk (hvordan de er generert)

Dette sikrer at metodikken kan testes uten tilgang til bedriftsdata.

---

## 4. Kravspesifikasjon

### 4.1 Funksjonelle krav

Systemet (prognoseløsningen) skal oppfylle følgende funksjonelle krav:

| ID | Krav | Prioritet |
|----|------|-----------|
| F1 | Systemet skal lese og behandle historiske tidsseriedata for lagervolum | Høy |
| F2 | Systemet skal trene en maskinlæringsbasert prognosemodell på historiske data | Høy |
| F3 | Systemet skal trene en enkel referansemodell (f.eks. glidende gjennomsnitt eller naiv sesongmodell) på samme data | Høy |
| F4 | Systemet skal generere prognoser for testperioden med begge modeller | Høy |
| F5 | Systemet skal beregne MAE, RMSE og eventuelt MAPE for begge modeller | Høy |
| F6 | Systemet skal presentere resultater i tabellform og visualisere prognoser mot faktiske verdier | Middels |
| F7 | Systemet skal dokumentere alle databehandlingssteg og modellparametere | Høy |

---

### 4.2 Ikke-funksjonelle krav

| ID | Krav | Begrunnelse |
|----|------|-------------|
| NF1 | Koden skal være reproduserbar – samme input gir samme output | Metodisk validitet og sensorvurdering |
| NF2 | Alle tilfeldige prosesser skal fikseres med seed | Sikrer repliserbarhet |
| NF3 | Tidsseriesplitt skal være kronologisk, ikke tilfeldig | Unngår data leakage |
| NF4 | Koden skal kommenteres slik at tredjeperson kan følge logikken | Transparens |
| NF5 | Datasettets kilde og egenskaper skal dokumenteres | Metodisk sporbarhet |

---

### 4.3 Tekniske krav

Prosjektet gjennomføres i Python med følgende biblioteker:

| Bibliotek | Formål |
|-----------|--------|
| `pandas` | Databehandling og tidsseriestruktur |
| `numpy` | Numeriske operasjoner |
| `scikit-learn` | Maskinlæringsmodell og evalueringsmål |
| `matplotlib` / `seaborn` | Visualisering |
| `statsmodels` (valgfri) | Referansemodell eller diagnostikk |

All kode leveres i Jupyter Notebook (.ipynb) med tilhørende forklarende tekst.

---

### 4.4 Avgrensende krav

Løsningen skal **ikke**:

- Optimere lagernivåer direkte (kun prognose av volum)
- Benytte sanntidsdata eller strømmende data
- Sammenlignes mot mer enn én maskinlæringsmodell og én referansemodell
- Implementeres som et produksjonssystem

---

## 5. Forskningsplan

### 5.1 Faser og milepæler

Prosjektet er strukturert i fem faser. Nåværende dato er 2026-03-26.

| Fase | Aktivitet | Periode | Leveranse |
|------|-----------|---------|-----------|
| 1 | Proposal (fullført) | – | proposal.md |
| 2 | Planlegging (pågående) | Uke 13 | plan.md |
| 3 | Data og forberedelse | Uke 14 | Datasett, notebook med databehandling |
| 4 | Implementering | Uke 15–16 | Modeller, prognoseresultater |
| 5 | Evaluering og analyse | Uke 17 | Sammenligningstabell, visualisering |
| 6 | Rapport og innlevering | Uke 18 | Endelig rapport |

---

### 5.2 Detaljert aktivitetsoversikt

**Fase 3 – Data og forberedelse (Uke 14)**

- Identifisere og laste ned datasett (åpen kilde eller simulere)
- Gjennomføre EDA (utforskende dataanalyse): plotte tidsserie, sjekke for hull og uteliggere
- Gjennomføre train/test-splitt (80/20, kronologisk)
- Feature engineering: sesongvariabler, glidende gjennomsnitt, laggede variabler
- Dokumentere alle steg i notebook

**Fase 4 – Implementering (Uke 15–16)**

- Implementere referansemodell (f.eks. sesongnaiv eller glidende gjennomsnitt)
- Implementere maskinlæringsmodell (f.eks. Random Forest eller Gradient Boosting med tidsserietilpasset feature-matrise)
- Trene begge modeller på treningssett
- Generere prognoser på testsett

**Fase 5 – Evaluering og analyse (Uke 17)**

- Beregne MAE, RMSE og MAPE for begge modeller
- Visualisere faktiske vs. predikerte verdier
- Vurdere praktisk relevans av forbedring i logistisk kontekst
- Gjennomføre enkel statistisk sammenligning dersom mulig

**Fase 6 – Rapport (Uke 18)**

- Skrive endelig rapport med metode, resultater og refleksjon
- Inkludere bærekraftsperspektiv (redusert overbeholdning)
- Rydde og kommentere notebook
- Levere rapport og kode

---

### 5.3 Avhengigheter

```
Fase 3  →  Fase 4  →  Fase 5  →  Fase 6
(data)    (modell)  (evaluering)  (rapport)
```

Fase 4 kan ikke starte uten ferdig databehandling. Fase 5 krever komplette prognoseresultater fra begge modeller.

---

## 6. Risikoanalyse

### 6.1 Risikoidentifikasjon og vurdering

| ID | Risiko | Sannsynlighet | Konsekvens | Risikoscore |
|----|--------|--------------|------------|-------------|
| R1 | Tilgang til reelle bedriftsdata oppnås ikke | Høy | Lav | Middels |
| R2 | Åpent datasett mangler sesong- eller trendstruktur | Middels | Middels | Middels |
| R3 | Maskinlæringsmodellen gir ikke bedre resultater enn referansemodellen | Middels | Middels | Middels |
| R4 | Data leakage ved feil splittemetode | Lav | Høy | Middels |
| R5 | Tidspress mot innlevering | Middels | Høy | Høy |
| R6 | Tekniske problemer med biblioteker eller verktøy | Lav | Middels | Lav |

*Risikoscore = kombinasjon av sannsynlighet og konsekvens, ikke et formelt tall.*

---

### 6.2 Risikorespons

**R1 – Manglende bedriftsdata**
- Tiltak: Prosjektet planlegger fra start for simulerte eller åpne datasett som fallback.
- Ansvarlig: Kim-Ove Hagerup
- Status: Håndtert – alternativ er allerede beskrevet i proposal og seksjon 3.5.

**R2 – Svakt datasett**
- Tiltak: Gjennomføre EDA tidlig i fase 3. Velg datasett med dokumentert sesongstruktur (f.eks. M5-competition, Kaggle Store Sales).
- Beredskap: Generer simulert datasett med kontrollert trend og sesong dersom åpen kilde er utilstrekkelig.

**R3 – ML-modell gir ikke forbedring**
- Tiltak: Dette er et akseptabelt forskningsfunn og dokumenteres som sådant.
- Refleksjon: Negative funn har metodisk verdi og besvarer fortsatt problemstillingen.
- Beredskap: Justere feature engineering eller prøve alternativ modelltype innenfor samme rammeverk.

**R4 – Data leakage**
- Tiltak: Kronologisk splitt implementeres som eksplisitt krav (F3, NF3). Koden gjennomgås for utilsiktet lekkasje (f.eks. skalering på hele datasettet før splitt).
- Kontroll: Sjekkliste for data leakage inkluderes i notebook.

**R5 – Tidspress**
- Tiltak: Fase 3 prioriteres og starter umiddelbart etter godkjent plan. Buffer på én uke er lagt inn før innlevering.
- Beredskap: Scope reduseres til statisk prognose (framfor rullerende) dersom tid er knapp.

**R6 – Tekniske problemer**
- Tiltak: Benytt `requirements.txt` eller `environment.yml` for å fryse avhengigheter.
- Beredskap: Fallback til Google Colab dersom lokal installasjon feiler.

---

### 6.3 Oppsummering av kritiske risikofaktorer

De to høyest prioriterte risikoene er:

1. **Tidspress (R5):** Reduseres ved tidlig oppstart av fase 3 og smalere scope ved behov.
2. **Data leakage (R4):** Reduseres ved eksplisitt kronologisk splitt og kodegjennomgang.

Alle øvrige risikoer er håndterbare innenfor prosjektets rammer.