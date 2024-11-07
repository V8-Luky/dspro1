import time
from typing import overload

from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from pinecone import Index


class GameDatabase:
    @staticmethod
    def _prepare_records(data, embeddings) -> list:
        records = []
        for d, e in zip(data, embeddings):
            # TODO: adapt to our own data structure
            records.append(
                {"id": d["id"], "values": e["values"], "metadata": {"text": d["text"]}}
            )

        return records

    def __init__(self, api_key: str):
        self.pc = Pinecone(api_key=api_key)
        # TODO:
        self._main_index = self._create_index(
            "game-index", dimension=1024, metric="cosine"
        )
        self._namespace = "steam-games"

    @property
    def index(self) -> Index:
        return self._main_index

    def get_similar(self, embedding, k: int = 1):
        index = self._main_index
        namespace = self._namespace

        results = index.query(
            namespace=namespace,
            vector=embedding,
            top_k=k + 1,
            include_values=False,
            include_metadata=True,
        )

        return results[1:]
    
    def get_by_id(self, id):
        pass

    def get_by_name(self, name: str):
        pass

    def load_data(self, data, embeddings):
        records = GameDatabase._prepare_records(data, embeddings)
        self._upsert_records(namespace=self._namespace, records=records)

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

        return self.pc.Index("example-index")

    def _upsert_records(self, namespace: str, records: list[dict]):
        self._upsert_records(
            namespace=namespace, index=self._main_index, records=records
        )

    @overload
    def _upsert_records(self, namespace: str, index: Index, records: list[dict]):
        index.upsert(records=records, namespace=namespace)
        time.sleep(5)
        print(f"{index.describe_index_stats()}")
