import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from transformers import BertTokenizer, BertModel
import torch
from dotenv import load_dotenv
import os
import ast
import joblib  # Для загрузки k-means модели
from sqlalchemy import create_engine

# === Загрузка модели KMeans ===
kmeans_model = joblib.load("Model\data\kmeans_model.joblib")

# === Загрузка переменных окружения ===
load_dotenv()

db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')

DATABASE_URL = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

# Создаем движок для подключения к базе данных
engine = create_engine(DATABASE_URL)

# === Загрузка модели RuBERT ===
model_name = 'DeepPavlov/rubert-base-cased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)
model.eval()  # Переключаем в режим инференса

# === Загрузка эмбеддингов из базы данных ===
query = "SELECT  catalog_num, title, author, date_category, embeddings FROM images"
df = pd.read_sql(query, engine)

# Проверка типов данных
print(df.dtypes)

# Преобразуем эмбеддинги в numpy-массив
# embeddings = np.vstack(df["embeddings"].apply(np.array))  # Предполагаем, что эмбеддинги хранятся как списки
# Функция для преобразования строк в массивы
def convert_to_array(embedding_string):
    try:
        return np.array(ast.literal_eval(embedding_string))
    except Exception as e:
        print(f"Ошибка преобразования: {e}")
        return np.array([])  # Возвращаем пустой массив

# Применяем преобразование
df['embeddings'] = df['embeddings'].apply(convert_to_array)

# Удаляем пустые массивы, если это необходимо
df = df[df['embeddings'].apply(lambda x: x.size > 0)]

# Пробуем встраивание массивов в один, если они всех одного размера
try:
    embeddings = np.vstack(df['embeddings'].to_numpy())
except ValueError as e:
    print(f"Ошибка при вертикальном сложении: {e}")

# === Функция для получения эмбеддингов запроса ===
def get_embeddings(query):
    inputs = tokenizer(query, padding=True, truncation=True, return_tensors="pt", max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)  # Усредняем по нужной размерности
    return embeddings.cpu().numpy()  # Переводим в numpy


# === Функция рекомендаций через KMeans + KNN ===
def recommend_by_kmeans_knn(query, embeddings, kmeans_model, n_recommendations=10):
    query_embedding = get_embeddings(query)  # Уже numpy
    query_cluster = kmeans_model.predict(query_embedding)[0]  # Получаем кластер
    cluster_indices = np.where(kmeans_model.labels_ == query_cluster)[0]  # Выбираем объекты из кластера

    cluster_embeddings = embeddings[cluster_indices]  # Берем их эмбеддинги

    # Создаем KNN-модель
    nn_model = NearestNeighbors(n_neighbors=n_recommendations, metric='cosine')
    nn_model.fit(cluster_embeddings)

    distances, indices = nn_model.kneighbors(query_embedding)

    recommended_indices = cluster_indices[indices.flatten()]  # Переводим в индексы исходного массива
    return recommended_indices


# === Функция получения экспонатов по индексам ===
def get_exhibits_by_indices(indices):
    return df.iloc[indices][["catalog_num", "title", "author", "date_category"]].to_dict(orient="records")


# === Пример использования ===
# user_query = "Айвазовский море"
# recommended_indices = recommend_by_kmeans_knn(user_query, embeddings, kmeans_model)

# Получаем рекомендованные экспонаты
# recommended_exhibits = get_exhibits_by_indices(recommended_indices)
# print(recommended_exhibits, sep='\n')


#===Отрабатывание модели на файлах===

# import numpy as np
# import pandas as pd
# from sklearn.neighbors import NearestNeighbors
# from transformers import BertTokenizer, BertModel
# import torch
# from dotenv import load_dotenv
# import os
# import joblib  # Для загрузки k-means модели

# # === Загрузка модели KMeans ===

# kmeans_model = joblib.load("Model\data\kmeans_model.joblib")

# # === Загрузка переменных окружения ===
# load_dotenv()

# db_host = os.getenv('DB_HOST')
# db_port = os.getenv('DB_PORT')
# db_name = os.getenv('DB_NAME')
# db_user = os.getenv('DB_USERNAME')
# db_password = os.getenv('DB_PASSWORD')

# DATABASE_URL = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

# # === Загрузка модели RuBERT ===
# model_name = 'DeepPavlov/rubert-base-cased'
# tokenizer = BertTokenizer.from_pretrained(model_name)
# model = BertModel.from_pretrained(model_name)
# model.eval()  # Переключаем в режим инференса

# # === Загрузка эмбеддингов из parquet ===
# df = pd.read_parquet('data_for_database_final.parquet')
# df["catalog_num"] = df.index

# # Преобразуем эмбеддинги в numpy-массив
# embeddings = np.vstack(df["embeddings"].apply(np.array))  # Если хранятся как списки


# # === Функция для получения эмбеддингов запроса ===
# def get_embeddings(query):
#     inputs = tokenizer(query, padding=True, truncation=True, return_tensors="pt", max_length=512)
#     with torch.no_grad():
#         outputs = model(**inputs)
#         embeddings = outputs.last_hidden_state.mean(dim=1)  # Усредняем по нужной размерности
#     return embeddings.cpu().numpy()  # Переводим в numpy


# # === Функция рекомендаций через KMeans + KNN ===
# def recommend_by_kmeans_knn(query, embeddings, kmeans_model, n_recommendations=10):
#     query_embedding = get_embeddings(query)  # Уже numpy
#     query_cluster = kmeans_model.predict(query_embedding)[0]  # Получаем кластер
#     cluster_indices = np.where(kmeans_model.labels_ == query_cluster)[0]  # Выбираем объекты из кластера

#     cluster_embeddings = embeddings[cluster_indices]  # Берем их эмбеддинги

#     # Создаем KNN-модель
#     nn_model = NearestNeighbors(n_neighbors=n_recommendations, metric='cosine')
#     nn_model.fit(cluster_embeddings)

#     distances, indices = nn_model.kneighbors(query_embedding)

#     recommended_indices = cluster_indices[indices.flatten()]  # Переводим в индексы исходного массива
#     return recommended_indices


# # === Функция получения экспонатов по индексам ===
# def get_exhibits_by_indices(indices):
#     return df.iloc[indices][["catalog_num", "title", "author", "date_category"]].to_dict(orient="records")


# # === Пример использования ===
# user_query = "Айвазовский море"
# recommended_indices = recommend_by_kmeans_knn(user_query, embeddings, kmeans_model)

# # Получаем рекомендованные экспонаты
# recommended_exhibits = get_exhibits_by_indices(recommended_indices)
# print(recommended_exhibits, sep='\n')