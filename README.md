# psrtype-samfyring

**ENTSO-Es skjema tillater å rapportere to produksjonstyper for samme produksjonsenhet. Ingen
TSO gjør det. Tre TSO-er møter det samme problemet — anlegg som brenner flere brensler — og
løser det på tre forskjellige måter, alle med én verdi.**

```bash
python3 -m src.tell
python3 -m pytest tests/ -q
```

---

## De tre omgåelsene

Ingen regel sier hvordan et flerbrenselsanlegg skal føres. Resultatet er ikke en ensartet feil,
men **divergerende praksis**.

| Sone | TSO | Løsning | Belegg |
|---|---|---|---|
| **PL** | PSE | **Splitter i to produksjonsenheter.** `Połaniec 2-Pasywna` 225 MW `Biomass` og `Połaniec` 1 350 MW `Fossil Hard coal`. Samfyringen inne i kullenheten har ingen representasjon. | 14.1.B, årgang 2019 og 2025 |
| **NL** | TenneT | **Bytter etikett over tid.** `Amer` 631 MW: `Fossil Hard coal` i 2019 → `Biomass` i 2025. Etiketten følger det dominerende brenselet, med etterslep. | 14.1.B, årgang 2019 og 2025 |
| **CZ** | ČEPS | **Bruker `Other`.** `EPOR` (Poříčí), 149 → 165 MW, står som `Other` i begge årganger — verken kull eller biomasse. | 14.1.B, årgang 2019 og 2025 |

Dette er **tre ulike løsninger på et problem uten regel**, ikke tre varianter av samme feil.
Ingen av dem er den skjemaet faktisk åpner for: to `TimeSeries` for samme enhet, med hver sin
`psrType`.

---

## Enhetsoppløsningen virker

Det er verdt å slå fast før noe annet, fordi det avgjør hva funnet gjelder.

`GB-2021-*.xml`, A73 for Storbritannia: **Drax står med seks enheter og tre produksjonstyper
samtidig, i de samme dokumentene.**

| Enhet | `psrType` | GWh, 1. januar – 31. mai 2021 |
|---|---|---:|
| `DRAXX-1` | **B01 Biomass** | 1 267,5 |
| `DRAXX-2` | **B01 Biomass** | 997,1 |
| `DRAXX-3` | **B01 Biomass** | 936,6 |
| `DRAXX-4` | **B01 Biomass** | 776,2 |
| `DRAXX-6` | **B05 Fossil Hard coal** | 206,4 |
| `DRAXX-5` | **B05 Fossil Hard coal** | 97,0 |
| `DRAXX-9G`, `-10G`, `-12G` | B04 Fossil Gas | 0,1 hver |

**Plattformen håndterer blandede anlegg helt presist så lenge brenslene ligger i separate
enheter.** Konverterte enheter får `Biomass`, ukonverterte får `Hard coal`, gassturbinene får
`Fossil Gas` — samme verk, samme døgn, samme dokument.

**Hullet er dermed ikke manglende enhetsoppløsning. Hullet er brenselsblanding inne i én
enhet.** Det er den ene situasjonen skjemaet har en mekanisme for, og den ene ingen bruker.

---

## Omfanget

| Sone | Enheter | Dokumenter | Dekning | **Treff** | Belegg for samfyring |
|---|---:|---:|---|---:|---|
| **FI** | 36 | **1 461** | **sensus** 2021–2024 | **0** | Alholmens Kraft, `Ympäristöraportti 2021` |
| **PL** | 120 | **365** | **sensus** 2023 | **0** | Enea, ESG-rapport for 2023 |
| **NL** | 43 | **365** | **sensus** 2023 | **0** | CBS, *Hernieuwbare energie in Nederland 2023* (2024) |
| **Sum belagt** | **199** | **2 191** | | **0** | |

**199 av 879 talte enheter = 22,6 %.** Resten ligger i soner uten belagt samfyring og
**telles ikke** ([PREREG-v1.md](PREREG-v1.md) §2.4).

**CZ er tatt ut.** Se «Hva som falt underveis».

