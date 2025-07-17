from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, services, database

router = APIRouter()

@router.post("/submit-income", response_model=schemas.TaxOutput)
def submit_income(
    income: schemas.IncomeInput,
    username: str,
    db: Session = Depends(database.SessionLocal)
):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    # Store income entry
    income_entry = models.IncomeEntry(
        amount=income.amount,
        regime=income.regime,
        user_id=db_user.id
    )
    db.add(income_entry)
    db.commit()
    # Calculate tax
    tax = services.tax.calculate_tax(income.amount, income.regime)
    # Store tax history
    tax_history = models.TaxHistory(
        user_id=db_user.id,
        year=2025,  # You can make this dynamic
        total_income=income.amount,
        tax_paid=tax
    )
    db.add(tax_history)
    db.commit()
    return {"tax": tax}