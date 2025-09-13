from pydantic import BaseModel, HttpUrl


class LinkCreate(BaseModel):
    original_url: HttpUrl


class Link(BaseModel):
    id: int
    short_url: str
    original_url: HttpUrl
    visit_count: int

    class Config:
        from_attributes = True
