from pydantic import BaseModel

class MTelegramAppData(BaseModel):
    title: str
    short_name: str
    api_id: int
    api_hash: str
    