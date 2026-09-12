# psrtype-samfyring

**ENTSO-Es skjema tillater å rapportere flere produksjonstyper for samme produksjonsenhet. I fire
soner der samfyring er dokumentert i primærkilde for 2021–2024, gjør ingen det — ikke i én av 238
enheter, i 1 497 dokumenter.**

```bash
python3 -m src.tell
python3 -m pytest tests/ -q
```

---

## Omfanget

| Sone | Enheter | Dokumenter | Dekning | **Treff** | Belegg for samfyring |
|---|---:|---:|---|---:|---|
| **FI** | 36 | **1 461** | **sensus** 2021–2024 | **0** | Alholmens Kraft, `Ympäristöraportti 2021` |
| **PL** | 120 | 12 | stikkprøve 2023 | **0** | Enea, ESG-rapport for 2023 |
| **NL** | 43 | 12 | stikkprøve 2023 | **0** | CBS, *Hernieuwbare energie in Nederland 2023* (2024) |
| **CZ** | 39 | 12 | stikkprøve 2023 | **0** | ČEZ, `Výroční finanční zpráva 2023` |
| **Sum belagt** | **238** | **1 497** | | **0** | |

**238 av 879 talte enheter = 27,1 %.** De øvrige 641 ligger i soner uten belagt samfyring og
**telles ikke** ([PREREG-v1.md](PREREG-v1.md) §2.4).

### Sensus mot stikkprøve

**ES, 365 av 365 døgn 2023** mot de tolv: **begge fant nøyaktig de samme elleve enhetene**,
deteksjonsrate 100 %, og **null treff i begge**. Stikkprøvens bomrate er regnet før måling og
ført i [PREREG-v1.md](PREREG-v1.md) §3 — **0,024 %** ved 50 % døgndekning, **96,8 %** ved ett døgn.

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

**`TimeSeries` er 1..unbounded per dokument, hver med nøyaktig én `psrType`, og ingen nøkkel
binder dem til én per enhet. To serier med samme EIC og ulik psrType er skjemagyldige.**

---

## Regelen finnes ikke

To ENTSO-E-dokumenter, begge lest i sin helhet:

| Dokument | Tegn | Tolv flerbrenselstermer | Kontrollstreng |
|---|---:|---|---|
| `Manual of Procedures V2R1` | 42 444 | **alle 0** | `transparency` 133, `production type` 7 |
| `Generation Load document and schema v1` | 43 532 | **alle 0** | `psrType` 31, `TimeSeries` 36 |

Termene: `co-firing`, `cofiring`, `co-fired`, `mixed fuel`, `multi-fuel`, `multiple production`,
`secondary fuel`, `main fuel`, `primary fuel`, `fuel mix`, `psrtype`, `psr type`. I
skjemadokumentet er også `predominant` og `dominant` **0**.

**Plattformen kan representere samfyring. Ingen gjør det. Ingen regel krever det.**

---

## Dekningsgrenser

**Åtte soner publiserer ikke A73 i det hele tatt:** DE-LU, DE-AT-LU, DK1, DK2, DK, GB, IE_SEM,
SE3 — alle med `Acknowledgement_MarketDocument`, kode **999**,
«No matching data found for Data item ACTUAL_GENERATION_OUTPUT_PER_UNIT_R3 [16.1.A]».

**Drax er utenfor rekkevidde.** GB publiserer ikke A73, så Europas største biomassekonvertering
kan ikke undersøkes på enhetsaksen — verken for å bekrefte eller avkrefte.

**Østerrike hadde samfyring, og den sluttet.** VERBUND, `Umwelterklärung 2024`:
«Aktivitäten zur Mitverbrennung biogener Ersatzbrennstoffe (**bis zur Einstellung des
Kohlebetriebes des FHKW Mellach mit 31.3.2020**)» — ni måneder før vinduet. AT er derfor **ubelagt
og telles ikke**, ikke talt som null.

**Stikkprøven har ingen styrke mot korte hendelser.** 96,8 % bomrate mot et éndøgnsfenomen.

---

## Hva som falt underveis

To påstander fra forarbeidet er trukket. De står her fordi de ellers ville blitt gjentatt.

### De 1 190 beviser ingenting om parallelle serier

I 1 569 dokumenter finnes **1 190 tilfeller der samme EIC har mer enn én `TimeSeries`**. Det ble
brukt som empirisk støtte for at mekanismen er i bruk.

**Alle 1 190 er retningssplitt:** én serie med `inBiddingZone_Domain` (generering) og én med
`outBiddingZone_Domain` (forbruk), med **samme `psrType`**. Fordelingen er ulik retning 1 190 ·
ulik psrType 0 · ulik businessType 0 · oppdelt tidsakse 0.

**Null parallelle genereringsserier.** XSD-beviset står; den empiriske støtten gjorde ikke.

### Ni soner ble ubelagte fordi kilden var fra 2017

Et tidligere utkast talte **879 enheter i ti soner**. Belegget for de ni ikke-finske sonene var
Embers *«Something nasty in the woodshed»* — **datert 6. oktober 2017, med 2015-tall**. En nioårig
sekundærkilde.

Etter regelen i [PREREG-v1.md](PREREG-v1.md) §2.3 teller den ikke. Omfanget falt til Finland
alene, og ble deretter bygget opp igjen til fire soner **med primærkilder lest og datert inn i
vinduet**.

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

**Etikettaksen — om en enhets registrerte type endres når anlegget konverteres — er målt i
`kapregister` v1.0.0**,
[10.5281/zenodo.22722722](https://doi.org/10.5281/zenodo.22722722).

**Bidraget her er målingen av at skjemaet tillater noe ingen gjør, og kriteriene som skiller
samtidig dobbeltføring fra omklassifisering over tid.** Ikke observasjonen, og ikke metoden.

## Lisens

Kode: **Apache-2.0** (`LICENSE`). Data og dokumentasjon: **CC BY 4.0** (`LICENSE-DATA`).
