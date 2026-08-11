from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column

from config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)

Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass


