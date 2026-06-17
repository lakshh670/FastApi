from pydantic import BaseModel,Field,AnyUrl,EmailStr
from typing import List,Dict,Annotated,Optional

class Patient(BaseModel):

    name: Annotated[str, Field(max_length=50, title='Name of the patient', description='Give the name of the patient in less than 50 chars', examples=['Nitish', 'Amit'])]
    email: EmailStr
    linkedin_url: AnyUrl
    age: int = Field(gt=0, lt=120)
    weight: Annotated[float, Field(gt=0, strict=True)] # i.e. automatic typeconversion will not be done. '60.2' will not be accepted only 60.2
    married: Annotated[bool, Field(default=None, description='Is the patient married or not')]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]
    contact_details: Dict[str, str]

def update_patient_data(data: Patient):
    print(data.name)
    print(data.age)
    print(data.allergies)
    print(data.married)
    print('updated')

patient_info = {'name':'nitish', 'email':'abc@gmail.com', 'linkedin_url':'http://linkedin.com/1322', 'age': '30', 'weight': 75.2,'contact_details':{'phone':'2353462'}}
patient1=Patient(**patient_info)
update_patient_data(patient1)
