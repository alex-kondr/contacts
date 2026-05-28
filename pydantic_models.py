from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl, EmailStr


class PhoneNumberModel(BaseModel):
    number: str = Field(..., description="Номер телефону", min_length=5)
    description: Optional[str] = Field(None, description="Опис")
    country: Optional[str] = Field("Україна", description="Країна")


class EmailModel(BaseModel):
    email: EmailStr = Field(..., description="Електронна скринька", min_length=3)
    description: Optional[str] = Field(None, description="Опис")


class PortfolioModel(BaseModel):
    url: str = Field(..., description="Веб-сторінка")
    description: Optional[str] = Field(None, description="Опис")


class ContactModel(BaseModel):
    first_name: str = Field(..., description="Ім'я", min_length=3)
    last_name: Optional[str] = Field(None, description="Прізвище")
    numbers: List[PhoneNumberModel] = Field([], description="Список номерів")
    emails: List[EmailModel] = Field([], description="Список електронних адрес")
    portfolio: Optional[PortfolioModel] = Field(None, description="Про себе")


class ContactModelResponse(ContactModel):
    id: int


class StudentModel(BaseModel):
    full_name: str = Field(..., description="Ім'я")
    bio: Optional[str] = Field(None, description="Опис")
    age: Optional[int] = Field(18, description="Вік")


class StudentModelResponse(StudentModel):
    id: int = Field(..., description="ID елемента")


class ClassRoomModel(BaseModel):
    students: List[StudentModel] = Field([])
    description: Optional[str] = Field(None, max_length=500)
    subject: Optional[str] = Field(None, description="Назва тематичного класу", max_length=50)


class ClassRoomModelResponse(ClassRoomModel):
    id: int = Field(...)
    students: List[StudentModelResponse] = Field([])


# student_1 = dict(
#     full_name="Василь"
# )
# student_2 = dict(
#     full_name="Наталя",
#     bio="Дуже розумна"
# )
# student_3 = dict(bio="Невірний запис")

# student_model_1 = StudentModel.model_validate(student_1)
# student_model_3 = StudentModel.model_validate(student_3)
# print(student_model_3)

# class_room_1 = dict()
# class_room_2 = dict(
#     students=[
#         dict(full_name="Петро"),
#         dict(full_name="Анастасія", bio="Полюбляє спорт"),
#         dict(bio="Тільки біографія", full_name="Ксенія")
#     ],
#     description="10-Б"
# )
# class_1 = ClassRoomModel.model_validate(class_room_1)
# class_2 = ClassRoomModel.model_validate(class_room_2)
# model_json = class_2.model_dump_json()
# print(type(class_1))
# print(type(class_2.model_dump()))
# print(type(class_2.model_dump_json()))

# model_json = '{"students":[{"full_name":"Петро","bio":null},{"full_name":"Анастасія","bio":"Полюбляє спорт"},{"full_name":"Ксенія","bio":"Тільки біографія"}],"description":"10-Б"}'

# class_2 = ClassRoomModel.model_validate_json(model_json)
# print(class_2)