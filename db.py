import uuid

from sqlalchemy import Column, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects import postgresql


engine = create_engine(
    'postgresql://postgres:12345@postgres_db:5432/restaurant',
    echo=True)

Session = sessionmaker(bind=engine)
Base = declarative_base()


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    submenus = relationship('Submenu', back_populates='menu', cascade='all, delete-orphan')


class Submenu(Base):
    __tablename__ = 'submenus'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    menu = relationship('Menu', back_populates='submenus')
    menu_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('menus.id', ondelete='CASCADE'), nullable=False)
    dishes = relationship('Dish', back_populates='submenu', cascade='all, delete-orphan')


class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(DECIMAL(precision=2), nullable=False)
    submenu_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('submenus.id', ondelete='CASCADE'), nullable=False)
    submenu = relationship('Submenu', back_populates='dishes')


Base.metadata.create_all(engine)
