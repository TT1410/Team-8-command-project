from sqlalchemy.orm import sessionmaker

from config import DB_PATH
from .base import create_pool


class DBSession:
    db_session: sessionmaker = create_pool(DB_PATH)
