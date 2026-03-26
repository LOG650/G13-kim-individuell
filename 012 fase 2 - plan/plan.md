# FASE 2 – PLANLEGGING

## 0. Sammendrag fra proposal

### Prosjekt

**Emne:** LOG650 – Forskningsprosjekt: Logistikk og kunstig intelligens
**Student:** Kim-Ove Hagerup
**Område:** Etterspørselsprognoser innen kvantitativ logistikk

### Problemstilling

> I hvilken grad kan en maskinlæringsbasert prognosemodell redusere prognosefeil ved estimering av fremtidig lagervolum, sammenlignet med en enkel referansemodell, og dermed bidra til mer presis operativ planlegging?

### Kjerneinnhold

- Én maskinlæringsmodell og én referansemodell utvikles og sammenlignes
- Datagrunnlag: historiske tidsseriedata for lagervolum (ukentlig/månedlig, min. 2–3 år)
- Feilmål: MAE og RMSE som primære evalueringsmetrikker
- Forventet bidrag: dokumentert sammenligning av prognosemodeller og analyse av operativ implikasjon

### Avgrensninger fra proposal

Prosjektet omfatter **ikke** full forsyningskjedeoptimering, nettverksdesign, klimaregnskap eller simulering av hele systemet. Fokuset er metodisk sammenligning av to prognosemodeller.

---

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

Prosjektet er strukturert i seks faser. Nåværende dato er 2026-03-26.

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

### 5.4 WBS (Work Breakdown Structure)

```
LOG650 Forskningsprosjekt
│
├── 1. Prosjektledelse
│   ├── 1.1 Planlegging og oppfølging
│   ├── 1.2 Veiledermøter og kommunikasjon
│   └── 1.3 Versjonskontroll (GitHub)
│
├── 2. Data
│   ├── 2.1 Identifisering og innhenting av datasett
│   ├── 2.2 Utforskende dataanalyse (EDA)
│   ├── 2.3 Databehandling og rensing
│   └── 2.4 Feature engineering
│
├── 3. Modellutvikling
│   ├── 3.1 Referansemodell
│   │   ├── 3.1.1 Implementering
│   │   └── 3.1.2 Prognose på testsett
│   └── 3.2 Maskinlæringsmodell
│       ├── 3.2.1 Implementering
│       ├── 3.2.2 Trening og validering
│       └── 3.2.3 Prognose på testsett
│
├── 4. Evaluering
│   ├── 4.1 Beregning av feilmål (MAE, RMSE, MAPE)
│   ├── 4.2 Visualisering av resultater
│   └── 4.3 Analyse av praktisk relevans
│
└── 5. Rapport
    ├── 5.1 Metodebeskrivelse
    ├── 5.2 Resultatpresentasjon
    ├── 5.3 Diskusjon og bærekraftsperspektiv
    └── 5.4 Korrekturfase og innlevering
```

---

## 6. Ressurser

### 6.1 Personell

| Rolle | Navn | Ansvar |
|-------|------|--------|
| Prosjektansvarlig / Forsker | Kim-Ove Hagerup | All gjennomføring, analyse og rapportering |

Prosjektet gjennomføres som et individuelt arbeid. Kim-Ove Hagerup er ansvarlig for samtlige leveranser.

---

### 6.2 Verktøy og teknologi

| Verktøy | Kategori | Bruksområde |
|---------|----------|-------------|
| Python | Programmeringsspråk | Databehandling, modellutvikling, evaluering |
| Jupyter Notebook | Utviklingsmiljø | Koding, dokumentasjon og presentasjon av resultater |
| VS Code | Editor | Kodeskriving og prosjektstruktur |
| GitHub | Versjonskontroll | Kildekodelagring, historikk og innlevering |
| Claude Code | AI-assistent | Kodegjennomgang, strukturhjelp og dokumentasjon |
| ChatGPT | AI-assistent | Idéutvikling og tekstforbedring |
| MS Project | Prosjektplanlegging | Oversikt over faser, milepæler og tidsplan |

---

## 7. Kommunikasjon

### 7.1 Veilederkontakt

Kommunikasjon med veileder foregår primært via **Microsoft Teams** og **e-post**.

Møter avtales etter behov, men minimum ved følgende milepæler:

- Etter godkjenning av fase 2 (plan)
- Etter fullført databehandling (fase 3)
- Etter ferdig evaluering (fase 5)

---

### 7.2 Møtestruktur

**Før møte:**
- Agenda sendes veileder minimum 24 timer i forveien
- Relevante dokumenter eller kode vedlegges ved behov

**Under møte:**
- Fremdrift gjennomgås mot milepælsplan
- Åpne spørsmål og metodiske avklaringer tas opp

**Etter møte:**
- Kort oppsummering av beslutninger og oppfølgingspunkter skrives og arkiveres (Teams-chat eller e-post)

---

### 7.3 Fremdriftsoppfølging

Prosjektets fremdrift dokumenteres løpende i **GitHub**:

- Commits beskriver hva som er gjort og hvorfor
- Branches brukes ved behov for å skille arbeidsflyt
- Ferdigstilte faser merkes med tydelig commit-melding

---

## 8. Kvalitetssikring

### 8.1 Repliserbar kode

All kode skal produsere identiske resultater ved gjenkjøring:

- Tilfeldige prosesser fikseres med `random_state` / `numpy.random.seed`
- Avhengigheter låses i `requirements.txt` eller `environment.yml`
- Notebook kjøres fra topp til bunn uten feil før innlevering

---

### 8.2 Kronologisk splitt

Tidsseriesplitt gjennomføres alltid kronologisk:

- Treningssett: første ~80 % av observasjonene
- Testsett: siste ~20 % (fremtidige observasjoner)
- Ingen tilfeldig splitt eller k-fold på tidsseriedata
- Skalering og transformasjoner fittes kun på treningssett

---

### 8.3 Modellkontroll

Før resultater rapporteres kontrolleres:

- At modellen ikke har sett testdata under trening
- At feilmål er beregnet på testsett, ikke treningssett
- At begge modeller evalueres under identiske betingelser
- At prognoseresultater visualiseres og ser plausible ut

---

### 8.4 Tekstrevisjon

Rapport og dokumentasjon gjennomgår følgende revisjonssteg:

1. Egenkontroll: konsistens mellom metode, resultater og konklusjon
2. Språklig gjennomgang: klar og presis norsk faglig skriving
3. Referansesjekk: alle påstander er underbygget eller avgrenset

---

### 8.5 Peer-review (egenvurdering)

Siden prosjektet er individuelt, erstattes ekstern peer-review med strukturert egenvurdering:

- Gå gjennom kode og rapport som om man er sensor
- Sjekk at problemstillingen er besvart, ikke bare beskrevet
- Vurder om konklusjonen følger logisk av resultatene

---

## 9. Risikoanalyse

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