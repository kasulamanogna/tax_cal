from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, auth, database

router = APIRouter()

@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(database.SessionLocal)):
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed = auth.hash_password(user.password)
    new_user = models.User(username=user.username, password=hashed)
    db.add(new_user)
    db.commit()
    return {"msg": "User created"}

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(database.SessionLocal)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not auth.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = auth.create_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/tax_history", response_model=schemas.TaxHistoryOut)
def create_tax_history(history: schemas.TaxHistoryCreate, db: Session = Depends(database.SessionLocal), user: schemas.UserLogin = Depends()):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    tax_history = models.TaxHistory(user_id=db_user.id, **history.dict())
    db.add(tax_history)
    db.commit()
    return tax_history

@router.get("/tax_history/{username}", response_model=list[schemas.TaxHistoryOut])
def get_tax_history(username: str, db: Session = Depends(database.SessionLocal)):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db.query(models.TaxHistory).filter(models.TaxHistory.user_id == db_user.id).all()
