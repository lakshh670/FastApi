from pydantic import BaseModel,Field,AnyUrl,EmailStr,field_validator
from typing import List,Dict,Annotated,Optional

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @field_validator('email',mode='before') # by-default mode is before i.e. validation will be done before the type coercion.
    @classmethod # it's not that normal instance method, as validation is done before the creation of the object so we need a class method.
    def validate_email(cls,value):
        valid_domains=['hdfc.com', 'icici.com']
        domain=value.split('@')[-1]
        if domain not in valid_domains:
            raise ValueError('Invalid email address')
        return value
    @field_validator('name')
    @classmethod
    def transform_name(cls,value):
        return value.upper()

    @field_validator('age',mode='after')
    @classmethod
    def validate_age(cls,value):
        if 0<value<60:
            return value
        raise ValueError('Invalid age')

def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('updated')

patient_info = {'name':'nitish', 'email':'abc@icici.com', 'age': '30', 'weight': 75.2, 'married': True, 'allergies': ['pollen', 'dust'], 'contact_details':{'phone':'2353462'}}

patient1 = Patient(**patient_info) # validation -> type coercion

update_patient_data(patient1)
