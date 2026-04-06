from pydantic.v1 import BaseModel, Field


class SkRssConnectorModuleConfiguration(BaseModel):
    pass 


class SkRssConnectorConfiguration(BaseModel):
    feed_url: str = Field(..., description="URL of the RSS feed to poll")
    frequency: int = Field(300, description="Polling frequency in seconds")
