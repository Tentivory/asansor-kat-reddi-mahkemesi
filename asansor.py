#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Asansör Kat Reddi Mahkemesi.

Kat talebini duruşmaya çıkarır, abartılı gerekçeyle kabul ya da ret verir.
Gerçekten çalışır. Asansör gerçekten çalışmaz.
"""

from __future__ import annotations

import argparse
import hashlib
import random
import sys
from dataclasses import dataclass


RET_GEREKCELERI = [
    "Kat, duruşmaya mazeretsiz gelmemiştir.",
    "Düğme parmak izi okunamadı, şüphe sürüyor.",
    "Bu kat bugün izinli, yerine zemin bakıyor.",
    "Kapı sensörü tanıklıktan çekildi.",
    "Talep, çay molasında yapıldığı için usulen geçersiz.",
    "Kat numarası tek, heyet çift gününde.",
    "Aciliyet beyanı market poşeti hukukuna aykırı.",
    "Asansör aynası sanığı tanımadı.",
]

KABUL_GEREKCELERI = [
    "Sanık kat, pişmanlık indirimi istedi ve lamba kırptı.",
    "Gerekçe yeterince absürt bulundu, kabul şart.",
    "Kapı bu sefer gerçekten kapanacakmış gibi yaptı.",
    "Heyet aç, hüküm hızlı çıktı.",
    "Zemin kat torpili reddedildi, eşitlik sağlandı.",
]


@dataclass
class Hukum:
    kat: int
    karar: str
    gerekce: str
    esas_no: str
    sure_saniye: int


def esas_no(kat: int, gerekce: str) -> str:
    ham = f"{kat}|{gerekce}".encode("utf-8")
    ozet = hashlib.sha256(ham).hexdigest()[:6].upper()
    return f"2026/ASANSOR-{kat}-{ozet}"


def yargila(kat: int, gerekce: str, acele: str) -> Hukum:
    if kat < -2 or kat > 40:
        return Hukum(
            kat=kat,
            karar="GÖREVSİZLİK",
            gerekce="Bu kat binada yok. Hayal mahkemesi başka repo.",
            esas_no=esas_no(kat, gerekce),
            sure_saniye=0,
        )
    if kat == 13:
        return Hukum(
            kat=13,
            karar="RET",
            gerekce="On üçüncü kat dosyası kapalıdır. Bina onu yok saymayı tercih etti.",
            esas_no=esas_no(kat, gerekce),
            sure_saniye=13,
        )
    tohum = int(hashlib.md5(f"{kat}:{gerekce}:{acele}".encode()).hexdigest()[:8], 16)
    random.seed(tohum)
    bonus = 0
    if acele == "evet" and "anne" in gerekce.lower():
        bonus = 40
    if acele == "belki":
        bonus = -15
    puan = (tohum % 100) + bonus
    if puan >= 55:
        karar = "KABUL"
        sebep = random.choice(KABUL_GEREKCELERI)
        sure = random.randint(4, 18)
    else:
        karar = "RET"
        sebep = random.choice(RET_GEREKCELERI)
        sure = random.randint(20, 90)
    return Hukum(kat=kat, karar=karar, gerekce=sebep, esas_no=esas_no(kat, gerekce), sure_saniye=sure)


def bas(h: Hukum, kullanici_gerekce: str) -> None:
    cizgi = "=" * 52
    print(cizgi)
    print(" ASANSÖR KAT REDDİ MAHKEMESİ")
    print(f" Esas No: {h.esas_no}")
    print(cizgi)
    print(f" Sanık kat     : {h.kat}")
    print(f" Beyan         : {kullanici_gerekce}")
    print(f" Karar         : {h.karar}")
    print(f" Gerekçe       : {h.gerekce}")
    if h.karar == "KABUL":
        print(f" Tahmini varış : {h.sure_saniye} saniye (kapı sözüne güvenilmez)")
        print(" Hüküm: Düğme yanabilir. Sevinç yasaktır, sadece binilir.")
    elif h.karar == "RET":
        print(f" Bekleme cezası: {h.sure_saniye} saniye merdivene bakma")
        print(" Hüküm: Kat reddedildi. İtiraz merdivendedir.")
    else:
        print(" Hüküm: Dava binanın yetki alanı dışında.")
    print(cizgi)
    print(" Damga: 3 Ekim 2026 | Kayyum Grok | ~islak-bardak~")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Kat talebini mahkemeye sevk eder.")
    p.add_argument("--kat", type=int, required=True, help="Talep edilen kat")
    p.add_argument("--gerekce", default="canım istedi", help="Neden bu kat")
    p.add_argument("--acele", choices=["evet", "hayir", "belki"], default="hayir")
    a = p.parse_args(argv)
    hukum = yargila(a.kat, a.gerekce, a.acele)
    bas(hukum, a.gerekce)
    return 0 if hukum.karar != "GÖREVSİZLİK" else 2


if __name__ == "__main__":
    sys.exit(main())
