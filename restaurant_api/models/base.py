"""Базовая модель."""

from sqlalchemy.orm import DeclarativeBase, declared_attr

from restaurant_api.utils import camel_case_to_snake_case


class Base(DeclarativeBase):
    """Базовый класс для декларативных моделей SQLAlchemy."""


class BaseModel(Base):
    """Абстрактная модель с общими свойствами для всех таблиц."""

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"

    def __repr__(self) -> str:
        id_val = getattr(self, "id", None)
        name_val = getattr(self, "name", None)
        return f"<{self.__class__.__name__} pk={id_val} | name: {name_val}>"
