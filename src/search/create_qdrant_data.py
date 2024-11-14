from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models
import pandas as pd
import ast


def create_qdrant_data(embedding_dim, embedding_file_path, collection_name="song_embeddings"):
    # 連接 Qdrant 服務
    client = QdrantClient(host="localhost", port=6333)

    # 建立 Qdrant 集合
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=qdrant_models.VectorParams(size=embedding_dim, distance="Cosine")
    )
    
    # 載入嵌入資料
    meta_df = pd.read_csv('../../data/song_id.csv')
    embeddings_df = pd.read_csv(embedding_file_path)
    embeddings_df['embeddings'] = embeddings_df['embeddings'].apply(ast.literal_eval)
    df = meta_df.merge(embeddings_df, how='left', on='song_id')
    print(df.columns)
    print(f'Num of songs: {df.shape[0]}')
    for index, row in df.iterrows():
        client.upsert(
            collection_name=collection_name,
            points=[qdrant_models.PointStruct(
                id=row['song_id'],
                vector=row['embeddings'],
                payload={'song_name': row['song_name']}
            )]
        )

    print(f"Data has been successfully uploaded to Qdrant collection '{collection_name}'.")

if __name__ == "__main__":
    # 假設嵌入的維度為 768，並且 CSV 檔案路徑為 "embeddings.csv"
    create_qdrant_data(embedding_dim=768, embedding_file_path="../../data/embeddings/maest30s_embeddings.csv")

