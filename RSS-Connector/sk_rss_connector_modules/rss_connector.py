import time, json, feedparser
from sekoia_automation.connector import Connector
from sk_rss_connector_modules.models import SkRssConnectorConfiguration

class RssConnector(Connector):
    configuration: SkRssConnectorConfiguration

    def run(self) -> None:

        self.log("RSS Connector starting", level="info")

        while self.running:
            feed = feedparser.parse(self.configuration.feed_url)
            events = [] 
            for entry in feed.entries:
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

            time.sleep(self.configuration.frequency)
        
