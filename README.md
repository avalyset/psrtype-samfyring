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

### Amer 9 står alene

Observasjonen er generalisert til en test, og testen er kjørt på alt som finnes på disk.

Per sone, år og `psrType`: summer A73 over alle enheter og timer, sammenlign med A75s kolonne.
A73 dekker bare enheter på 100 MW eller mer, så **A73 ≤ A75 er normalen og ikke et funn**.
Funnet er kolonner der A73 *overstiger* A75 — da må minst én enhet ligge et annet sted i A75.

Tre kriterier, alle fastsatt før dommen:

1. **kildekolonne** — A73-summen overstiger A75-kolonnen.
2. **vedvarenhet** — A73 > 1,02 × A75 i mer enn **57,0 %** av timene. Terskelen er ikke valgt,
   den er **målt**: maksimum blant de **121** parene der A73 ≤ A75 og det ikke er noe å finne.
   Fordelingen der har median **0,0 %** og 90-persentil 6,1 %.
3. **entydig tilskrivning** — nøyaktig **én** (enhet, målkolonne) lukker 90–110 % av et
   *eksisterende* gap i målkolonnen og lander innenfor 2 %.

Begge tilleggene til kriterium 3 felte falske treff. Uten kravet om entydighet «forklarer» sju
Bełchatów-enheter det samme gapet på 2 100 GWh i PLs gasskolonne, fordi de alle er rundt
2 000 GWh. Uten kravet om at gapet skal finnes fra før, «avstemmer» en enhet på 68 GWh inn i en
brunkullkolonne på 31 473 GWh med 0,775 % avvik.

**130 (sone, psrType)-par i tolv sone-år:** FI 2021–2024, PL, NL, CZ, ES, AT, BE, IT og PT 2023,
DK kontrollområde 2023 og 2019+2021, GB 1.1.–31.5.2021.

**Ni par har A73 > A75. Ett består alle tre.**

| Sone | psrType | A73 | A75 | ratio | vedvarenhet | dom |
|---|---|---:|---:|---:|---:|---|
| **NL 2023** | **B01 Biomass** | **2 650,6** | **190,6** | **13,904** | **70,3 %** | **treff** |
| ES 2023 | B14 Nuclear | 50 788,4 | 19 980,3 | 2,542 | 88,9 % | A75-defekt |
| ES 2023 | B05 Fossil Hard coal | 3 733,6 | 2 174,2 | 1,717 | 80,3 % | A75-defekt |
| PL 2023 | B12 Hydro Reservoir | 176,7 | 133,3 | 1,325 | 38,3 % | støy |
| DK-CA 2023 | B04 Fossil Gas | 2 527,8 | 1 934,7 | 1,307 | 70,4 % | uavklart |
| GB 2021 | B10 Hydro Pumped | 871,0 | 764,4 | 1,139 | 64,8 % | annen akse |
| NL 2023 | B14 Nuclear | 3 579,4 | 3 500,7 | 1,022 | 22,4 % | støy |
| PL 2023 | B02 Lignite | 31 649,1 | 31 473,1 | 1,006 | 41,9 % | støy |
| FI 2021-2024 | B14 Nuclear | 105 532,2 | 105 389,7 | 1,001 | 10,5 % | støy |

**Amer 9 er enkeltstående.** Ingen annen enhet i de tolv sone-årene viser en tilskrivbar uenighet
mellom A73 og A75.

Testen er også kontrollert for tidsforskyvning: for PL `B02` er middelavviket **2,70 %** ved
lag 0 mot 6,95 % ved −1 t og 6,97 % ved +1 t. Rasteret er justert riktig.

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

**A75 er ikke alltid publisert komplett.** Spansk A75 for kjernekraft gir 15. juni 2023
timeverdier som hopper mellom 1 254 og 5 125 MW og mangler sju av døgnets 24 timer, mens A73
ligger stabilt på ~5 000 MW. Tilsvarende for spansk steinkull. **Det er en publiseringsfeil i
A75, ikke en tilordning**, og spanske A75-kolonner kan ikke brukes som fasit for A73.

