# Tillegg 01 til PREREG-v1

**Datert 2026-09-12.** [PREREG-v1.md](PREREG-v1.md) er uendret,
`sha256 e722a60e3edf2dd843d6c3149f4d8a02f734b0905b5ed4f45e13b208e52e95db`. Dette tillegget
legger til én kategori som manglet, og utvider utvalget. Det endrer ikke definisjonen av TREFF.

---

## T1.1 — ny kategori: BELAGT SONE UNDER RAPPORTERINGSGRENSEN

§2.3 skiller mellom belagt og ubelagt sone. Den manglet et tilfelle:

**En sone kan ha dokumentert samfyring i en primær, lest og datert kilde, og likevel ikke kunne
testes — fordi anleggene ligger under terskelen A73 i det hele tatt dekker.**

Artikkel 16(1)(a) i forordning (EU) 543/2013 krever rapportering per **genereringsenhet på
100 MW eller mer**. Et anlegg hvis genereringsenheter alle er mindre, finnes ikke i A73 —
uavhengig av hvordan det ville blitt merket.

**En slik sone telles ikke**, av samme grunn som §2.4: null der er ikke evidens om merkepraksis.
Den føres som **belagt, men under rapporteringsgrensen**, med anleggenes enhetsstørrelser
oppgitt.

**Tilfellet som utløste kategorien:** Tsjekkia. ČEZ, `Výroční finanční zpráva 2023`, dokumenterer
samfyring ved **Hodonín** (1× 50 MW + 1× 57 MW) og **Poříčí II** (3× 55 MW). Alle fem
genereringsenheter er under 100 MW. Kontroll: ingen av de 39 tsjekkiske A73-enhetene er Hodonín
eller Poříčí.

CZ var talt som belagt sone i v1.0.0 med 39 enheter. Det var feil, og er rettet.

## T1.2 — utvalget utvidet fra stikkprøve til sensus

§3 låste stikkprøven til den 15. i hver måned, tolv døgn per sone, med FI og ES som sensus.
**Utvalget er siden utvidet, ikke endret:**

| Sone | v1.0.0 | v1.1 |
|---|---|---|
| FI | sensus 1 461 døgn 2021–2024 | uendret |
| ES | sensus 365 døgn 2023 | uendret |
| PL | stikkprøve 12 døgn | **sensus 365 døgn 2023** |
| NL | stikkprøve 12 døgn | **sensus 365 døgn 2023** |
| CZ | stikkprøve 12 døgn | sensus 365 døgn 2023, men sonen telles ikke (T1.1) |

**Begge utvidelsene ga samme svar som stikkprøven ga:** samme enhetstall (PL 120, NL 43), null
treff. Det er den tredje bekreftelsen av at stikkprøvens styrke er som forhåndsregnet — ES var
den første.

## T1.3 — to soner målt uten å telles

Danmark og Storbritannia publiserer A73 i deler av vinduet. Begge er målt og gir null. **Ingen av
dem er belagt sone** — det er ikke lest en primær, datert kilde for samfyring i vinduet for noen
av dem — og etter §2.4 telles de ikke.

| Sone | Domene | Dekning | Enheter | Treff |
|---|---|---|---:|---:|
| DK, kontrollområde | `10Y1001A1001A796` | sensus 365 døgn 2023 | 25 | 0 |
| GB | `10YGB----------A` | 113 døgn med data, 1.1.–31.5.2021 | 268 | 0 |

De står ført fordi de ble målt, ikke fordi de teller. Skulle samfyring i vinduet bli belagt i en
primærkilde for en av dem, kan tallene tas inn uten ny måling.

## T1.4 — observasjon utenfor §2.1

`Amer 9` bærer `B01 Biomass` i A73 og ligger i `Fossil Hard coal` i A75 for samme sone og år.
**Dette er ikke et treff etter §2.1**, som krever to `TimeSeries` i samme dokument. Det er en
uoverensstemmelse mellom to dataprodukter, og det er ført som egen observasjon i README —
ikke i tellingen.
