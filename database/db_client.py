import time
from typing import overload

from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from pinecone import Index


class DatabaseClient:
    @staticmethod
    def _prepare_records(data, embeddings) -> list:
        records = []
        for d, e in zip(data, embeddings):
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

    def load_data(self, data, embeddings):
        records = DatabaseClient._prepare_records(data, embeddings)
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
