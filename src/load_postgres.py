"""Load the Step 2 cleaned CSV into PostgreSQL. Run SQL scripts 01 and 02 separately."""
import os
from pathlib import Path
import psycopg
from dotenv import load_dotenv
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / '.env')
CSV = ROOT / 'data' / 'processed' / 'call_center_clean.csv'

def main():
    if not CSV.exists():
        raise FileNotFoundError(f'Missing {CSV}; run clean_data.py first')
    dsn = os.getenv('DATABASE_URL')
    if not dsn:
        raise RuntimeError('Set DATABASE_URL in your local .env file')
    with psycopg.connect(dsn) as conn:
        with conn.cursor() as cur:
            cur.execute('TRUNCATE TABLE staging.call_center')
            with cur.copy("COPY staging.call_center FROM STDIN WITH (FORMAT CSV, HEADER TRUE, NULL '')") as copy:
                with CSV.open('rb') as f:
                    while chunk := f.read(1024 * 1024):
                        copy.write(chunk)
            cur.execute('SELECT COUNT(*) FROM staging.call_center')
            print('Loaded rows:', cur.fetchone()[0])
    print('Import committed successfully')

if __name__ == '__main__':
    main()
