from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parents[1]
TABLES = ROOT/'outputs/tables'; CHARTS=ROOT/'outputs/charts'
TABLES.mkdir(parents=True,exist_ok=True); CHARTS.mkdir(parents=True,exist_ok=True)
df = pd.read_csv(ROOT/'data/processed/call_center_clean.csv',parse_dates=['call_timestamp'])

def grouped(field):
    t = df.groupby(field,dropna=False).agg(
        contacts=('id','nunique'),average_duration_minutes=('call_duration_in_minutes','mean'),
        average_csat=('csat_score','mean'),csat_responses=('has_csat','sum'),
        csat_response_rate=('has_csat','mean'),within_sla_rate=('within_sla','mean'),
        negative_sentiment_rate=('negative_sentiment','mean')).reset_index()
    t['contact_share'] = t['contacts']/len(df)
    t.to_csv(TABLES/f'by_{field}.csv',index=False)
    return t
for field in ['call_centres_city','channel','reason','sentiment','response_time','state','day_of_week']:
    grouped(field)
daily = grouped('call_timestamp').sort_values('call_timestamp')
summary = pd.DataFrame([{
    'total_contacts':len(df),'average_duration_minutes':df.call_duration_in_minutes.mean(),
    'average_csat':df.csat_score.mean(),'csat_responses':int(df.has_csat.sum()),
    'csat_response_rate':df.has_csat.mean(),'within_sla_rate':df.within_sla.mean(),
    'negative_sentiment_rate':df.negative_sentiment.mean(),
    'missing_csat':int(df.csat_score.isna().sum())}])
summary.to_csv(TABLES/'overall_kpis.csv',index=False)

def bar(field, metric, filename, title):
    t=pd.read_csv(TABLES/f'by_{field}.csv').sort_values(metric)
    fig,ax=plt.subplots(figsize=(10,5))
    ax.barh(t[field].astype(str),t[metric]);ax.set_title(title);ax.set_xlabel(metric.replace('_',' ').title())
    fig.tight_layout();fig.savefig(CHARTS/filename,dpi=160);plt.close(fig)
bar('channel','contacts','contacts_by_channel.png','Contacts by Channel')
bar('call_centres_city','average_csat','csat_by_centre.png','Average CSAT by Centre (Scored Contacts Only)')
bar('call_centres_city','within_sla_rate','sla_by_centre.png','Within-SLA Share by Centre')
bar('reason','contacts','contacts_by_reason.png','Contacts by Reason')
bar('sentiment','contacts','sentiment_distribution.png','Contacts by Sentiment')
fig,ax=plt.subplots(figsize=(10,5));ax.plot(daily.call_timestamp,daily.contacts,marker='o',markersize=3)
ax.set_title('Daily Contact Volume');ax.set_ylabel('Contacts');fig.autofmt_xdate();fig.tight_layout()
fig.savefig(CHARTS/'daily_contacts.png',dpi=160);plt.close(fig)
print('\nOVERALL KPIs\n',summary.to_string(index=False))
print('\nBY CENTRE\n',pd.read_csv(TABLES/'by_call_centres_city.csv').to_string(index=False))
print('\nBY CHANNEL\n',pd.read_csv(TABLES/'by_channel.csv').to_string(index=False))
print('\nSaved tables to',TABLES,'and charts to',CHARTS)
