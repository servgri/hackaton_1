from datetime import date

from pydantic import BaseModel, ConfigDict

class ImageInfo(BaseModel):
    catalog_num: int
    title: str 
    image_url: str | None
    author_lastname: str | None
    author_name: str | None
    author_patronymic: str | None
    description:  str | None
  

    