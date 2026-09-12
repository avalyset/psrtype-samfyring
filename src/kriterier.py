# -*- coding: utf-8 -*-
"""Kriteriene fra PREREG-v1 §2. Laast, skal ikke endres her."""
from __future__ import annotations

def treff(psrtyper_i_samme_dokument) -> bool:
    """TREFF = to TimeSeries, samme dokument, samme mRID, ULIK psrType (§2.1)."""
    return len(set(psrtyper_i_samme_dokument)) > 1

def omklassifisering(psr_per_dokument) -> bool:
    """Ulik type i ULIKE dokumenter er IKKE et treff (§2.2). ES er presedensen."""
    alle = {t for v in psr_per_dokument for t in v}
    return len(alle) > 1 and not any(treff(v) for v in psr_per_dokument)

def belagt_sone(primaer: bool, lest: bool, aar: int | None) -> bool:
    """BELAGT = primaer OG lest OG datert inn i 2021-2024 (§2.3)."""
    return bool(primaer and lest and aar is not None and 2021 <= aar <= 2024)

def bomrate(varighet_doegn: int, n_doegn: int = 12, aar: int = 365) -> float:
    """Sannsynlighet for at n tilfeldige doegn bommer paa et fenomen (§3)."""
    return (1 - varighet_doegn/aar) ** n_doegn

# --- PREREG-v1-TILLEGG-01, datert 2026-09-12. Legger til, endrer ingenting over. ---

A73_TERSKEL_MW = 100.0  # forordning (EU) 543/2013 artikkel 16(1)(a)

def under_terskel(genereringsenheter_mw) -> bool:
    """T1.1: alle anleggets genereringsenheter under 100 MW -> ikke i A73 i det hele tatt."""
    e = list(genereringsenheter_mw)
    return bool(e) and all(mw < A73_TERSKEL_MW for mw in e)

def telles(primaer: bool, lest: bool, aar: int | None, genereringsenheter_mw=()) -> bool:
    """En sone teller bare hvis den er belagt (§2.3) OG anleggene er over terskelen (T1.1)."""
    return belagt_sone(primaer, lest, aar) and not under_terskel(genereringsenheter_mw)