**To soner til er målt, og telles ikke.** Danmark (kontrollområdet) gir **365 dokumenter,
25 enheter, 0 treff** for 2023; Storbritannia gir **113 dokumenter, 268 enheter, 0 treff** for
1. januar – 31. mai 2021. For ingen av dem er samfyring i vinduet belagt i en primærkilde som er
lest og datert, og etter [PREREG-v1.md](PREREG-v1.md) §2.4 er null der ikke evidens. De står
her fordi de ble målt, ikke fordi de teller.

### Sensus mot stikkprøve

**ES, 365 av 365 døgn 2023** mot tolv døgn: **begge fant nøyaktig de samme elleve enhetene**,
deteksjonsrate 100 %, og **null treff i begge**. PL og NL er siden kjørt som sensus over alle
365 døgn i 2023 og gir samme svar som tolvdøgnsutvalget ga: null.

Stikkprøvens bomrate er regnet før måling og ført i [PREREG-v1.md](PREREG-v1.md) §3 —
**0,024 %** ved 50 % døgndekning, **96,8 %** ved ett døgn.

---

## Kausaliteten: hva som faktisk bokføres

**Enea Elektrownia Połaniec, 2023.** Anlegget har et dedikert biomasseanlegg (Zielony Blok) og
syv kullblokker, hvorav blokk 2–7 samfyrer. Fra Eneas egen ESG-rapport for 2023:

> Całkowite wytwarzanie energii elektrycznej (netto) **6 628** GWh · Produkcja netto ze źródeł
> konwencjonalnych **4 870** · Produkcja z OZE (spalanie biomasy – Zielony Blok) **1 507** ·
> Produkcja z OZE (**współspalanie** biomasy) **252**

og om hvilke blokker: «projekty Elektrowni Połaniec obejmujące **bloki od 2 do 7**; wprowadziliśmy
zmiany związane ze **współspalaniem węgla i biomasy**».

A73 for hele 2023, sensus over 365 døgn:

| A73-enhet | `psrType` | GWh |
|---|---|---:|
| `Połaniec 2 blok 9` | B01 Biomass | **1 505,7** |
| `Połaniec B1`–`B7` (sum) | B05 Fossil Hard coal | **5 235,6** |
| sum, hele anlegget | | 6 741,3 |

**Referansemålingen først.** Zielony Blok er dedikert biomasse — A73 og anleggets egen rapport
måler det samme: **1 505,7 mot 1 507,0 GWh, R = 0,999.** Bokføringen per enhet er presis når
enheten brenner ett brensel. Metoden er dermed ikke kilden til avviket.

A73 ligger systematisk **1,71 %** over Eneas nettotall på anleggsnivå (6 741,3 mot 6 628,0).
Normalisert bort:

| A73 `B05` normalisert | mot | GWh | **R** |
|---:|---|---:|---:|
| 5 147,6 | **hele produksjonen** i blokk 2–7 (4 870 + 252) | 5 122,0 | **1,005** |
| 5 147,6 | **kull-tilskrevet** produksjon alene (4 870) | 4 870,0 | 1,057 |

**A73s kullkolonne matcher hele blokkenes produksjon til 0,5 %, ikke den kull-tilskrevne delen.**
Hele enhetens produksjon føres under ett brensel. Samme mekanisme er vist for Alholmens Kraft
AK 2 i Finland — nå på et annet anlegg, i en annen sone, med en intern referansemåling.

---

## Samme enhet, to produksjonstyper — i to ulike dataprodukter

Dette er ikke et treff etter [PREREG-v1.md](PREREG-v1.md) §2.1, som krever to `TimeSeries` i
**samme** dokument. Det er noe annet, og det ble funnet mens omfanget ble utvidet til sensus.

**`Amer 9` bærer `B01 Biomass` i A73 og telles i `Fossil Hard coal` i A75.** Samme TSO, samme
enhet, samme år.

A73 for Nederland 2023, sensus over 365 døgn, alle enheter med kull- eller biomasseetikett:

| A73-enhet | `psrType` | GWh 2023 |
|---|---|---:|
| `Maasvlakte 3` | B05 Fossil Hard coal | 3 334,9 |
| `Eemshaven A` | B05 Fossil Hard coal | 2 500,2 |
| `Eemshaven B` | B05 Fossil Hard coal | 1 961,2 |
| `NLROTTETH__1` | B05 Fossil Hard coal | 1 445,4 |
| **sum `B05`** | | **9 241,7** |
| `Amer 9` | **B01 Biomass** | **2 650,6** |

