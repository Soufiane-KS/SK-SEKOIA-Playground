import time, json, feedparser
from sekoia_automation.connector import Connector
from sk_rss_connector_modules.models import SkRssConnectorConfiguration

class RssConnector(Connector):
    configuration: SkRssConnectorConfiguration

    def run(self) -> None:
        self.log("RSS Connector starting", level="info")
        while self.running:
            self._fetch_and_push()
            time.sleep(self.configuration.frequency)

    def _fetch_and_push(self) -> None:
        feed = feedparser.parse(self.configuration.feed_url)
        events = []
        last_checkpoint = self.get_last_checkpoint()
        latest_date = last_checkpoint


        for entry in feed.entries:
            published = entry.get("published_parsed")
            if not published:
                continue
            else:
                if last_checkpoint and published <= last_checkpoint:
                    continue
                else:
                    if latest_date is None or published > latest_date:
                        latest_date = published
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
            self.set_last_checkpoint(latest_date)
