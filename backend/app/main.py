from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, database

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

# Dependency для получения сессии БД
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/rails", response_model=List[schemas.Rail])
def get_rails(db: Session = Depends(get_db)):
    rails = db.query(models.Rail).all()
    return rails

@app.put("/rails/{rail_id}/status")
def update_rail_status(rail_id: str, status: str, db: Session = Depends(get_db)):
    rail = db.query(models.Rail).filter(models.Rail.id == rail_id).first()
    if rail:
        rail.status = status
        db.commit()
        return {"message": "Status updated"}
    else:
        raise HTTPException(status_code=404, detail="Rail not found")