A75 for samme sone og år, summert time for time fra tolv månedsdokumenter:

| | GWh 2023 |
|---|---:|
| A75 `Fossil Hard coal` | **11 897,1** |
| A73 `B05` + `Amer 9` | **11 892,3** |
| **avvik** | **−4,8 GWh = −0,040 %** |
| A75 `Biomass` | 190,6 |

**Regnestykket går bare opp hvis Amer 9 ligger i kullkolonnen.** A75s `Biomass`-kolonne er
190,6 GWh for hele året — Amer 9 alene er 2 650,6. Enheten er ikke der.

Og andelen stemmer med den uavhengige kilden: 3 775,3 / 11 897,1 = **31,7 %**, mot CBS' **31 %
av den totale energiinnsatsen i kolencentrales**. De to er ikke identiske størrelser —
CBS måler innsats, dette måler utbytte, og de faller sammen bare hvis brenslene omdannes med
lik virkningsgrad — men de peker på samme tall.

**Konsekvensen:** kullkolonnen i A75 for Nederland inneholder én enhet som ENTSO-Es eget
enhetsdatasett fører som biomasse. Det er ikke samfyring inne i én enhet; det er to
dataprodukter fra samme leverandør som ikke er enige om hva enheten brenner.

---

## Regelverkskjeden

**Ingen regel krever det, og ingen regel forbyr det.** Fraværet er dokumentert på tre nivåer.

**1. Forordningen.** Kommisjonsforordning (EU) nr. **543/2013**, EUR-Lex CELEX `32013R0543`.
Artikkel 16 nr. 1, ordrett:

> «(a) actual generation output (MW) per market time unit and **per generation unit** of 100 MW
> or more installed generation capacity; (b) **aggregated** generation output per market time
> unit and **per production type**»

**Produksjonstype nevnes ikke i bokstav (a).** Kravet til 16.1.A er ren effekt per
genereringsenhet. `psrType` på A73 er ENTSO-Es eget tillegg gjennom skjemaet — ikke et
forordningskrav.

**2. Delegasjonen.** Artikkel 5, ordrett:

> «The ENTSO for Electricity shall develop a manual specifying: … (d) **appropriate
> classification of production types** referred to in Articles 14(1), 15(1) and 16(1).»

Klassifiseringen er delegert til ENTSO-Es Manual of Procedures.

**3. Manualen.** Lest i sin helhet. Ingen av tolv flerbrenselstermer forekommer.

| | forordning 543/2013 | Manual of Procedures |
|---|---:|---:|
| `co-firing` · `cofiring` · `co-fired` | 0 · 0 · 0 | 0 · 0 · 0 |
| `mixed fuel` · `multi-fuel` · `multiple production` | 0 · 0 · 0 | 0 · 0 · 0 |
| `secondary fuel` · `main fuel` · `primary fuel` · `fuel mix` | 0 · 0 · 0 · 0 | 0 · 0 · 0 · 0 |
| `predominant` · `dominant` | 0 · 0 | 0 · 0 |
| *kontroll* `production type` | **8** | **7** |
| *kontroll* `generation unit` | **18** | — |
| *kontroll* `transparency` | **14** | **133** |
| tegn i dokumentet | 43 092 | **42 444** |

**Nasjonalt nivå er uavklart, ikke belagt fravær.** PSE, URE, ČEPS, OTE og ACM ble hentet og gav
2 771–15 896 tegn tekst — JavaScript-genererte skall. **Kontrollstrengene traff ikke** (`ENTSO`
gir 0 på PSE, OTE og ACM), så søket virket ikke; det er ikke det samme som at feltet er tomt.
TenneT svarer **403** på ren HTTP. For å lukke dette trengs TSO-enes egne
datalevering-dokumenter, ikke landingssider.

---

## XSD-beviset

