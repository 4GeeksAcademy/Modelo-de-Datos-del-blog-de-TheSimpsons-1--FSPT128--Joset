from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship 

db = SQLAlchemy()

favs_characters_table = Table(
    "favs_characters",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("character_id", ForeignKey("character.id"), primary_key=True)
)

favs_locations_table = Table(
    "favs_locations",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("location_id", ForeignKey("location.id"), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    favs_characters: Mapped[list["Character"]] = relationship(
        "Character",
        secondary=favs_characters_table,
        back_populates="favorited_by"
    )
    favs_locations: Mapped[list["Location"]] = relationship(
        "Location",
        secondary=favs_locations_table,
        back_populates="favorited_by"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites": self.favorites
            # do not serialize the password, its a security breach
        }
    
class Character(db.Model):
    __tablename__ = 'character'
    id: Mapped[int] = mapped_column(primary_key=True)
    age: Mapped[int] = mapped_column(nullable=True) 
    name: Mapped[str] = mapped_column(String(120), nullable=False) 
    image: Mapped[str] = mapped_column(String(120), nullable=True)
    birthdate: Mapped[str] = mapped_column(String(15), nullable=True) 
    gender: Mapped[str] = mapped_column(String(10), nullable=False) 
    occupation: Mapped[str] = mapped_column(String(120), nullable=False) 
    phrases: Mapped[str] = mapped_column(String(200), nullable=True) 

    favorited_by: Mapped[list["User"]] = relationship(
        "User",
        secondary=favs_characters_table,
        back_populates="favs_characters"
    )

    def serialize(self):
        return {
            "id": self.id,
            "age": self.age,
            "name": self.name,
            "image": self.image,
            "birthdate": self.birthdate,
            "gender": self.gender,
            "occupation": self.occupation,
            "phrases": self.phrases,
        }

class Location (db.Model):
    __tablename__ = 'location'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False) 
    image: Mapped[str] = mapped_column(String(120), nullable=True)
    town: Mapped[str] = mapped_column(String(120), nullable=False)
    use: Mapped[str] = mapped_column(String(120), nullable=False)

    favorited_by: Mapped[list["User"]] = relationship(
        "User",
        secondary=favs_locations_table,
        back_populates="favs_locations"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "town": self.town,
            "use": self.use,
        }
