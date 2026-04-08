import time
import json
import feedparser
from datetime import datetime, timezone
from sekoia_automation.connector import Connector
from sk_rss_connector_modules.models import SkRssConnectorConfiguration


class RssConnector(Connector):
    configuration: SkRssConnectorConfiguration

    def run(self) -> None:
        self.log("RSS Connector starting", level="info")
        self._last_seen = None

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
        latest_date = self._last_seen

        for entry in feed.entries:
            published = entry.get("published_parsed")
            if not published:
                continue
            published_dt = datetime(*published[:6], tzinfo=timezone.utc)

            if self._last_seen and published_dt <= self._last_seen:
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
            self._last_seen = latest_date
        else:
            self.log("No new events to push", level="info")