Kilde: **`Generation Load document and schema v1`**, ENTSO-E EDI Library,
`eepublicdownloads.entsoe.eu/clean-documents/EDI/Library/cim_based/schema/`.
**588 944 B**, `sha256 a0d80ff18f7b3f06016076905b8e3c40a5c524d78d93dbc1db06cebe2a4e834b`.
**PDF-en er ikke inkludert her** — den er ENTSO-Es, og siteres.

Kardinalitetene, ordrett fra XSD-en gjengitt i dokumentet:

```xml
<xs:element name="TimeSeries"              type="TimeSeries"        minOccurs="1" maxOccurs="unbounded"/>
<xs:element name="MktPSRType"              type="MktPSRType"        minOccurs="0" maxOccurs="1"/>
<xs:element name="psrType"                 type="PsrType_String"    minOccurs="1" maxOccurs="1"/>
<xs:element name="PowerSystemResources"    type="MktGeneratingUnit" minOccurs="0" maxOccurs="unbounded"/>
<xs:element name="registeredResource.mRID" type="ResourceID_String" minOccurs="0" maxOccurs="1"/>
```

Og ingen unikhetsbetingelse finnes:

| Betingelse | Forekomster |
|---|---:|
| `xs:unique`, `xs:key`, `xs:keyref` | **0, 0, 0** |
| `xs:selector`, `xs:field`, `xs:assert`, `xs:ID` | **0, 0, 0, 0** |
| *kontroll* `xs:element` | 38 |
| *kontroll* `minOccurs` / `maxOccurs` | 37 / 37 |
| *kontroll* `</xs:schema>` | 1 |

Ordet «unique» står åtte ganger i dokumentet — **alle åtte i prosabeskrivelser av attributter**,
ingen som skjemabetingelse.

Kontrollstrengene for selve dokumentet: **43 532 tegn**, `TimeSeries` **36**, `psrType` **31**.
Tellingen av `psrType` er **ufølsom for store og små bokstaver** (24 `MktPSRType` + 4
`PsrType_String` + 3 `psrType`); case-sensitivt er tallet 3.

**`TimeSeries` er 1..unbounded per dokument, hver med nøyaktig én `psrType`, og ingen nøkkel
binder dem til én per enhet. To serier med samme EIC og ulik psrType er skjemagyldige.**

---

## Nedstrøms: hvem det biter på

**Ember har funnet dette — for Finland, og skriver det.** Fra
`ember_electricity_data_methodology.pdf` (1 492 958 B,
`sha256 4044e49f2aa7de3b3f5309ad22d425906430e61cdfc0dcbc1afba9f4b145e309`), landkapittelet for
Finland, ordrett:

> «**Finnish data in ENTSO-E is known to undercount Bioenergy**, and to show low volatility
> compared to expectation. We therefore take Bioenergy, Solar, Gas, Wind and Hydro **from
> Eurostat monthly data**.»

og generelt, om retningen de har sett:

> «Bioenergy is also frequently cofired with fossil fuels. We have disaggregated these wherever
> possible, but in certain cases **recorded bioenergy generation may include some co-firing**. In
> these circumstances, actual emissions will be higher than we estimate.»

Korreksjonen er ikke anvendt på PL eller NL. Embers landkapitler oppgir at **PLs månedsserie
kommer fra ENTSO-E**, mens **NLs kommer fra CBS og NED** — nasjonal statistikk, ikke ENTSO-E.

**Electricity Maps har ingen korreksjon.** Kodesøk over `electricitymaps/electricitymaps-contrib`:
`cofiring` **0**, `co-firing` **0**, `co-fired` **0** (kontroll: `biomass` 502, `psrType` 16).
Parseren tar `psrType` på pålydende — `B02`, `B05`, `B07`, `B08` → `COAL`; `B01`, `B17` →
`BIOMASS`.

Men utslippsfaktoren settes ikke fra litteratur. Den **utledes** som `EU-ETS-utslipp ÷
ENTSO-E-generering` (kilde oppgitt i sonefilene: «EU-ETS 2025, ENTSO-E 2024»). ETS teller
biomasse som null, og da blir

> tilskrevet CO₂ = (ETS ÷ MWh_rapportert) × MWh_rapportert = ETS

**Sonetotalen blir riktig uansett hvor mye biomasse som ligger i kullkolonnen. Feilen flytter seg
fra totalen til faktoren** — og faktoren viser den:

