# -*- coding: utf-8 -*-
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from src.kriterier import treff, omklassifisering, belagt_sone, bomrate

def test_treff_krever_ulik_type_samme_dokument():
    assert treff(['B10','B12']) is True
    assert treff(['B10','B10']) is False     # retningssplitt: samme type
    assert treff(['B08']) is False

def test_es_er_ikke_et_treff():
    """MUELA 1G: B12 i jan-feb, B10 fra mars. Ulike dokumenter."""
    dok = [['B12'],['B12'],['B10'],['B10'],['B10']]
    assert omklassifisering(dok) is True
    assert not any(treff(d) for d in dok)

def test_samme_doegn_slaar_ut_selv_om_typen_ogsaa_varierer_over_tid():
    dok = [['B12'],['B10','B12'],['B10']]
    assert any(treff(d) for d in dok)
    assert omklassifisering(dok) is False

def test_belagt_krever_alle_tre():
    assert belagt_sone(True, True, 2023) is True
    assert belagt_sone(True, True, 2020) is False   # AT: sluttet 31.3.2020
    assert belagt_sone(True, True, 2017) is False   # Ember 2017
    assert belagt_sone(True, False, 2023) is False  # sammendrag, ikke lest
    assert belagt_sone(False, True, 2023) is False  # sekundaer

def test_bomraten_er_den_som_staar_i_prereg():
    assert abs(bomrate(1) - 0.968) < 0.001
    assert abs(bomrate(30) - 0.357) < 0.001
    # 50 % doegndekning = 182 av 365
    assert bomrate(182) < 0.0003
