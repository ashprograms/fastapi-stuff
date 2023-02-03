from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class StudentClass(BaseModel):
    name: str
    age: int
    year: int

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[int] = None

students = {
    1: StudentClass(name="Jesus Christ", age=17, year=12)
}

@app.get("/")
def index():
    return {"Hello": "World!"}

@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(None, description="The ID of the target student", gt=0)):
    if student_id in students:
        return students[student_id]
    else:
        return {"Error": "Student not found"}

@app.get("/get-by-name/{student_name}")
def get_by_name(student_name: str = Path(None, description="The full name of the target student")):
    for student_id in students:
        if students[student_id].name.lower() == student_name.lower():
            to_return = {"name": students[student_id].name, "age": students[student_id].age, "year": students[student_id].year, "userid": student_id}
            return to_return
    return {"Error": "Student not found"}

@app.post("/create-student/")
def create_student(student: StudentClass):
    new_id = len(students) + 1
    students[new_id] = student
    to_return = {"name": students[new_id].name, "age": students[new_id].age, "year": students[new_id].year, "userid": new_id}
    return to_return

@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student not found"}
    
    if student.name != None:
        students[student_id].name = student.name

    if student.age != None:
        students[student_id].age = student.age

    if student.year != None:
        students[student_id].year = student.year

    to_return = {"name": students[student_id].name, "age": students[student_id].age, "year": students[student_id].year, "userid": student_id}
    return to_return