| Sone | Electricity Maps' kullfaktor | mot litteratur 995 | implisitt nullkarbonandel |
|---|---:|---:|---:|
| **NL** | **756,63** | | **+24,0 %** |
| FI | 961,66 | | +3,4 % |
| CZ | 992,75 | | +0,2 % |
| PL | 1 019,85 | | −2,5 % |

NL er det rene tilfellet: kullkolonnen er ren `B05`, ingen brunkull. **Den utledede faktoren
bærer en fortynning på 24 %, der CBS dokumenterer 31 % av energiinnsatsen.** Samme retning,
samme størrelsesorden, to uavhengige veier. For PL og CZ er testen konfundert av at «coal» slår
sammen `B02`+`B05`+`B07`+`B08`, og brunkull har høyere faktor enn 995.

**Konsekvensen er ikke at totalen blir gal, men at faktoren ikke er en kullfaktor.**

**Hvem det faktisk biter på:** den som henter **A75 eller A73 direkte og legger på en
litteraturfaktor** — og den som henter en ETS-utledet faktor og bruker den på et annet datasett.
Ikke «alle som bruker tallene».

### Effekten, tallfestet

Karbonintensitet for 2023 regnet på A75 som den står, og på nytt med dokumentert
biomasse-elektrisitet flyttet fra kull-koden til `B01`. Faktorsett: codecarbons
`carbon_intensity_per_source.json` (kull 995, gass 743, olje 816, «fossil» 635, kjerne 29, sol 48,
vind/vann 26, biomasse og avfall 0 gCO2eq/kWh).

| Sone | A75 total | som den står | korrigert | differanse | | flyttet |
|---|---:|---:|---:|---:|---|---:|
| **NL** | 108 426,8 GWh | **552,40** | 517,76 | **−34,64 g/kWh** | **−6,27 %** | 3 775 GWh |
| NL, nedre | | | 520,77 | −31,63 g/kWh | −5,73 % | 3 447 GWh |
| **PL** | 153 207,4 GWh | **713,86** | 712,22 | **−1,64 g/kWh** | **−0,23 %** | 252 GWh |

Differansen i g/kWh er uavhengig av resten av miksen: Δ = −(995 − 0) · X / total. Bare prosenten
avhenger av basis.

**NL-tallet hviler på tre uavhengige veier:**

