import requests
from datetime import datetime, timedelta
import pytz

class NewsChamber:
    def __init__(self):
        self.url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
        
    def fetch_usd_high_impact(self):
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            events = response.json()
            
            critical_news = []
            now = datetime.utcnow()
            
            for event in events:
                if event.get('country') == 'USD' and event.get('impact') == 'High':
                    event_time = datetime.strptime(event['date'], "%Y-%m-%dT%H:%M:%S%z")
                    event_time_utc = event_time.astimezone(pytz.utc).replace(tzinfo=None)
                    
                    time_diff = event_time_utc - now
                    if timedelta(hours=0) <= time_diff <= timedelta(hours=12):
                        critical_news.append({
                            'title': event['title'],
                            'time_utc': event_time_utc.strftime("%Y-%m-%d %H:%M:%S"),
                            'hours_away': round(time_diff.total_seconds() / 3600, 2)
                        })
            return critical_news
        except Exception as e:
            return []

    def is_safe_to_trade(self, buffer_hours=1.0):
        upcoming_news = self.fetch_usd_high_impact()
        for news in upcoming_news:
            if news['hours_away'] <= buffer_hours:
                print(f"[ALERT] High Impact News Approaching: {news['title']} in {news['hours_away']} hrs.")
                return False
        return True
