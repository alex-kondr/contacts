from typing import Optional, List

from sqlalchemy import String, create_engine, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, relationship, declarative_base


engine = create_engine("sqlite:///students.db", echo=True)
Session = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)
Base = declarative_base()


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(50))
    bio: Mapped[Optional[str]] = mapped_column(String(500), default=None, nullable=True)
    classroom_id: Mapped[Optional[int]] = mapped_column(ForeignKey("classrooms.id", ondelete="CASCADE"), default=None, nullable=True)
    classroom: Mapped["ClassRoom"] = relationship(back_populates="students")


class ClassRoom(Base):
    __tablename__ = "classrooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[Optional[str]] = mapped_column(String(500), default=None, nullable=True)
    students: Mapped[List[Student]] = relationship(back_populates="classroom")


# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)


def get_db():
    with Session() as db:
        yield db
