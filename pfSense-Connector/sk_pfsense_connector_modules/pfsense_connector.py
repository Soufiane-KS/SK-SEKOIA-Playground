import queue, threading
from sekoia_automation.connector import Connector
from sk_pfsense_connector_modules.models import PfSenseConnectorConfiguration
from sk_pfsense_connector_modules.syslog_receiver import SyslogReceiver

class PfSenseConnector(Connector):
    configuration: PfSenseConnectorConfiguration

    def run(self) -> None:
        self.log("pfSense Connector starting", level="info")
        self._event_queue = queue.Queue()
        self._stop_event = threading.Event()
        self._syslog_receiver = SyslogReceiver(
            port=self.configuration.listen_port,
            queue=self._event_queue,
            logger=self.log,
            stop_event=self._stop_event
        )

        self._syslog_receiver.start()
        events = []   
        while self.running:
            try:
                event = self._event_queue.get(timeout=1)
                events.append(event)
                if len(events) >= self.configuration.batch_size: 
                    self.push_events_to_intakes(events=events)
                    events = []
            except queue.Empty:
                continue
            except Exception as e:
                self.log(f"Error processing event: {e}", level="error")

        self._stop_event.set()
        self._syslog_receiver.join()