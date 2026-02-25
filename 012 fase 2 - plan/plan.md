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

- Treningssett (første ~80 % av observasjonene)
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