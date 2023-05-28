# Dronebasert sanking av sau

Dette prosjektet er utviklet i forbindelse med en masteroppgave om dronebasert sanking av sau, skrevet av Royce Lu og Moira Charlotte Reinholdt Belsvik.

## Implementerte metoder

I forbindelse med masteroppgaven er det implementert totalt fem ulike metoder for å simulere sauesanking med droner. De tre førstnevnte er gjenskapninger av metoder fra den eksisterende litteraturen. Basert på en vurdering av resultatene har vi utviklet to varianter av vår egen metode, i et forsøk på å lage en metode som er mer pålitelig og effektiv.

1. Sirkelformasjonsmetoden (Kubo et al., 2021)
1. V-formasjonsmetoden (Fujioka et al., 2022)
1. Polygonformasjonsmetoden (Li et al., 2022)
1. Massesentermetoden
1. V-polygonmetoden

## Hvordan kjøre simuleringene og testene

### Simuleringer

For å kjøre simuleringene av metodene, med variasjon på sauenes synsrekkevidde, kjør i terminalen: `python3 sim.py`. Resultatene havner i mappa `./sim_results`, og ligger i en mappe med dato/tid for når testen ble kjørt.

For å kjøre simuleringer av våre egne metoder, med variasjon på vinkelen mellom dronene i en v-formasjon, kjør i terminalen: `python3 our_sim.py`. Resultatene havner i mappa `./our_sim_results`, og ligger i en mappe med dato/tid for når testen ble kjørt.

### Diagrammer

Alle resultatene vises som CSV-filer. Om man ønsker å visualisere dataene i diagrammer, kan man kjøre følgende kommando: `python3 diagrams.py`. Da vil diverse søylediagrammer og linjediagrammer bli generert i samme mappe som CSV-filene ligger. OBS! Husk å endre på `RESULTS_PATH`- eller `OUR_RESULTS_PATH`-variabelen i `constants.py`-filen for at riktig resultater blir brukt til å generere diagrammene og tabellene!

### Resultater

Alle resultatene genereres i mapper etter dato/tid for når simuleringene ble kjørt. Vi har valgt å trekke ut de nyeste resultatene, slik at de ikke ligger inni dato/tid-mappene for å lettere lese filene.

Om man ønsker å se en overordnet oversikt over resultatene i tabellform, kan man kjøre følgende kommando: `python3 tables.py`.
