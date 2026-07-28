from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User, UserRole
from app.schemas.expense import ExpenseCreate, ExpenseResponse, ExpenseUpdate, ExpenseStatusUpdate
from app.services.expense import create_expense, update_expense, change_expense_status
from app.core.security import get_current_user, RoleChecker

router = APIRouter(prefix="/expenses", tags=["Expenses"])

# Instantiate our RBAC Bouncer: Only Managers and Admins can pass this check
allow_managers = RoleChecker([UserRole.MANAGER, UserRole.ADMIN])

@router.post("/", response_model=ExpenseResponse)
def submit_expense(
    expense_in: ExpenseCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Any logged-in user can submit an expense."""
    return create_expense(db=db, expense_in=expense_in, current_user=current_user)

@router.put("/{expense_id}", response_model=ExpenseResponse)
def edit_expense(
    expense_id: int,
    expense_in: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Edit a pending expense (must be the owner)."""
    return update_expense(db=db, expense_id=expense_id, expense_in=expense_in, current_user=current_user)

@router.put("/{expense_id}/status", response_model=ExpenseResponse)
def review_expense(
    expense_id: int,
    status_in: ExpenseStatusUpdate,
    db: Session = Depends(get_db),
    # RBAC AuthZ: Standard employees will be blocked right here with a 403 Forbidden
    current_user: User = Depends(allow_managers) 
):
    """Managers/Admins only: Approve or Reject an expense."""
    return change_expense_status(db=db, expense_id=expense_id, status_in=status_in)