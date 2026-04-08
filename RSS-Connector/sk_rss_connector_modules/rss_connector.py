import time
import json
import feedparser
from sekoia_automation.connector import Connector
from sk_rss_connector_modules.models import SkRssConnectorConfiguration


class RssConnector(Connector):
    configuration: SkRssConnectorConfiguration

    def run(self) -> None:
        self.log("RSS Connector starting", level="info")

        while self.running:
            try:
                self._fetch_and_push()
            except Exception as e:
                self.log(f"Error during fetch: {e}", level="error")
            time.sleep(self.configuration.frequency)

    def _fetch_and_push(self) -> None:
        self.log("Fetching feed...", level="info")
        feed = feedparser.parse(self.configuration.feed_url)
        self.log(f"Feed fetched, {len(feed.entries)} entries found", level="info")
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
        else:
            self.log("No events to push", level="info")
