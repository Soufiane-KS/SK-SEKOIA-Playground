from sk_rss_connector_modules import SkRssConnectorModule
from sk_rss_connector_modules.rss_connector import RssConnector


if __name__ == "__main__":
    module = SkRssConnectorModule()
    module.register(RssConnector, "RssConnector")
    module.run()
