import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from transformers import BertTokenizer, BertModel
import torch
import joblib

def load_kmeans_model(model_path="kmeans_model2.joblib"):
    """
    Загрузка модели KMeans.
    """
    return joblib.load(model_path)

def load_rubert_model():
    """
    Загрузка модели RuBERT и ее токенайзера.
    """
    model_name = 'DeepPavlov/rubert-base-cased'
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertModel.from_pretrained(model_name)
    model.eval()  # Переключение в режим инференса
    return tokenizer, model

def load_data(data_path='data_for_database_final2.parquet'):
    """
    Загрузка данных и их подготовка.
    """
    df = pd.read_parquet(data_path)
    df["catalog_num"] = df.index  # Добавляем столбец для идентификатора
    embeddings = np.vstack(df["embeddings"].apply(np.array))  # Преобразуем эмбеддинги в numpy-массив
    return df, embeddings

def get_query_embedding(user_query, tokenizer, model):
    """
    Преобразование текстового запроса пользователя в эмбеддинг.
    """
    inputs = tokenizer(user_query, padding=True, truncation=True, return_tensors="pt", max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        query_embedding = outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
    return query_embedding

def get_cluster(query_embedding, kmeans_model):
    """
    Предсказание кластера для запроса.
    """
    query_embedding_2d = query_embedding.reshape(1, -1)
    cluster = kmeans_model.predict(query_embedding_2d)[0]  # Определяем ближайший кластер
    return cluster

def get_recommendations(
        user_query, 
        kmeans_model_path="Model\data\kmeans_model.joblib", 
        data_path='data_for_database_final.parquet', 
        n_recommendations=5
    ):
    """
    Возвращает рекомендации на основе запроса пользователя.
    """
    # Загрузка необходимых моделей и данных
    kmeans_model = load_kmeans_model(kmeans_model_path)
    tokenizer, rubert_model = load_rubert_model()
    df, embeddings = load_data(data_path)
    
    # Получение эмбеддинга пользователя
    query_embedding = get_query_embedding(user_query, tokenizer, rubert_model)
    
    # Предсказание кластера
    cluster = get_cluster(query_embedding, kmeans_model)

    # Фильтрация данных по кластеру
    cluster_data = df[df["cluster"] == cluster]
    cluster_embeddings = np.vstack(cluster_data["embeddings"].apply(np.array))

    # Поиск наиболее похожих объектов в этом кластере. Создаем KNN-модель
    nn_model = NearestNeighbors(n_neighbors=n_recommendations, metric="cosine", algorithm="brute")
    nn_model.fit(cluster_embeddings)

    distances, indices = nn_model.kneighbors(query_embedding.reshape(1, -1))

    # Составление списка рекомендаций
    recommended_indices = cluster_data.iloc[indices[0]].index
    recommended_exhibits = df.loc[recommended_indices][["title", "author", "date_category"]].to_dict(orient="records")
    return recommended_exhibits
