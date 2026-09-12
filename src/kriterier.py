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
