from fastapi import FastAPI,Path,Query,HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import List,Annotated,Literal,Optional
import json
app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]


    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

def load_record():
    with open("patients.json",'r') as file:
        json_data = json.load(file)
    return json_data

def save_record(data):
    with open("patients.json",'w') as file:
        json.dump(data,file)
@app.get("/")
def hello():
    return {"message": "Patient managment system API"}

@app.get("/about")
def about():
    return {"message":"A fully functional API to manage your patient's records."}

@app.get("/view")
def view():
    data=load_record()
    return data

@app.get("/patient/{patient_id}") # Path Parameter. It is dynamically passed at the end of the URL and it's value is required.
def patient(patient_id:str=Path(...,description='ID of the patient in the DB', example='P001')):
    data=load_record()
    if patient_id in data:
        return data[patient_id]
    return {"message":"Patient does not exist"}

@app.get("/sort")
def sort_patients(sort_by:str=Query(...,description='Sort on the basis of height, weight or bmi'),order:str=Query('asc',description='Sort in asc or desc order.')):

    #   ... means that parameter is required
    valid_fields=['height','weight','bmi']
    ord=['asc','desc']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail="Invalid field.Choose from {}".format(valid_fields))
    if order not in ord:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')

    reverse=True if order=='desc' else False
    data=load_record()
    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=reverse)
    return sorted_data


@app.post("/create")
def create_patient(patient:Patient):
    # load existing data
    data = load_record()

    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    # new patient add to the database
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save into the json file
    save_record(data)

    return JSONResponse(status_code=201, content={'message': 'patient created successfully'})

@app.put("/edit/{patient_id}")
def update_patient(patient:PatientUpdate,patient_id:str):
    data=load_record()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient does not exist')

    patient_dict=patient.model_dump(exclude_unset=True) # We want only those fields whose values are not none.
    old_info=data[patient_id]
    for key,value in patient_dict.items():
        old_info[key]=value

    # Now this old key is a dict with the updated values but are computed fields bmi and verdict still arent updated.
    # So we will first convert this dict to the pydantic object and our fields will be automatically created.
    old_info['id']=patient_id
    updated_patient_info=Patient(**old_info) # dict->pydantic
    updated_patient_info=updated_patient_info.model_dump(exclude=['id']) # pydantic->dict

    data[patient_id]=updated_patient_info
    save_record(data)
    return JSONResponse(status_code=200, content={'message': 'patient updated successfully'})


# delete method
@app.delete("/delete/{patient_id}")
def delete(patient_id:str):
    data=load_record()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient does not exist')

    del data[patient_id]
    save_record(data)
    return JSONResponse(status_code=200, content={'message': 'patient deleted successfully'})




