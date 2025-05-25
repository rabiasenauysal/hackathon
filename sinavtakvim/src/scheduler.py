# src/scheduler.py

import pandas as pd

def load_data(csv_path: str) -> pd.DataFrame:
    """Önceden işlenmiş CSV'i oku."""
    return pd.read_csv(csv_path)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    - Tamamen boş satır ve sütunları atar
    - Sütun adlarının baş/son boşluklarını siler
    - Boşlukları alt çizgiye çevirir, tamamını küçük harfe çevirir
    """
    # 1) Boş satırları ve sütunları çıkar
    df = df.dropna(axis=0, how='all').dropna(axis=1, how='all')
    
    # 2) Sütun adlarını normalize et
    df.columns = [
        col.strip()                  # baş/son boşluk sil
           .lower()                  # küçük harfe çevir
           .replace(' ', '_')        # boşluğu alt çizgiye çevir
        for col in df.columns
    ]
    
    # 3) Eğer gerekiyorsa, saat formatları vs. burda dönüştürülebilir
    #    Örnek: df['start_time'] = pd.to_datetime(df['start_time']).dt.time

    return df
