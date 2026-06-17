from fastapi import FastAPI,Path,Query,HTTPException
import json
app = FastAPI()

def load_record():
    with open("patients.json",'r') as file:
        json_data = json.load(file)
    return json_data
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





