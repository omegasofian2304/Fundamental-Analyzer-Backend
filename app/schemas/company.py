from pydantic import BaseModel, ConfigDict


class Company(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # pydantic can't read objects without the option from_attributes

    ticker: str
    name: str | None = None  # name can be None
