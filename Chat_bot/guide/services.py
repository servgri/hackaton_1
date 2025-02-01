# import numpy as np
# import pickle
# from sklearn.cluster import KMeans
# from transformers import BertTokenizer, BertModel
# import torch

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