**Én uenighet står uavklart.** DK-kontrollområdets gasskolonne har et vedvarende overskudd på
**593,1 GWh** (A73 2 527,8 mot A75 1 934,7, 70,4 % av timene). A75 for kontrollområdet er ikke
defekt — den er lik DK1 + DK2 på alle typer — men overskuddet lar seg ikke tilskrive én enhet.
Ført som uavklart, ikke som treff.

**En fjerde feiltype ligger utenfor dette arbeidet.** GBs `B10 Hydro Pumped` ble flagget av de
to første kriteriene, men A73 og A75 er *enige*; uenigheten er mot det britiske registeret.
Det er etikettaksen, ikke samfyringsaksen, og er ført i `kapregister` v1.1.0 som første
tilfelle på aksen *vedvarende feilklassifisering uten typeendring*.

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

### Et beslektet spor, prøvd og lukket: implisert utslippsintensitet

**Unnewehr, Weidlich, Gfüllner & Schäfer (2022) bygde koblingen ENTSO-E ↔ EUTL og regnet
implisert utslippsintensitet per anlegg.** Deres ligning (1):

> «The annual average emission factor `EF(α)` for a power plant α is calculated as the ratio of
> the total generation per year … to the corresponding emissions per power plant»

De filtrerer resultatet mot et **brenselstypespesifikt plausibilitetsbånd** — gass 300–1 000,
kull og brunkull 675–1 700 gCO₂/kWh, fra en NREL-gjennomgang — og skriver:

> «If the calculated power plant EF is outside this plausibility range, we assume potential
> issues with the underlying data (**errors, gaps, misreporting**) and omit the corresponding
> power plant from further calculations.»

Det ser ut som en detektor for feil brenselsetikett, og de peker selv på neste steg:
«for a further analysis, plant-specific EFs based on technical properties and fuel types would
have to be evaluated.» **Vi undersøkte de forkastede.**

**Reproduksjonen er eksakt.** Ligning (1) kjørt på deres egne publiserte mellomfiler gir for
`Verbund FHKW Mellach` **884,0696448879658** gCO₂/kWh. Deres egen `EF_bottom_up_method.csv`
fører `AT, hard_coal, 0.8840696448879658`. AT/hard_coal har nøyaktig én validert enhet, så
teknologifaktoren *er* anleggets faktor — kontrollen er entydig.

**Utfallet: av tolv kandidater under båndet som ikke er kraftvarme, er null et brenselsavvik.
Alle er koblingsfeil.**

- **ENGIE Eemscentrale (NL), 1 580 MW.** Koblet til A73-enhetene `Eemshaven A` og `B`. Men
  Nederlands 14.1.B har to Eemshaven-produksjonsenheter — `49W000000000044-` **Fossil Gas**
  1 410 MW og `49W000000000066Q` **Fossil Hard coal** 1 580 MW — og EUTL-kontoen er ENGIEs
  **gassanlegg**. Kullenhetenes produksjon ligger på gassanleggets utslippskonto: 1,77 Mt mot
  10,7 TWh, **en faktor fem for lavt.**
- **ČEZ, a. s., EPC PPC (CZ), 681 MW.** Koblet til `EPR2_G23/G24/G25`, som Tsjekkias 14.1.B
  fører som 1 059 MW **brunkull** — Prunéřov II. Men `EPC PPC` er Elektrárna Počerady,
  *paroplynový cyklus*, og ČEZ skriver selv i årsrapporten for 2023: «Pro **paroplynovou
  elektrárnu Počerady 2** je **zemní plyn** nakupován na velkoobchodním trhu.» Implisert faktor
  249,3 er en gassfaktor, ikke en brunkullfaktor.
- **Sju av de tolv har implisert faktor under 50 gCO₂/kWh.** Et kullverk som brenner biomasse
  ville også vist lav faktor, men **null** betyr at kontoen ikke har utslipp som svarer til
  produksjonen.

**Lærdommen: en test som leter etter feiletiketter gjennom en kobling som selv feiler, finner
koblingsfeilene først.** Koblingen ENTSO-E ↔ EUTL er en feilkilde av samme størrelsesorden som
det man leter etter.

