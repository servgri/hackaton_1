from datetime import date

from pydantic import BaseModel, ConfigDict

class ImageInfo(BaseModel):
    id: int
    title: str
    items: str
    description: str
    typology: str 
    author: str
    date_category: str
    key_words: str
    embedding: list[float]
    cluster: int 
    author_name: str
    author_patronymic: str
    catalog_num: float
    registration_date: date 
    image_url: str
  

    