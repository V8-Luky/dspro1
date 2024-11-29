import time
import numpy as np

from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from pinecone import Index


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

    def __init__(self, api_key: str, dimension: int = 1024):
        self.pc = Pinecone(api_key=api_key)
        self._dimension = dimension
        self._create_main_index()
        self._namespace = "steam-games"

    @property
    def index(self) -> Index:
        return self._main_index

    def get_similarity(self, name: str, embedding: np.ndarray):
        index = self._main_index
        namespace = self._namespace

        results = index.query(
            namespace=namespace,
            vector=embedding,
            top_k=1,
            filter={"name": {"$eq": name}},
            include_values=False,
            include_metadata=True,
        )

        if len(results["matches"]) < 1:
            return None

        return results["matches"][0]

    def get_similar(self, embedding: np.ndarray, k: int = 1):
        index = self._main_index
        namespace = self._namespace

        results = index.query(
            namespace=namespace,
            vector=embedding,
            top_k=k,
            include_values=False,
            include_metadata=True,
        )

        return results["matches"]

    def get_by_id(self, id_: str):
        index = self._main_index
        namespace = self._namespace

        results = index.fetch(
            namespace=namespace,
            ids=[id_],
        )

        return results["vectors"][id_]

    def get_ids(self):
        return list(self._main_index.list(namespace=self._namespace))[0]

    def get_random(self):
        ids = self.get_ids()
        id_ = np.random.choice(ids)
        return self.get_by_id(id_)

    def load_data(self, ids: list[str], data: list[dict], embeddings: list):
        records = GameDatabase._prepare_records(ids, data, embeddings)
        if len(records) < 1:
            return

        self._clear_data()
        self._create_main_index()

        step = 100
        from_i, to_i = 0, 0
        while from_i < len(records):
            to_i += step
            to_i = min(to_i, len(records))
            print(f"Inserting records {from_i + 1} to {to_i}")
            self._upsert_records(
                namespace=self._namespace, index=self._main_index, records=records
            )
            from_i = to_i

    def describe_index(self):
        return self._main_index.describe_index_stats()

    def _clear_data(self):
        self._delete_index("game-index")

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

        return self.pc.Index(index_name)

    def _create_main_index(self):
        self._main_index = self._create_index(
            "game-index", dimension=self._dimension, metric="cosine"
        )

    def _delete_index(self, index_name: str):
        self.pc.delete_index(index_name)

    def _upsert_records(self, namespace: str, index: Index, records: list[dict]):
        index.upsert(vectors=records, namespace=namespace)
