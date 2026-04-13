from sk_pfsense_connector_modules import SkPfSenseConnectorModule

from sk_pfsense_connector_modules.pfsense_connector import PfSenseConnector


if __name__ == "__main__":
    module = SkPfSenseConnectorModule()
    module.register(PfSenseConnector, "PfSenseConnector")
    module.run()