**Plausibilitetsfilteret gjør nøyaktig det det skal.** Det Unnewehr m.fl. forkastet var dårlige
koblinger, ikke skjult signal — filteret er riktig for deres formål, som er å bygge et robust
utvalg for intensitetssignaler. Det er en annen oppgave enn å lete etter feilmerket brensel.

**Tallene, og at de er våre.** Datapakken oppgir **852 opprinnelige · 797 matchede · 554
validerte** genereringsenheter; differansen er **243**. Artikkelens tabell 5 oppgir 890 · 812 ·
595, altså **217**. Pakken er datert august 2021 og artikkelen januar 2022 — ulike kjøringer.
Listen over de forkastede er ikke publisert, og er utledet her. **Alt gjelder 2018.**

### Hvorfor intensitetsveien ikke er en akse i dette arbeidet

Den er ikke lukket fordi den ikke virker. Den er lukket fordi den **ikke når fram hit**.

CHP-korreksjonen er løst per anlegg med en proxy — `CO2_el = CO2_total − 2 × gratis kvoter`,
begrunnet med at kraftproduksjon ikke får gratistildeling i EU ETS. Proxyen er **kalibrert til
tildelingsreglene i 2018** og kan ikke overføres uten ny kalibrering.

Men den gir **ett årstall per anlegg**. For et kraftvarmeanlegg med varierende varmelast
karakteriserer det tallet ingen faktisk driftstilstand, og å måle det mot et bånd utledet for
stasjonær drift er da ikke en gyldig test. Finlands egen avgrensning er presedensen:
`erillistuotanto` omfatter kondensdelen av kraftvarmeanlegg, skilt ut **driftsvis** ved lav
varmelast — skillet går innenfor året, ikke mellom anlegg.

**Alle anleggene i denne studien er kraftvarme.** Alholmens, Poříčí, Hodonín, Amagerværket,
Avedøreværket, Studstrupværket. Metoden treffer rene kondensanlegg — og europeisk samfyring
foregår i hovedsak ikke der.

**Ført som metodegrense, ikke som nederlag:** implisert intensitet per anlegg er en brukbar vei
til feilmerket brensel *for ren kondens*, forutsatt at koblingen holder. For kraftvarme er
størrelsen ikke veldefinert som årstall.

**Etikettaksen er målt i `kapregister` v1.1.0**,
[10.5281/zenodo.22728747](https://doi.org/10.5281/zenodo.22728747), på to akser: om en enhets
registrerte type endres når anlegget konverteres, og — lagt til i v1.1 — **vedvarende
feilklassifisering uten typeendring**, der Lynemouth er første tilfelle.

**Bidraget her er målingen av at skjemaet tillater noe ingen gjør, kartleggingen av de tre
enkeltverdi-omgåelsene som brukes i stedet, og kriteriene som skiller samtidig dobbeltføring fra
omklassifisering over tid.** Ikke observasjonen, og ikke metoden.

## Sitering

| | DOI |
|---|---|
| **Denne versjonen** (v1.2.0) | *fylles inn når Zenodo har mintet den* |
| Forrige versjon (v1.1.0) | [10.5281/zenodo.22726830](https://doi.org/10.5281/zenodo.22726830) |
| Forrige versjon (v1.0.0) | [10.5281/zenodo.22726239](https://doi.org/10.5281/zenodo.22726239) |
| **Alle versjoner** (konsept) | [10.5281/zenodo.22726238](https://doi.org/10.5281/zenodo.22726238) |

Konsept-DOI-en peker alltid på nyeste versjon; versjons-DOI-ene endrer seg ikke. **Sitér
versjons-DOI-en når et tall skal kunne etterprøves.**

**Ingen tidligere versjon er trukket.** Den er frysingsøyeblikket, og Zenodo-posten for den røres ikke.
Rettelsene over står som daterte merknader, ikke som sletting. Kriteriefila `PREREG-v1.md` er
uendret i begge versjoner, `sha256 e722a60e3edf2dd843d6c3149f4d8a02f734b0905b5ed4f45e13b208e52e95db`.

## Lisens

Kode: **Apache-2.0** (`LICENSE`). Data og dokumentasjon: **CC BY 4.0** (`LICENSE-DATA`).
