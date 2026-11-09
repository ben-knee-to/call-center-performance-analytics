from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw/Call_Center.csv'
OUT = ROOT / 'data/processed/call_center_clean.csv'

def main():
    df = pd.read_csv(RAW)
    df.columns = (df.columns.str.strip().str.lower().str.replace(r'[^a-z0-9]+','_',regex=True).str.strip('_'))
    assert df['id'].notna().all(), 'Missing interaction IDs'
    assert not df['id'].duplicated().any(), 'Duplicate interaction IDs'
    df['call_timestamp'] = pd.to_datetime(df['call_timestamp'],format='%d-%m-%Y',errors='coerce')
    assert df['call_timestamp'].notna().all(), 'Unparseable call dates'
    df['call_duration_in_minutes'] = pd.to_numeric(df['call_duration_in_minutes'],errors='coerce')
    df['csat_score'] = pd.to_numeric(df['csat_score'],errors='coerce')
    assert df['call_duration_in_minutes'].ge(0).all(), 'Invalid durations'
    assert df['csat_score'].dropna().between(1,10).all(), 'CSAT outside 1–10'
    for col in ['call_centres_city','channel','city','customer_name','reason','response_time','sentiment','state']:
        df[col] = df[col].astype('string').str.strip()
    df['within_sla'] = df['response_time'].eq('Within SLA').astype(int)
    df['negative_sentiment'] = df['sentiment'].isin(['Negative','Very Negative']).astype(int)
    df['has_csat'] = df['csat_score'].notna().astype(int)
    df['day_of_week'] = df['call_timestamp'].dt.day_name()
    df['day'] = df['call_timestamp'].dt.day
    df['week_start'] = (df['call_timestamp']-pd.to_timedelta(df['call_timestamp'].dt.weekday,unit='D')).dt.date
    OUT.parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(OUT,index=False)
    print('Rows:',len(df),'Columns:',len(df.columns),'Missing CSAT:',df.csat_score.isna().sum())
    print('Saved:',OUT)
if __name__=='__main__': main()
