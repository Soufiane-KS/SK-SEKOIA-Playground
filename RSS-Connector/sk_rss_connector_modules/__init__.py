from sekoia_automation.module import Module
from sk_rss_connector_modules.models import SkRssConnectorModuleConfiguration


class SkRssConnectorModule(Module):
    configuration: SkRssConnectorModuleConfiguration
