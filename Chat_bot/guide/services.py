import logging
import numpy as np
import pickle
from sklearn.cluster import KMeans
from transformers import BertTokenizer, BertModel
import torch
import psycopg2

# # Загрузка моделей и данных
# with open('kmeans_model.pkl', 'rb') as f:
#     kmeans_model = pickle.load(f)

# with open('rubert_embeddings.pkl', 'rb') as f:
#     data = pickle.load(f)

# # Загрузка RuBERT модели и токенизатора
# model_name = 'rubert-base-cased' 
# tokenizer = BertTokenizer.from_pretrained(model_name)
# model = BertModel.from_pretrained(model_name)


# # Функция для получения эмбеддингов запроса
# def get_embeddings(query):
#     inputs = tokenizer(query, padding=True, truncation=True, return_tensors="pt", max_length=512)
#     with torch.no_grad():
#         outputs = model(**inputs)
#         embeddings = outputs.last_hidden_state.mean(dim=1)
#     return embeddings

# def resize_embedding(embedding, target_dim):
#     current_dim = embedding.shape[1]
#     if current_dim == target_dim:
#         return embedding
#     if current_dim < target_dim:
#         padding = np.zeros((embedding.shape[0], target_dim - current_dim))
#         return np.hstack([embedding, padding])
#     return embedding[:, :target_dim]

# # Рекомендация экспонатов по кластеру
# def recommend_by_cluster(query, data, kmeans_model, n_recommendations=5):
#     # Получаем целевую размерность из KMeans
#     target_dim = kmeans_model.cluster_centers_.shape[1]
#     # Получаем эмбеддинг запроса
#     query_embedding = get_embeddings([query]).numpy()
#     # Приводим эмбеддинг к нужной размерности
#     query_embedding_resized = resize_embedding(query_embedding, target_dim)
#     query_cluster = kmeans_model.predict(query_embedding_resized)
#     recommended_items = data[data['cluster'] == query_cluster[0]].head(n_recommendations)
#     return recommended_items


conn = psycopg2.connect(
    dbname="",
    user="",
    password="",
    host="",
    port=""
)
cursor = conn.cursor()


# Загрузка RuBERT модели и токенизатора
model_name = 'rubert-base-cased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

# Функция для получения эмбеддингов запроса
def get_embeddings(query):
    inputs = tokenizer(query, padding=True, truncation=True, return_tensors="pt", max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).numpy()
    return embeddings[0]  # Преобразуем в 1D массив

# Рекомендация экспонатов по кластеру
def recommend_by_cluster(query, conn, n_recommendations=5):
    # Получаем эмбеддинг запроса
    query_embedding = get_embeddings([query])
    
    # Находим ближайший кластер с помощью kmeans
    cursor = conn.cursor()
    cursor.execute("SELECT id, center FROM clusters ORDER BY center <-> %s LIMIT 1;", (query_embedding,))
    cluster_id = cursor.fetchone()[0]
    
    # Получаем рекомендованные объекты из этого кластера
    cursor.execute("SELECT title, author, date_category FROM images WHERE cluster_id = %s ORDER BY embedding <-> %s LIMIT %s;", 
                   (cluster_id, query_embedding, n_recommendations))
    recommended_items = cursor.fetchall()
    
    return recommended_items

user_query = "картина, изображающая пейзаж с озером"
recommendations = recommend_by_cluster(user_query, conn)

print(recommendations)
