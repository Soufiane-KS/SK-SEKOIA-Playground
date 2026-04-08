import time, json, feedparser
from datetime import datetime, timezone
from sekoia_automation.connector import Connector
from sekoia_automation.checkpoint import CheckpointDatetime
from sk_rss_connector_modules.models import SkRssConnectorConfiguration

class RssConnector(Connector):
    configuration: SkRssConnectorConfiguration

    def run(self) -> None:
        self.log("RSS Connector starting", level="info")

        self._checkpoint = CheckpointDatetime(path=self.data_path)

        while self.running:
            self._fetch_and_push()
            time.sleep(self.configuration.frequency)

    def _fetch_and_push(self) -> None:
        feed = feedparser.parse(self.configuration.feed_url)
        events = []
        last_checkpoint = self._checkpoint.offset
        latest_date = None


        for entry in feed.entries:
            published = entry.get("published_parsed")
            if not published:
                continue
            published_dt = datetime(*published[:6], tzinfo=timezone.utc)
            if published_dt <= last_checkpoint:
                continue
            if latest_date is None or published_dt > latest_date:
                latest_date = published_dt
            event = json.dumps({
                "title": entry.title,
                "link": entry.link,
                "published": entry.get("published", ""),
                "description": entry.get("summary", "")      
            })
            events.append(event)


        if events:
            self.log(f"Pushing {len(events)} events", level="info")
            self.push_events_to_intakes(events=events)
            self._checkpoint.offset = latest_date
