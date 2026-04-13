from pydantic.v1 import BaseModel, Field

class SkPfSenseConnectorModuleConfiguration(BaseModel):
    pass


class PfSenseConnectorConfiguration(BaseModel):
    listen_port: int = Field(514, description="Port on which the connector will listen for incoming pfSense logs")
    intake_key: str = Field(..., description="Intake key to use when sending events")
    intake_server: str = Field("https://intake.sekoia.io", description="Intake server URL")
    batch_size: int = Field(50, description="Number of events to batch before sending to intake")