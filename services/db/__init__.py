from .session import DBSession


__all__ = (
    "DBSession",
)


def create_all_tables() -> None:
    from .models import Base
    from .base import ENGINE

    Base.metadata.create_all(ENGINE)
