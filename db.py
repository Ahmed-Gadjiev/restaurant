import decimal
import os
import uuid

from dotenv import load_dotenv
from sqlalchemy import Column, String, ForeignKey, Numeric, DECIMAL
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects import postgresql

load_dotenv()

db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_url = os.getenv('DB_URL')
db_port = os.getenv('DB_PORT')

engine = create_engine(
    f'postgresql://{db_user}:{db_password}@{db_url}:{db_port}/{db_name}',
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
