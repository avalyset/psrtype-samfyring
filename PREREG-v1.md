# Preregistrering v1 — psrType og samfyring

**Låst 2026-09-12.** Endringer føres som daterte tillegg i egen fil, aldri ved redigering.

---

## 1. Spørsmålet

**Rapporterer noen TSO mer enn én produksjonstype for samme produksjonsenhet i ENTSO-Es A73, i
soner der samfyring er dokumentert?**

Deskriptivt. Vi måler hva dataene gjør.

## 2. Definisjonene, låst

### 2.1 TREFF

**To `TimeSeries` i samme `GL_MarketDocument`, med samme
`MktPSRType/PowerSystemResources/mRID` og ulik `psrType`.**

Samme dokument betyr samme døgn, siden A73 har hard P1D-grense. **Samtidighet er kravet.**

### 2.2 IKKE et treff — omklassifisering over tid

At en enhet bærer én `psrType` i én periode og en annen i en senere periode er **ikke** et treff.

**Presedens, ført før måling:** MUELA 1G–7G og SALLENT 1G–4G i ES bærer `Hydro Water Reservoir`
i januar–februar 2023 og `Hydro Pumped Storage` fra mars. Elleve enheter. **Ingen av dem bærer
begge i samme dokument.** De er en registeromklassifisering som forplanter seg — den samme ES
har i 14.1.B — og de telles ikke.

### 2.3 BELAGT SONE

En sone teller **bare** når samfyring er dokumentert i en kilde som er

1. **primær** — anleggets eller operatørens egen rapportering, nasjonal statistikk, eller
   myndighetskilde,
2. **lest** i sin helhet, ikke gjengitt fra et søkesammendrag,
3. **datert inn i vinduet 2021–2024.**

**Et sekundærsammendrag teller ikke.** Regelen finnes fordi tre påstander i forarbeidet falt på
nettopp det: «Rauhalahti 100 % tre» (primærkilden sa støttebrensel), «SEVO >90 % torv» (tallet
var fra 2008), «Aittaluoto avviklet 2022» (aldri lest).

**Et sammendrag bærer ikke alder.** Det gjengir en setning uten å si når den ble skrevet.

### 2.4 UBELAGT SONE telles ikke som null

En sone uten dokumentert samfyring har ingenting å representere. **Null treff der er ikke
evidens.** Den føres som ubelagt, med antall enheter oppgitt, og holdes utenfor konklusjonen.

**Dette er den sentrale feilslutningen i designet**, og 2.3 og 2.4 finnes for å hindre den.

## 3. Utvalg og styrke, tallfestet før måling

**Stikkprøve: den 15. i hver måned, tolv døgn per sone.** Finland er sensus over 1 461 døgn
2021–2024. ES er sensus over 365 døgn 2023.

**Bomraten er regnet og ført:**

| Fenomenets varighet | Sannsynlighet for at 12 døgn bommer |
|---|---:|
| 1 døgn | **96,8 %** |
| 7 døgn | 79,3 % |
| 30 døgn | 35,7 % |

| Andel døgn med dobbeltføring | Bomrate |
|---|---:|
| 25 % | 3,17 % |
| **50 %** | **0,024 %** |
| 80 % | ~0 |

**Stikkprøven er gyldig for et vedvarende fenomen og svak mot et sjeldent.** Et samfyrt anlegg
som rapporterte begge brensler ville gjort det hver dag det samfyrer. **Designet er valgt mot det
fenomenet, og har ingen styrke mot enkelthendelser.**

**Verifisert:** ES-sensus over 365 døgn fant nøyaktig de samme elleve enhetene som tolv døgn
fant. Deteksjonsrate 100 %, og null treff i begge.

## 4. Hva som IKKE måles

- **Om praksisen er gal.** Vi måler at den finnes, ikke om den burde vært annerledes.
- **Hvem som bør endre den.** Ansvarsdelingen mellom TSO, ENTSO-E og anleggseier er ikke
  undersøkt og skal ikke antydes.
- **CHP-allokering mellom el og varme.** Felt fire ganger i forarbeidet, algebraisk og empirisk.
  Gjenopptas ikke uten ny evidens.
- **Konvertering og etikettetterslep.** Det er `kapregister`,
  [10.5281/zenodo.22722722](https://doi.org/10.5281/zenodo.22722722).
- **Anlegg under A73s rapporteringsgrense.** De kan ikke nås på denne aksen.

## 5. Kjente begrensninger, ført før resultatene

1. **Åtte soner publiserer ikke A73** — DE-LU, DE-AT-LU, DK1, DK2, DK, GB, IE_SEM, SE3. Alle gir
   `Acknowledgement_MarketDocument` kode 999.
2. **Drax er utenfor rekkevidde.** GB publiserer ikke A73. Europas største biomassekonvertering
   kan ikke undersøkes.
3. **Stikkprøven har ingen styrke mot korte hendelser.** Se §3.
4. **Belegget varierer i styrke mellom soner** — ett anleggs regnskap er svakere enn nasjonal
   statistikk for en hel anleggsklasse.

## 6. Forhåndsspesifisert utfall

- **Null treff i alle belagte soner** → ingen TSO rapporterer samfyring per enhet, selv om
  skjemaet tillater det.
- **Treff i minst én belagt sone** → praksisen er ikke universell, og spørsmålet blir hvem som
  gjør hva.
- **Ingen sone lar seg belegge** → dataene bærer ikke spørsmålet.

## 7. Forutgående arbeid

**Verken observasjonen eller metoden er ny.**
[#1161](https://github.com/electricitymaps/electricitymaps-contrib/issues/1161) (28.02.2018),
[#3602](https://github.com/electricitymaps/electricitymaps-contrib/issues/3602) (11.12.2021),
[#872](https://github.com/electricitymaps/electricitymaps-contrib/issues/872) (27.11.2017),
Hirth m.fl. (2018) [10.1016/j.apenergy.2018.04.048](https://doi.org/10.1016/j.apenergy.2018.04.048),
Unnewehr m.fl. (2022) [10.1016/j.cles.2022.100018](https://doi.org/10.1016/j.cles.2022.100018),
og *Towards Standardized Grid Emission Factors* [arXiv:2311.01103](https://arxiv.org/abs/2311.01103),
som dekker seks CHP-allokeringsmetoder og sier at «no consensus appears to exist which one is the
"correct" or most suitable one».

**Etikettaksen er målt i `kapregister` v1.0.0**,
[10.5281/zenodo.22722722](https://doi.org/10.5281/zenodo.22722722).

**Bidraget her er målingen at skjemaet tillater noe ingen gjør, og kriteriene som skiller
samtidig dobbeltføring fra omklassifisering over tid.**
