from unittest.mock import patch, MagicMock
from sk_rss_connector_modules.rss_connector import RssConnector
from sk_rss_connector_modules.models import SkRssConnectorConfiguration

def test_rss_connector_pushes_events():
    fake_feed = MagicMock()
    fake_feed.entries = [
        MagicMock(title="Test Article",
                  link="http://example.com/test-article",
                  get=lambda key, default="": {"published": "Mon, 06 Apr 2026", "summary": "Test description"}.get(key, default)
                )
    ]

    with patch("feedparser.parse", return_value=fake_feed):
        with patch.object(RssConnector, "push_events_to_intakes") as mock_push:
            connector = RssConnector()
            connector.configuration = SkRssConnectorConfiguration(
                feed_url="http://example.com/feed", 
                frequency=300
                )
            connector._fetch_and_push()
            mock_push.assert_called_once()