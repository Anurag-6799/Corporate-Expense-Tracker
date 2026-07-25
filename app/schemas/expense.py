from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal # Use Decimal to match SQLAlchemy's Numeric
from datetime import datetime
from app.db.models import ExpenseStatus
from app.schemas.user import UserResponse # Import for nesting

class ExpenseBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=150)
    description: Optional[str] = None
    # We enforce that an expense must be strictly positive and > 0
    amount: Decimal = Field(..., gt=0)

# Used by employees to submit a new receipt
class ExpenseCreate(ExpenseBase):
    pass # Inherits everything from ExpenseBase, needs nothing else

# Used by employees to edit an expense (only if it is still PENDING)
class ExpenseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=150)
    description: Optional[str] = None
    amount: Optional[Decimal] = Field(None, gt=0)

# Used by managers to approve/reject an expense
class ExpenseStatusUpdate(BaseModel):
    status: ExpenseStatus

# Used when returning expense data to the client
class ExpenseResponse(ExpenseBase):
    id: int
    status: ExpenseStatus
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    # Nested Schema: When this Expense is returned, it will optionally 
    # include the full UserResponse object of the owner.
    owner: Optional[UserResponse] = None

    class Config:
        from_attributes = True