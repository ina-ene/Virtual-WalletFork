from datetime import datetime, date
from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    String,
    Integer,
    Boolean,
    Text,
    ForeignKey,
    DateTime,
    Date,
    DECIMAL,
)
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.orm.decl_api import Mapped
from dataclasses import dataclass

Base = declarative_base()


@dataclass
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(length=25), unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(length=200), nullable=False)
    email: Mapped[str] = mapped_column(String(length=50), unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(
        String(length=100), unique=True, nullable=False
    )
    photo_path: Mapped[str] = mapped_column(String(length=300), nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_restricted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user_accounts = relationship("Account", back_populates="accounts_user")

    contacts_as_user = relationship(
        "Contact", foreign_keys="[Contact.user_username]", back_populates="user"
    )
    contacts_as_contact = relationship(
        "Contact",
        foreign_keys="[Contact.contact_username]",
        back_populates="contact_user",
    )


@dataclass
class Contact(Base):
    __tablename__ = "contacts"
    user_username: Mapped[str] = mapped_column(
        String(length=25), ForeignKey("users.username"), primary_key=True
    )
    contact_username: Mapped[str] = mapped_column(
        String(length=25), ForeignKey("users.username"), primary_key=True
    )

    user = relationship(
        "User", foreign_keys=[user_username], back_populates="contacts_as_user"
    )
    contact_user = relationship(
        "User", foreign_keys=[contact_username], back_populates="contacts_as_contact"
    )


@dataclass
class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(length=25), ForeignKey("users.username"), nullable=False
    )
    balance: Mapped[float] = mapped_column(DECIMAL(10, 2), default=0.00, nullable=False)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)

    accounts_user = relationship(
        "User", back_populates="user_accounts", foreign_keys=[username]
    )
    accounts_cards = relationship("Card", back_populates="cards_accounts")


@dataclass
class Card(Base):
    __tablename__ = "cards"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("accounts.id"), nullable=False
    )
    card_number: Mapped[str] = mapped_column(
        String(length=16), unique=True, nullable=False
    )
    expiration_date: Mapped[date] = mapped_column(Date, nullable=False)
    card_holder: Mapped[str] = mapped_column(String(length=50), nullable=False)
    cvv: Mapped[str] = mapped_column(String(length=3), nullable=False)
    design_path: Mapped[str] = mapped_column(String(length=150), nullable=True)

    cards_accounts = relationship("Account", back_populates="accounts_cards")


@dataclass
class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    sender_account: Mapped[int] = mapped_column(Integer, nullable=False)
    receiver_account: Mapped[int] = mapped_column(Integer, nullable=False)
    amount: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("categories.id"), nullable=False
    )
    description: Mapped[str] = mapped_column(Text, nullable=True)
    transaction_date: Mapped[datetime] = mapped_column(DateTime, default=None)
    status: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )  # (0 = pending, 1 = completed, 2 = declined)
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    recurring_interval: Mapped[int] = mapped_column(
        Integer
    )  # (0 = daily, 1 = weekly, 2 = monthly)
    is_flagged: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


@dataclass
class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=30), nullable=False)
    color_hex: Mapped[str] = mapped_column(String(length=7), nullable=False)

    categories_transactions = relationship("Transaction", backref="categories")