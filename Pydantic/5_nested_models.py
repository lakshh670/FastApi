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
print(patient1.address.pincode)
