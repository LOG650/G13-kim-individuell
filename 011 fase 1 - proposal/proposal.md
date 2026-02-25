# PROSJEKTBESKRIVELSE (PROPOSAL)

## LOG650 – Forskningsprosjekt: Logistikk og kunstig intelligens

### Gruppemedlemmer

- Kim-Ove Hagerup

### Område

Etterspørselsprognoser innen kvantitativ logistikk.

Prosjektet tilhører området Etterspørselsprognoser slik det er definert i kompendiet for emnet. Fokuset er prediksjon av fremtidig lagervolum basert på historiske tidsseriedata, med anvendelse i operativ planlegging.

### Bedrift (valgfritt)

Prosjektet gjennomføres enten i samarbeid med relevant virksomhet (dersom tilgjengelig), eller som et generisk case basert på åpne eller simulerte datasett.

### Problemstilling

I hvilken grad kan en maskinlæringsbasert prognosemodell redusere prognosefeil ved estimering av fremtidig lagervolum, sammenlignet med en enkel referansemodell, og dermed bidra til mer presis operativ planlegging?

Problemstillingen er kvantitativ og innebærer:

- Utvikling av én maskinlæringsmodell for prediksjon av lagervolum
- Utvikling av én enkel referansemodell
- Sammenligning av prognosepresisjon ved bruk av standard feilmål
- Analyse av operativ betydning av forbedret prognosepresisjon

### Data

Prosjektet vil benytte historiske tidsseriedata knyttet til lagervolum.

Datagrunnlaget forventes å bestå av:

- Historiske volumdata per uke eller måned
- Minimum 2–3 års observasjoner for å sikre tilstrekkelig datagrunnlag
- Eventuelle forklaringsvariabler som sesong, kampanjer, kalenderstruktur eller andre relevante påvirkningsfaktorer

Dersom tilgang til reelle bedriftsdata ikke oppnås, vil realistiske simulerte datasett benyttes for å demonstrere metodikken.

### Målfunksjon

Forbedring måles som reduksjon i prognosefeil sammenlignet med referansemodellen.

Prognosepresisjon vil vurderes ved hjelp av standard feilmål for tidsserier, eksempelvis:

- Gjennomsnittlig absolutt feil
- Roten av gjennomsnittlig kvadratisk feil

Målet er å dokumentere om maskinlæringsmodellen gir en statistisk og praktisk relevant forbedring i presisjon.

### Avgrensninger

Prosjektet omfatter:

- Én maskinlæringsmodell
- Én referansemodell
- Én type volum (lagervolum)

Prosjektet omfatter ikke:

- Full optimering av hele forsyningskjeden
- Nettverksdesign
- Komplett bærekraftsanalyse eller klimaregnskap
- Simulering av hele systemet
- Sammenligning av et stort antall avanserte modeller

Fokuset er metodisk sammenligning av prognosemodeller og operativ implikasjon av forbedret presisjon.

### Forventet bidrag

Prosjektet forventes å bidra med:

1. En strukturert implementering av maskinlæringsbasert prognosemodell i logistisk kontekst
2. Dokumentert sammenligning mot tradisjonell referansemodell
3. Analyse av hvordan forbedret prognosepresisjon kan påvirke operativ planlegging
4. Refleksjon rundt potensielle bærekraftseffekter gjennom redusert overbeholdning og svinn
