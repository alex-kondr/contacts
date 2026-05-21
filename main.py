from typing import Optional, List, Annotated

from fastapi import FastAPI, status, HTTPException, Query, Path, Depends
from sqlalchemy.orm import Session
import uvicorn

from models import get_db, ClassRoom, Student
from pydantic_models import StudentModel, ClassRoomModel, StudentModelResponse, ClassRoomModelResponse


app = FastAPI()


@app.post("/classroom/", status_code=status.HTTP_201_CREATED, response_model=ClassRoomModelResponse)
def add_class_room(class_room_model: ClassRoomModel, db: Annotated[Session, Depends(get_db)]):
    class_room = ClassRoom(
        description=class_room_model.description
    )
    db.add(class_room)
    db.commit()
    db.refresh(class_room)
    return class_room


@app.get("/classroom/", status_code=status.HTTP_202_ACCEPTED, response_model=List[ClassRoomModelResponse])
def get_class_rooms(db: Annotated[Session, Depends(get_db)]):
    return db.query(ClassRoom).all()


@app.get("/classroom/{classroom_id}/", response_model=ClassRoomModelResponse)
def get_class_room(db: Annotated[Session, Depends(get_db)], classroom_id: int = Path(...)):
    class_room = db.query(ClassRoom).filter_by(id=classroom_id).first()
    if not class_room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого класу не існує")
    return class_room


# db.delete(class_room)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
