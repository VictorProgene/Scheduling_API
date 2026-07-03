from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.provider import Provider


class Service(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    duration_minutes: int

    provider_id: int = Field(foreign_key="provider.id")
    provider: "Provider" = Relationship(back_populates="services")
