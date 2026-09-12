# -*- coding: utf-8 -*-
"""Teller psrType per produksjonsenhet, per sone. Stikkprøve over de hentede doegnene."""
import os, pathlib, collections, json
import xml.etree.ElementTree as ET
NS={'g':'urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0'}
PSR={'B01':'Biomass','B02':'Lignite','B03':'Coal-derived gas','B04':'Fossil Gas',
     'B05':'Fossil Hard coal','B06':'Fossil Oil','B07':'Oil shale','B08':'Fossil Peat',
     'B09':'Geothermal','B10':'Hydro Pumped','B11':'Hydro RoR','B12':'Hydro Reservoir',
     'B13':'Marine','B14':'Nuclear','B15':'Other renewable','B16':'Solar','B17':'Waste',
     'B18':'Wind Offshore','B19':'Wind Onshore','B20':'Other','B25':'Energy storage'}

def tell(katalog, prefiks=None):
    per=collections.defaultdict(lambda: collections.defaultdict(set))  # sone->eic->{psr}
    navn=collections.defaultdict(dict); doegn=collections.Counter(); forekomst=collections.defaultdict(collections.Counter)
    for p in sorted(pathlib.Path(katalog).glob('*.xml')):
        sone = p.stem.rsplit('-',3)[0] if prefiks is None else prefiks
        try: root=ET.parse(p).getroot()
        except Exception: continue
        doegn[sone]+=1
        for ts in root.findall('g:TimeSeries',NS):
            m=ts.find('g:MktPSRType',NS)
            if m is None: continue
            typ=m.findtext('g:psrType','',NS)
            pr=m.find('g:PowerSystemResources',NS)
            eic=pr.findtext('g:mRID','',NS) if pr is not None else ''
            nm =pr.findtext('g:name','',NS) if pr is not None else ''
            if not eic: continue
            per[sone][eic].add(typ); navn[sone][eic]=nm; forekomst[sone][eic]+=1
    return per, navn, doegn, forekomst

if __name__=="__main__":
    import sys
    H=pathlib.Path(os.environ.get("PSRTYPE_DATA","./data-inn")).expanduser()
    res={}
    per,navn,doegn,fore = tell(H/"a75-avvik/a73-soner")
    pf,nf,df,ff = tell(H/"finland/anlegg/a73-raw", prefiks='FI')
    per.update(pf); navn.update(nf); doegn.update(df); fore.update(ff)
    print(f"{'sone':<10}{'døgn':>6}{'enheter':>9}{'>1 psrType':>12}   psrTyper i sonen")
    tot_e=tot_f=0
    for s in sorted(per):
        e=len(per[s]); f=sum(1 for v in per[s].values() if len(v)>1)
        tot_e+=e; tot_f+=f
        typer=sorted({t for v in per[s].values() for t in v})
        print(f"{s:<10}{doegn[s]:>6}{e:>9}{f:>12}   {', '.join(PSR.get(t,t) for t in typer)[:70]}")
        if f:
            for eic,v in per[s].items():
                if len(v)>1: print(f"      *** {navn[s][eic]} ({eic}): {sorted(PSR.get(t,t) for t in v)}")
    print(f"\n{'SUM':<10}{'':>6}{tot_e:>9}{tot_f:>12}")
    json.dump({s:{e:sorted(v) for e,v in d.items()} for s,d in per.items()},
              open(H/"a75-avvik/psrtype-per-enhet.json","w"), indent=0)
