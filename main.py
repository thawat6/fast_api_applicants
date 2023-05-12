from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://localhost:3000", "http://172.25.0.2:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

applicants = []


class Applicant(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    address: str
    position: str
    expected_salary: float
    years_of_experience: int


@app.post("/applicants")
async def create_applicant(applicant: Applicant):
    applicant.id = len(applicants) + 1
    applicants.append(applicant)
    return {"message": "Applicant created successfully."}


@app.put("/applicants/{id}")
async def update_applicant(id: int, applicant: Applicant):
    for index, db_applicant in enumerate(applicants):
        if db_applicant.id == id:
            applicants[index] = applicant
            return {"message": "Applicant updated successfully."}
    return {"message": "Applicant not found."}


@app.delete("/applicants/{id}")
async def delete_applicant(id: int):
    for index, db_applicant in enumerate(applicants):
        if db_applicant.id == id:
            applicants.pop(index)
            return {"message": "Applicant deleted successfully."}
    return {"message": "Applicant not found."}


@app.get("/applicants/{applicant_id}", response_model=Applicant)
async def get_applicant_by_id(applicant_id: int):
    for applicant in applicants:
        if applicant.id == applicant_id:
            return applicant
    return {"message": "Applicant not found"}


@app.get("/applicants", response_model=List[Applicant])
async def get_all_applicants():
    return applicants
