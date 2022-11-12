from typing import Optional

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import (
    make_url,
    create_engine,
    Engine,
)


Base = declarative_base()


ENGINE: Optional[Engine] = None


def create_pool(db_path: str) -> sessionmaker:
    global ENGINE
    ENGINE = create_engine(url=make_url("sqlite:///" + db_path), future=True)

    # expire_on_commit=False will prevent attributes from being expired
    # after commit.
    pool = sessionmaker(bind=ENGINE, expire_on_commit=False)

    return pool
