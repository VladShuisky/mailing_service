from typing import Optional
from datetime import datetime

from sqlmodel import Field, SQLModel, create_engine, Session, UniqueConstraint, select
import sqlalchemy

from settings import DB_URL



class VkManagerAccountBase(SQLModel):
    __tablename__ = "managers_accounts"

    vk_id: str
    city_id: Optional[int] = Field(default=None, foreign_key='cities.id')
    token: str = None
    last_activity: datetime = Field(
        default=None,
        sa_column=sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), nullable=True)
    )

    __table_args__ = (
        UniqueConstraint('vk_id'),
    ) #Уникальные поля

class VkUsersBase(SQLModel):
    __tablename__ = "vk_users"

    vk_id: str
    screen_name: str = None
    city_id: Optional[int] = Field(default=None, foreign_key='cities.id')
    status: int = None
    manager_id: Optional[int] = Field(default=None, foreign_key='managers_accounts.id')
    last_seen: datetime = Field(
        default=None,
        sa_column=sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), nullable=True)
    )

    __table_args__ = (
        UniqueConstraint('vk_id'),
    )

class CityBase(SQLModel):
    __tablename__ = "cities"

    name: str

    __table_args__ = (
        UniqueConstraint('name'),
    )

class VkManagerAccount(VkManagerAccountBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class VkUsers(VkUsersBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class City(CityBase, table=True):
    id: int | None = Field(default=None, primary_key=True)




















