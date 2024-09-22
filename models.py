from sqlalchemy.orm import Mapped, mapped_column

from settings import Base


class Character(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    birth_year: Mapped[str]
    eye_color: Mapped[str]
    films: Mapped[str]
    gender: Mapped[str]
    hair_color: Mapped[str]
    height: Mapped[str]
    homeworld: Mapped[str]
    mass: Mapped[str]
    name: Mapped[str]
    skin_color: Mapped[str]
    species: Mapped[str]
    starships: Mapped[str]
    vehicles: Mapped[str]
