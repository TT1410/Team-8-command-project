from .session import DBSession


def create_all_tables() -> None:
    from .models import Base
    from .base import ENGINE

    Base.metadata.create_all(ENGINE)


__all__ = (
    "DBSession",
    "create_all_tables",
)
