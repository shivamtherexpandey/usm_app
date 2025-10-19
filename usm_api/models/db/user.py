from __future__ import annotations
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


# Define models without relationships first
class SubscriptionPlan(SQLModel, table=True):
    __tablename__ = "usm_user_subscriptionplan"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, max_length=100)
    description: Optional[str] = Field(default=None)
    time_duration: int = Field(nullable=False, description="Duration in days")
    is_active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Subscription(SQLModel, table=True):
    __tablename__ = "usm_user_subscription"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    plan_id: int = Field(foreign_key="usm_user_subscriptionplan.id", nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class User(SQLModel, table=True):
    __tablename__ = "usm_user_user"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(nullable=False, unique=True, max_length=254)
    password: str = Field(nullable=False, max_length=128)
    subscription_id: Optional[int] = Field(default=None, foreign_key="usm_user_subscription.id")

    is_active: bool = Field(default=True, nullable=False)
    is_staff: bool = Field(default=False, nullable=False)
    is_superuser: bool = Field(default=False, nullable=False)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def __repr__(self) -> str:
        return f"<User email={self.email}>"


# Add relationships manually after class definitions
SubscriptionPlan.subscriptions = Relationship(back_populates="plan")
Subscription.plan = Relationship(back_populates="subscriptions")
Subscription.users = Relationship(back_populates="subscription")
User.subscription = Relationship(back_populates="users")