| | GWh |
|---|---:|
| CBS tabell 8.3.2, elektrisitet fra medfyrt biomasse (13 591 TJ) | **3 775,3** |
| 31 % av A75s kullkolonne (CBS' andel av energiinnsatsen) | 3 688,1 |
| A75 `Fossil Hard coal` minus Ember/OWIDs kulltall (11 897,1 − 8 450) | 3 447,1 |

Spredningen er 9 %. **CBS-tallet brukes som sentralestimat** fordi det er den eneste av de tre
som er en direkte måling, og fordi det treffer kullkolonnen på 31,7 % — se avsnittet om Amer 9.
Den laveste er oppgitt som nedre grense.

**PL-tallet er lite fordi anlegget er lite**, ikke fordi mekanismen er svak. Połaniecs samfyring
er 0,16 % av polsk produksjon.

**Grense ved NL-beregningen:** NLs A75 bærer ikke en brukbar brenselsmiks uansett samfyring.
`B20 Other` er **35,3 %** av kolonnen, og `B16 Solar` er 546,6 GWh mot OWIDs 21 150 GWh for samme
år. De absolutte CI-verdiene for NL er derfor ikke meningsfulle. Differansen er det.

---

## Dekningsgrenser

**A73 er ikke tilgjengelig i alle soner, og ikke i alle år.** Prøve på tre døgn per år
(15. januar, 15. juni, 15. november) for 2019, 2021 og 2023. Et `Acknowledgement_MarketDocument`
med kode 999 er 968 B; alt over er innhold.

| Domene | EIC | 2019 | 2021 | 2023 |
|---|---|---|---|---|
| **DK, kontrollområde** | `10Y1001A1001A796` | **ja** | **ja** | **ja** |
| DK1 · DK2 · DK land | `10YDK-1--------W` · `10YDK-2--------M` · `10Y1001A1001A65H` | nei | nei | nei |
| **GB** | `10YGB----------A` | **ja** | **til 31.05.** | nei |
| DE-LU | `10Y1001A1001A82H` | nei | nei | nei |
| DE-AT-LU | `10Y1001A1001A63L` | nei | nei | nei |
| IE_SEM | `10Y1001A1001A59C` | nei | nei | nei |
| SE3 | `10Y1001A1001A46L` | nei | nei | nei |

**Danmark publiserer A73** — men under **kontrollområde-domenet `10Y1001A1001A796`**, ikke under
budsonene. `DK-CA-2023-01-15.xml` gir 22 navngitte enheter, 0 med mer enn én `psrType`:
Amagerværket 3 (`Hard coal`) og 4 (`Biomass`), Asnæsværket 2 og 5, Avedøreværket 1 og 2,
Esbjergværket 3, Fynsværket 7, Nordjyllandsværket 3, Kyndbyværket 21 og 22, Silkeborgværket,
Skærbækværket 3, Studstrupværket 3 og 4, samt seks havvindparker.

**GB publiserte til og med 31. mai 2021.** Sensus over 1. januar – 31. mai 2021 gir **113
dokumenter med innhold og 38 tomme**, 268 enheter, 0 treff. Prøven for 15. juni 2021 og senere er
tom. Dekningen er ujevn også innenfor perioden: januar 21/31, februar 28/28, mars 12/31, april
25/30, mai 27/31.

**Fem soner er tomme i alle tre testede år:** DE-LU, DE-AT-LU, IE_SEM, SE3 og de tre danske
budsone-domenene.

**Anlegg under terskelen kan ikke nås.** Artikkel 16(1)(a) gjelder genereringsenheter på 100 MW
eller mer. Det er ikke en svakhet ved metoden, men en grense for hva A73 i det hele tatt
inneholder — og den felte Tsjekkia, se under.

**Stikkprøven har ingen styrke mot korte hendelser.** 96,8 % bomrate mot et éndøgnsfenomen.
PL, NL, FI og ES er derfor kjørt som sensus.

---

## Hva som falt underveis

Fem påstander fra forarbeidet og fra v1.0.0 er trukket. De står her fordi de ellers ville blitt
gjentatt.

### Rettet 2026-09-12, etter v1.0.0

**v1.0.0 skrev: «Åtte soner publiserer ikke A73 i det hele tatt: DE-LU, DE-AT-LU, DK1, DK2, DK,
GB, IE_SEM, SE3».** Det stemmer for de tre danske budsone-domenene, men **ikke for Danmark**:
kontrollområdet `10Y1001A1001A796` publiserer A73 i 2019, 2021 og 2023. Og **ikke for GB**, som
publiserte til og med 31. mai 2021 — fire måneder inne i vinduet 2021–2024. Fem soner står
igjen, ikke åtte.

**v1.0.0 skrev: «Drax er utenfor rekkevidde … kan ikke undersøkes — verken for å bekrefte eller
avkrefte».** Feil. Drax ligger i A73 for 2019 og januar–mai 2021, med seks enheter og tre
produksjonstyper. Se «Enhetsoppløsningen virker». Funnet ble sterkere, ikke svakere.

**v1.0.0 talte CZ som belagt sone med 39 enheter.** ČEZs to dokumenterte samfyringsanlegg er
**Hodonín** (1× 50 MW + 1× 57 MW) og **Poříčí II** (3× 55 MW). **Alle genereringsenhetene er
under 100 MW-terskelen i artikkel 16(1)(a)** og finnes derfor ikke i A73 i det hele tatt.
Kontroll: ingen av de 39 tsjekkiske A73-enhetene er Hodonín eller Poříčí — `EPR1`/`EPR2` er
Prunéřov I og II (393 og 1 059 MW, ren brunkull).

CZ er **usynlig av kapasitetsgrunner, ikke av merkegrunner**, og et null derfra er ikke evidens
om merkepraksis. Sonen er tatt ut av tellingen. Registeret (14.1.B) tar derimot Poříčí med, og
det er der `Other`-føringen ble funnet — se «De tre omgåelsene».

### Fra forarbeidet

**De 1 190 beviser ingenting om parallelle serier.** I 1 569 dokumenter finnes 1 190 tilfeller
der samme EIC har mer enn én `TimeSeries`. Det ble brukt som empirisk støtte for at mekanismen
er i bruk. **Alle 1 190 er retningssplitt:** én serie med `inBiddingZone_Domain`, én med
`outBiddingZone_Domain`, **samme `psrType`**. Ulik psrType 0 · ulik businessType 0 · oppdelt
tidsakse 0. XSD-beviset står; den empiriske støtten gjorde ikke.

**Ni soner ble ubelagte fordi kilden var fra 2017.** Et tidligere utkast talte 879 enheter i ti
soner. Belegget for de ni ikke-finske var Embers *«Something nasty in the woodshed»* — **datert
6. oktober 2017, med 2015-tall**. Etter [PREREG-v1.md](PREREG-v1.md) §2.3 teller den ikke.

---

## Forutgående arbeid

**Verken observasjonen eller metoden er ny.**

Feiletikettering av konverterte anlegg i ENTSO-E ble beskrevet og kvantifisert i
[electricitymaps-contrib#1161](https://github.com/electricitymaps/electricitymaps-contrib/issues/1161)
(28.02.2018), tatt opp igjen i
[#3602](https://github.com/electricitymaps/electricitymaps-contrib/issues/3602) (11.12.2021), og
svensk aggregering er dokumentert i
[#872](https://github.com/electricitymaps/electricitymaps-contrib/issues/872) (27.11.2017).
Massebevaringsprinsippet er formulert i **Hirth, Mühlenpfordt & Bulkeley (2018)**,
[10.1016/j.apenergy.2018.04.048](https://doi.org/10.1016/j.apenergy.2018.04.048).
**Unnewehr, Weidlich, Gfüllner & Schäfer (2022)**,
[10.1016/j.cles.2022.100018](https://doi.org/10.1016/j.cles.2022.100018), koblet ENTSO-E mot
EU ETS på EIC. **Towards Standardized Grid Emission Factors**,
[arXiv:2311.01103](https://arxiv.org/abs/2311.01103), dekker seks CHP-allokeringsmetoder og slår
fast at «no consensus appears to exist which one is the "correct" or most suitable one».

**Ember har publisert observasjonen for Finland** i sin metodedokumentasjon: ENTSO-E-dataene
underteller bioenergi, og de bytter derfor kilde til Eurostat. Sitert ordrett under «Nedstrøms».

**Etikettaksen — om en enhets registrerte type endres når anlegget konverteres — er målt i
`kapregister` v1.0.0**,
[10.5281/zenodo.22722722](https://doi.org/10.5281/zenodo.22722722).

**Bidraget her er målingen av at skjemaet tillater noe ingen gjør, kartleggingen av de tre
enkeltverdi-omgåelsene som brukes i stedet, og kriteriene som skiller samtidig dobbeltføring fra
omklassifisering over tid.** Ikke observasjonen, og ikke metoden.

## Sitering

| | DOI |
|---|---|
| **Denne versjonen** (v1.1.0) | [10.5281/zenodo.22726830](https://doi.org/10.5281/zenodo.22726830) |
| Forrige versjon (v1.0.0) | [10.5281/zenodo.22726239](https://doi.org/10.5281/zenodo.22726239) |
| **Alle versjoner** (konsept) | [10.5281/zenodo.22726238](https://doi.org/10.5281/zenodo.22726238) |

Konsept-DOI-en peker alltid på nyeste versjon; versjons-DOI-ene endrer seg ikke. **Sitér
versjons-DOI-en når et tall skal kunne etterprøves.**

**v1.0.0 er ikke trukket.** Den er frysingsøyeblikket, og Zenodo-posten for den røres ikke.
Rettelsene over står som daterte merknader, ikke som sletting. Kriteriefila `PREREG-v1.md` er
uendret i begge versjoner, `sha256 e722a60e3edf2dd843d6c3149f4d8a02f734b0905b5ed4f45e13b208e52e95db`.

## Lisens

Kode: **Apache-2.0** (`LICENSE`). Data og dokumentasjon: **CC BY 4.0** (`LICENSE-DATA`).
