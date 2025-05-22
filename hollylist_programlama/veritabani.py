# veritabani.py

import csv
import os
import re

CSV_KULLANICI = os.path.join(os.path.dirname(__file__), "kullanicilar.csv")
CSV_DIZIFILM = os.path.join(os.path.dirname(__file__), "dizifilm.csv")
EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

def kullanicilari_oku():
    if not os.path.exists(CSV_KULLANICI):
        print(f"CSV dosyası bulunamadı: {CSV_KULLANICI}")  # Debug
        return []
    with open(CSV_KULLANICI, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        kullanicilar = list(reader)
        print(f"Okunan Kullanıcılar: {kullanicilar}")  # Debug
        return kullanicilar

def kullanicilari_yaz(kullanicilar):
    alanlar = ["adSoyad", "kullaniciAdi", "email", "sifre"]
    with open(CSV_KULLANICI, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=alanlar)
        writer.writeheader()
        for k in kullanicilar:
            writer.writerow(k)
    print(f"Kullanıcılar yazıldı: {kullanicilar}")  # Debug

def eposta_mevcut_mu(email):
    for k in kullanicilari_oku():
        if k["email"].strip().lower() == email.strip().lower():
            print(f"E-posta mevcut: {email}")  # Debug
            return True
    return False

def kullaniciadi_mevcut_mu(kullaniciAdi):
    for k in kullanicilari_oku():
        if k["kullaniciAdi"].strip().lower() == kullaniciAdi.strip().lower():
            print(f"Kullanıcı adı mevcut: {kullaniciAdi}")  # Debug
            return True
    return False

def eposta_gecerli_mi(email):
    return bool(EMAIL_REGEX.match(email))

def sifre_uygun_mu(sifre):
    return 8 <= len(sifre) <= 12

def kullanici_ekle(adSoyad, kullaniciAdi, email, sifre):
    kullanicilar = kullanicilari_oku()
    kullanicilar.append({
        "adSoyad": adSoyad,
        "kullaniciAdi": kullaniciAdi,
        "email": email,
        "sifre": sifre
    })
    kullanicilari_yaz(kullanicilar)
    print(f"Kullanıcı eklendi: {adSoyad}, {kullaniciAdi}, {email}, {sifre}")  # Debug

def giris_kontrol(kullaniciAdi, sifre):
    kayitlar = kullanicilari_oku()
    for k in kayitlar:
        if k["kullaniciAdi"].strip().lower() == kullaniciAdi.strip().lower():
            if k["sifre"] == sifre:
                print("Giriş kontrolü: OK")  # Debug
                return "OK"
            else:
                print("Giriş kontrolü: HATALI_SIFRE")  # Debug
                return "HATALI_SIFRE"
    print("Giriş kontrolü: BULUNAMADI")  # Debug
    return "BULUNAMADI"

def kayitlari_oku(kullaniciAdi, durum=None):
    kayitlar = []
    if not os.path.exists(CSV_DIZIFILM):
        print(f"Dizi/Film CSV dosyası bulunamadı: {CSV_DIZIFILM}")  # Debug
        return kayitlar

    with open(CSV_DIZIFILM, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for satir in reader:
            if satir["kullaniciAdi"].strip().lower() != kullaniciAdi.strip().lower():
                continue
            if durum and satir["Durum"].strip().lower() != durum.strip().lower():
                continue
            try:
                satir["Puan"] = int(satir["Puan"])
            except:
                satir["Puan"] = 0
            kayitlar.append(satir)
    print(f"Okunan Kayitlar: {kayitlar}")  # Debug
    return kayitlar

def turleri_oku_csv(csv_tur_dosyasi="tur.csv"):
    turler = []
    csv_tur_dosyasi = os.path.join(os.path.dirname(__file__), csv_tur_dosyasi)
    if os.path.exists(csv_tur_dosyasi):
        with open(csv_tur_dosyasi, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            first_line = True
            for row in reader:
                if first_line:
                    # başlık satırı "Tür" vs. atla
                    first_line = False
                    continue
                if row:
                    turler.append(row[0].strip())
    print(f"Okunan Türler: {turler}")  # Debug
    return turler

def kayit_guncelle(kayit, csv_dosyasi=CSV_DIZIFILM):
    kayitlar = []
    kayit_guncellendi = False

    if os.path.exists(csv_dosyasi):
        with open(csv_dosyasi, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                if (r["kullaniciAdi"].strip().lower() == kayit["kullaniciAdi"].strip().lower() and
                    r["Ad"].strip().lower() == kayit["Ad"].strip().lower()):
                    r.update(kayit)
                    try:
                        r["Puan"] = int(kayit["Puan"])
                    except ValueError:
                        r["Puan"] = 0
                    kayit_guncellendi = True
                    print(f"Kayit güncellendi: {r}")  # Debug
                else:
                    try:
                        r["Puan"] = int(r["Puan"])
                    except ValueError:
                        r["Puan"] = 0
                kayitlar.append(r)

    if not kayit_guncellendi:
        try:
            kayit["Puan"] = int(kayit["Puan"])
        except ValueError:
            kayit["Puan"] = 0
        kayitlar.append(kayit)
        print(f"Yeni kayit eklendi: {kayit}")  # Debug

    alanlar = ["kullaniciAdi", "Dizi/Film", "Tür", "Ad", "İlerleme", "Puan", "Not", "Durum", "Afiş"]
    with open(csv_dosyasi, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=alanlar)
        writer.writeheader()
        for r in kayitlar:
            r["Puan"] = str(r["Puan"])
            writer.writerow(r)
    print(f"Kayıtlar güncellendi: {kayitlar}")  # Debug

def kayit_var_mi(kullaniciAdi, ad, csv_dosyasi=CSV_DIZIFILM):
    if not os.path.exists(csv_dosyasi):
        print(f"Dizi/Film CSV dosyası bulunamadı: {csv_dosyasi}")  # Debug
        return False

    with open(csv_dosyasi, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for satir in reader:
            if (satir["kullaniciAdi"].strip().lower() == kullaniciAdi.strip().lower() and
                satir["Ad"].strip().lower() == ad.strip().lower()):
                print(f"Kayit var: {satir}")  # Debug
                return True
    return False

def kayit_ekle(kayit, csv_dosyasi=CSV_DIZIFILM):
    alanlar = ["kullaniciAdi", "Dizi/Film", "Tür", "Ad", "İlerleme", "Puan", "Not", "Durum", "Afiş"]
    csv_dosyasi = os.path.join(os.path.dirname(__file__), csv_dosyasi)
    dosya_var_mi = os.path.exists(csv_dosyasi)

    with open(csv_dosyasi, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=alanlar)
        if not dosya_var_mi:
            writer.writeheader()
        writer.writerow(kayit)
    print(f"Kayit eklendi: {kayit}")  # Debug

def kullanici_bilgilerini_oku(kullaniciAdi):
    kullanicilar = kullanicilari_oku()
    print(f"Aranan Kullanıcı Adı: '{kullaniciAdi}'")  # Debug
    for kullanici in kullanicilar:
        print(f"Kontrol Edilen Kullanıcı: {kullanici}")  # Debug
        if kullanici["kullaniciAdi"].strip().lower() == kullaniciAdi.strip().lower():
            print("Kullanıcı bulundu.")  # Debug
            return kullanici
    print("Kullanıcı bulunamadı.")  # Debug
    return None

def kullanici_bilgilerini_guncelle(eski_kullaniciAdi, yeni_bilgiler):
    kullanicilar = kullanicilari_oku()
    guncellendi = False
    for kullanici in kullanicilar:
        if kullanici["kullaniciAdi"].strip().lower() == eski_kullaniciAdi.strip().lower():
            kullanici.update(yeni_bilgiler)
            guncellendi = True
            break
    if guncellendi:
        kullanicilari_yaz(kullanicilar)
        return True
    return False

def kullanici_sil(kullaniciAdi):
    kullanicilar = kullanicilari_oku()
    kullanicilar = [kullanici for kullanici in kullanicilar if kullanici["kullaniciAdi"].strip().lower() != kullaniciAdi.strip().lower()]
    kullanicilari_yaz(kullanicilar)
    return True
