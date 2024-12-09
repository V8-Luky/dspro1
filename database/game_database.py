import time
import numpy as np

from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from pinecone import Index

DEFAULT_METRIC = "cosine"

class GameDatabase:
    @staticmethod
    def _prepare_records(
        ids: list[str], metadata_records: list[dict], embeddings: list
    ) -> list:
        records = []
        for id_, metadata, embedding in zip(ids, metadata_records, embeddings):
            records.append(
                {
                    "id": id_,
                    "values": embedding,
                    "metadata": {
                        key: metadata[key] for key in metadata.keys() if key != "id"
                    },
                }
            )

        return records

    def __init__(self, api_key: str, indexes: dict[str, int] = None):
        self.pc = Pinecone(api_key=api_key)
        self._namespace = "steam-games"
        self._indexes = dict()
        if indexes:
            for key, value in indexes.items():
                self._create_index(index_name=key, dimension=value, metric=DEFAULT_METRIC)

    def get_similarity(self, index_name: str, name: str, embedding: np.ndarray):
        index = self._get_index(index_name)

        results = index.query(
            namespace=self._namespace,
            vector=embedding,
            top_k=1,
            filter={"Name": {"$eq": name}},
            include_values=False,
            include_metadata=True,
        )

        if len(results["matches"]) < 1:
            return None

        return results["matches"][0]

    def get_similar(self, index_name:str, embedding: np.ndarray, k: int = 1):
        index = self._get_index(index_name)
        namespace = self._namespace

        results = index.query(
            namespace=namespace,
            vector=embedding,
            top_k=k,
            include_values=False,
            include_metadata=True,
        )

        return results["matches"]

    def get_by_id(self, index_name: str, id_: str):
        index = self._get_index(index_name)

        results = index.fetch(
            namespace=self._namespace,
            ids=[id_],
        )

        return results["vectors"][id_]

    def get_ids(self, index_name: str):
        all_ids = []
        for page in list(self._get_index(index_name).list(namespace=self._namespace)):
            all_ids.extend(page)
        return all_ids

    def load_data(self, index_name: str, ids: list[str], data: list[dict], embeddings: list, slice_size: int = 100):
        records = GameDatabase._prepare_records(ids, data, embeddings)
        if len(records) < 1:
            return

        self._clear_data(index_name=index_name)
        
        dimension = len(embeddings[0])
        index = self._create_index(index_name=index_name, dimension=dimension, metric=DEFAULT_METRIC)

        step = slice_size
        from_i, to_i = 0, 0
        while from_i < len(records):
            to_i += step
            to_i = min(to_i, len(records))
            print(f"Inserting records {from_i + 1} to {to_i}")
            self._upsert_records(
                namespace=self._namespace, index=index, records=records[from_i:to_i]
            )
            from_i = to_i

    def describe_index(self, index_name: str):
        return self._get_index(index_name).describe_index_stats()

    def _clear_data(self, index_name: str):
        self._delete_index(index_name=index_name)

    def _create_index(self, index_name: str, dimension: int, metric: str):
        if not self.pc.has_index(index_name):
            self.pc.create_index(
                name=index_name,
                dimension=dimension,
                metric=metric,
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )

        # Wait for the index to be ready
        while not self.pc.describe_index(index_name).status["ready"]:
            time.sleep(1)
        
        self._indexes[index_name] = self.pc.Index(index_name)
        return self._get_index(index_name)

    def _delete_index(self, index_name: str):
        if not self.pc.has_index(index_name):
            return
        self.pc.delete_index(index_name)

    def _upsert_records(self, namespace: str, index: Index, records: list[dict]):
        index.upsert(vectors=records, namespace=namespace)

    def _get_index(self, index_name: str):
        return self._indexes[index_name]
