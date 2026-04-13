from sekoia_automation.module import Module
from sk_pfsense_connector_modules.models import SkPfSenseConnectorModuleConfiguration


class SkPfSenseConnectorModule(Module):
    configuration: SkPfSenseConnectorModuleConfiguration