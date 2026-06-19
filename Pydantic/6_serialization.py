from pydantic import BaseModel
class Address(BaseModel):
    city:str
    state:str
    pincode:str

class Patient(BaseModel):
    name:str
    gender:str
    age:int
    address:Address

address_info={
    'city':'Jaipur',
    'state':'Rajasthan',
    'pincode':'302031'
}
address1=Address(**address_info)
patient_info={
    'name':'X',
    'gender':'Male',
    'age':18,
    'address':address1
}
patient1=Patient(**patient_info)

temp_dict=patient1.model_dump() # store model object as dictionary
temp_json=patient1.model_dump_json() # store model object as json
temp_dict=patient1.model_dump(include=['name', 'gender', 'age'}]) # only include these fields
temp_dict=patient1.model_dump(include={'name':True, 'gender':True, 'age':True, 'address':{'pincode'}}) # only include these fields



