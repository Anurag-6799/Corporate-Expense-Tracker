import enum
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Numeric, DateTime, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

# --- 1. ENUMS (Strict State Management) ---

class UserRole(str, enum.Enum):
    EMPLOYEE = "employee"
    MANAGER = "manager"
    ADMIN = "admin"

class ExpenseStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

# --- 2. MODELS ---

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    
    # RBAC Core: Default everyone to employee. 
    # Only Admins will be able to change this field.
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE, nullable=False)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # The Relationship pointing to the Expense table
    expenses = relationship("Expense", back_populates="owner")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text)
    
    # Numeric is used for currency to prevent floating-point rounding errors
    amount = Column(Numeric(10, 2), nullable=False)
    
    # State Management
    status = Column(Enum(ExpenseStatus), default=ExpenseStatus.PENDING, nullable=False)
    
    # Auditing Timestamps
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    # onupdate automatically fires when this row is modified
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # The Foreign Key linking back to the User who submitted it
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # The Relationship pointing back to the User table
    owner = relationship("User", back_populates="expenses")