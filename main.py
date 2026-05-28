from typing import Optional, List, Annotated

from fastapi import FastAPI, status, HTTPException, Query, Path, Depends
from sqlalchemy.orm import Session
import uvicorn

from models import get_db, ClassRoom, Student, Contact, Email, Portfolio, PhoneNumber
from pydantic_models import StudentModel, ClassRoomModel, StudentModelResponse, ClassRoomModelResponse, ContactModelResponse, ContactModel


app = FastAPI()
DBSession = Annotated[Session, Depends(get_db)]


@app.post("/classroom/", status_code=status.HTTP_201_CREATED, response_model=ClassRoomModelResponse)
def add_class_room(class_room_model: ClassRoomModel, db: DBSession):
    class_room = ClassRoom(
        description=class_room_model.description
    )
    db.add(class_room)
    db.commit()
    db.refresh(class_room)
    return class_room


@app.get("/classroom/", status_code=status.HTTP_202_ACCEPTED, response_model=List[ClassRoomModelResponse])
def get_class_rooms(db: DBSession):
    return db.query(ClassRoom).all()


@app.get("/classroom/{classroom_id}/", response_model=ClassRoomModelResponse)
def get_class_room(db: DBSession, classroom_id: int = Path(...)):
    class_room = db.query(ClassRoom).filter_by(id=classroom_id).first()
    if not class_room:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого класу не існує")
    return class_room


@app.delete("/classroom/{classroom_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_classroom(db: DBSession, classroom_id: int = Path(..., description="ID класу(кабінету)")):
    classroom = db.query(ClassRoom).filter_by(id=classroom_id).first()
    if not classroom:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого кабінету не існує")

    db.delete(classroom)
    db.commit()


@app.post("/students/", status_code=status.HTTP_201_CREATED, response_model=StudentModelResponse)
def add_student(db: DBSession, student_model: StudentModel):
    student = Student(**student_model.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@app.get("/students/", status_code=status.HTTP_200_OK, response_model=List[StudentModelResponse])
def get_students(db: DBSession):
    return db.query(Student).all()


@app.get("/students/{student_id}/", status_code=status.HTTP_200_OK, response_model=StudentModelResponse)
def get_student(db: DBSession, student_id: int = Path(...)):
    student = db.query(Student).filter_by(id=student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Студента з id={student_id} не знайдено")
    return student


@app.delete("/students/{student_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(db: DBSession, student_id: int = Path(...)):
    student = db.query(Student).filter_by(id=student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Студента з id={student_id} не знайдено")

    db.delete(student)
    db.commit()


@app.patch("/student-to-class/", status_code=status.HTTP_202_ACCEPTED)
def add_student_to_class(
    db: DBSession,
    student_id: int = Query(..., description="ID студента"),
    classroom_id: int = Query(..., description="ID групи")
):
    student = db.query(Student).filter_by(id=student_id).first()
    classroom = db.query(ClassRoom).filter_by(id=classroom_id).first()
    if not student or not classroom:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Студента або групу не знайдено")

    student.classroom_id = classroom_id
    # student.classroom = classroom
    # classroom.students.append(student)

    db.commit()


@app.delete("/student-to-class/", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_to_class(
    db: DBSession,
    student_id: int = Query(...),
    classroom_id: int = Query(...)
):
    student = db.query(Student).filter_by(id=student_id).first()
    classroom = db.query(ClassRoom).filter_by(id=classroom_id).first()
    if not all(student, classroom, student in classroom.students):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Не можливо видалити")

    classroom.students.remove(student)


@app.post("/contacts/", response_model=ContactModelResponse, status_code=status.HTTP_201_CREATED)
def app_contact(db: DBSession, contact_model: ContactModel):
    contact = Contact(
        first_name=contact_model.first_name,
        last_name=contact_model.last_name
    )
    for phone_number_model in contact_model.numbers:
        phone_number = PhoneNumber(**phone_number_model.model_dump())
        contact.numbers.append(phone_number)

    for email_model in contact_model.emails:
        email = Email(**email_model.model_dump())
        contact.emails.append(email)

    portfolio = Portfolio(**contact_model.portfolio.model_dump())
    contact.portfolio = portfolio

    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
