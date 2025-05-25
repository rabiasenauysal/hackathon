"""
exam_scheduler.py
─────────────────
• Öğrenci listesi  (.xlsx)
• Salon-kapasite   (.xlsx / .xls / .docx-tablolu → Excel’e dönüştürülmüş)
dosyalarını okuyup kural setine göre sınav takvimi üretir ve Excel’e kaydeder.
"""

from datetime import datetime, timedelta
import pandas as pd
from unidecode import unidecode   # pip install unidecode


# ────────────────────────────────────────────────────────────────────────────────
# 1) GİRDİ DOSYALARINI OKUMA
# ────────────────────────────────────────────────────────────────────────────────
def read_input_files(ogrenci_file: str, salon_file: str):
    """
    Parametreler
    ------------
    ogrenci_file : str
        "DersBazliOgrenciSayisi*.xlsx" benzeri dosya yolu
    salon_file   : str
        Sınıf & kapasite tablosu (.xlsx/.xls). Başlıklar farklı olabilir:
        • SINIF – KAPASİTE
        • SALON KODU – KAPASITE
        • vs.

    Dönüş
    -----
    ogrenci_df, salon_df : pandas.DataFrame
    """
    # ── Öğrenci tablosu
    ogrenci_df = pd.read_excel(ogrenci_file)

    # ── Salon tablosu
    salon_df = pd.read_excel(salon_file)

    # Başlıkları normalize et → ASCII + büyük harf
    salon_df.columns = [unidecode(str(c)).strip().upper() for c in salon_df.columns]

    # Olası başlıkları tek forma indir
    rename_map = {}
    for col in salon_df.columns:
        if col in {"SALON ADI", "SINIF", "SALON KODU"}:
            rename_map[col] = "SALON"
        elif col in {"KAPASITE", "KAPASITI", "KAPASITESI"}:  # İ / İ̇ varyasyonları
            rename_map[col] = "KAPASITE"
    salon_df.rename(columns=rename_map, inplace=True)

    # Gerekli iki sütun var mı?
    if not {"SALON", "KAPASITE"} <= set(salon_df.columns):
        raise ValueError(
            "Salon tablosunda 'SALON' ve 'KAPASITE' sütunları bulunamadı! "
            f"Mevcut sütunlar: {list(salon_df.columns)}"
        )

    # Kapasite → tam sayı
    salon_df["KAPASITE"] = pd.to_numeric(salon_df["KAPASITE"], errors="coerce").fillna(0).astype(int)

    return ogrenci_df, salon_df


# ────────────────────────────────────────────────────────────────────────────────
# 2) YARDIMCI FONKSİYONLAR
# ────────────────────────────────────────────────────────────────────────────────
def get_exam_days(start_date: str, end_date: str, include_weekends: bool = True):
    """Sınav yapılacak günlerin pandas.Timestamp listesi"""
    days = pd.date_range(start=start_date, end=end_date, freq="D")
    if not include_weekends:
        days = [d for d in days if d.weekday() < 5]  # 0-4 ⇒ Pzt-Cum
    return days


def find_suitable_salon(
    ogr_sayisi: int,
    salon_df: pd.DataFrame,
    busy_salons: set,
    tarih: str,
    saat: int,
):
    """Yeterli kapasiteli ve o anda boş bir salon döndürür (yoksa None)."""
    for _, salon in salon_df.iterrows():
        salon_adi = str(salon["SALON"])
        kapasite  = int(salon["KAPASITE"])
        if kapasite >= ogr_sayisi and (salon_adi, tarih, saat) not in busy_salons:
            return salon_adi
    return None


# ────────────────────────────────────────────────────────────────────────────────
# 3) ANA YERLEŞTİRME ALGORİTMASI   (Basit sürüm)
# ────────────────────────────────────────────────────────────────────────────────
def assign_exams(
    ogrenci_df: pd.DataFrame,
    salon_df: pd.DataFrame,
    *,
    start_date="2025-06-01",
    end_date="2025-06-14",
    slot_hours=(9, 12, 15),
    slot_duration=2,
    max_daily_exams=2,
    include_weekends=True,
):
    """
    Öğrenci ve salon verilerine göre sınav takvimi üretir (çok temel kurallar).

    Gelişmiş kurallar (seçmeli+zorunlu çakışma, öğrenci başına max 2 sınav vb.)
    örnek olması için MINİMAL tutuldu — detaylı optimizasyon eklemek serbest.
    """
    exam_days      = get_exam_days(start_date, end_date, include_weekends)
    takvim_kayit   = []
    busy_salons    = set()  # (salon, tarih, saat)

    # Basit sıra algoritması: her dersi sırayla yerleştir
    for idx, ders in ogrenci_df.iterrows():
        ders_kodu  = ders.get("Ders Kodu", ders.get("Ders", f"Ders_{idx+1}"))
        ogr_sayisi = int(ders.get("Mevcut", ders.get("Öğrenci Sayısı", 0)))
        yerlestirildi = False

        for gun in exam_days:
            g_str = gun.strftime("%Y-%m-%d")
            for saat in slot_hours:
                salon_adi = find_suitable_salon(ogr_sayisi, salon_df, busy_salons, g_str, saat)
                if salon_adi:
                    takvim_kayit.append(
                        {
                            "Ders":  ders_kodu,
                            "Salon": salon_adi,
                            "Tarih": g_str,
                            "Saat":  f"{saat:02d}:00-{saat+slot_duration:02d}:00",
                        }
                    )
                    busy_salons.add((salon_adi, g_str, saat))
                    yerlestirildi = True
                    break
            if yerlestirildi:
                break

        if not yerlestirildi:  # hiçbir yere sığmadı
            takvim_kayit.append(
                {
                    "Ders":  ders_kodu,
                    "Salon": "SALON BULUNAMADI",
                    "Tarih": "YERLEŞTİRİLEMEDİ",
                    "Saat":  "",
                }
            )

    return pd.DataFrame(takvim_kayit)


# ────────────────────────────────────────────────────────────────────────────────
# 4) ÇIKTI
# ────────────────────────────────────────────────────────────────────────────────
def save_schedule(takvim_df: pd.DataFrame, output_excel="sinav_takvimi.xlsx"):
    """Takvimi Excel dosyasına kaydet."""
    takvim_df.to_excel(output_excel, index=False)
    print(f"[✓] Sınav takvimi kaydedildi →  {output_excel}")


# ────────────────────────────────────────────────────────────────────────────────
# 5) HIZLI TEST (python exam_scheduler.py)
# ────────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    ogrenci_file = r"C:\Users\uysal\OneDrive\Desktop\projects\sinavtakvim\data\raw\DersBazliOgrenciSayisi2025Bahar.xlsx"
    salon_file   = r"C:\Users\uysal\OneDrive\Desktop\projects\sinavtakvim\data\raw\salon_kapasite_tablosu.xlsx"

    ogrenci_df, salon_df = read_input_files(ogrenci_file, salon_file)

    takvim_df = assign_exams(
        ogrenci_df,
        salon_df,
        start_date="2025-06-01",
        end_date="2025-06-14",
        slot_hours=(9, 12, 15),
        include_weekends=True,
    )

    save_schedule(takvim_df)
