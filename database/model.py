from sqlalchemy import TEXT, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from .manager import manager


class Author(manager.Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(35), nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String)
    posts: Mapped[list['Post']] = relationship(back_populates='author', lazy='selectin')

    def __repr__(self) -> str:
        return f'<Author {self.name}>'


class Post(manager.Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(60), nullable=False)
    text = Column(TEXT)

    author_id = Column(Integer, ForeignKey('author.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    author: Mapped[Author] = relationship(back_populates='posts', lazy='selectin')

    def __repr__(self) -> str:
        return f'<Post {self.title[:7]}>'


class User(manager.Base):
    __tablename__ = 'user'

    name = Column(String(30), nullable=False, primary_key=True)
    hashed_password = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f'<Post {self.name}>'
    