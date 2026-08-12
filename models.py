from database import Base
from sqlalchemy.orm import mapped_column, Mapped

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    hashed_password: Mapped[str]



