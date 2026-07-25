from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models import Expense, User, ExpenseStatus
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseStatusUpdate

def create_expense(db: Session, expense_in: ExpenseCreate, current_user: User) -> Expense:
    db_expense = Expense(
        title=expense_in.title,
        description=expense_in.description,
        amount=expense_in.amount,
        owner_id=current_user.id
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def update_expense(db: Session, expense_id: int, expense_in: ExpenseUpdate, current_user: User) -> Expense:
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    
    if not db_expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found.")
        
    # Domain Rule 1: Ownership Check
    if db_expense.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not own this expense.")
        
    # Domain Rule 2: State Machine Check (Cannot edit approved/rejected expenses)
    if db_expense.status != ExpenseStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Cannot edit an expense that is already {db_expense.status.value}."
        )

    # Apply updates
    update_data = expense_in.model_dump(exclude_unset=True) # Pydantic v2 syntax
    for key, value in update_data.items():
        setattr(db_expense, key, value)

    db.commit()
    db.refresh(db_expense)
    return db_expense


def change_expense_status(db: Session, expense_id: int, status_in: ExpenseStatusUpdate) -> Expense:
    """
    Called by Managers/Admins to approve or reject. 
    Notice we don't check the user role here—the Bouncer does that at the router level!
    """
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    
    if not db_expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found.")
        
    db_expense.status = status_in.status
    db.commit()
    db.refresh(db_expense)
    return db_expense