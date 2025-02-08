from sqlalchemy import select
from guide.schemas import ImageInfo
from core.db import async_session_maker
from guide.models import Image

    
async def get_images_by_author_lastname(author_lastnames: List[str]) -> List[ImageInfo]:
    async with async_session_maker() as session: 
        # Создаем запрос с фильтрацией по author's last name
        query = select(Image).filter(Image.author_lastname.in_(author_lastnames))
        
        # Выполняем запрос
        result = await session.execute(query)
        
        # Извлекаем все записи
        images = result.scalars().all()
        
        # Преобразуем результаты в Pydantic модели
        image_info_list = [
            ImageInfo(
                catalog_num=image.catalog_num,
                title=image.title,
                image_url=image.image_url,
                author_lastname=image.author_lastname,
                author_name=image.author_name,
                author_patronymic=image.author_patronymic,
                description=image.description
            ) for image in images
        ]
        
        return image_info_list