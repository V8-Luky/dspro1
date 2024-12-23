"""This module contains the GameDatabase class, which is used to interact with the Pinecone API."""

import time
import numpy as np

from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from pinecone import Index

DEFAULT_METRIC = "cosine"


class GameDatabase:
    """
    Represents a database to store game embeddings and their metadata.

    Attributes:
        pc: The Pinecone client.
        namespace: The namespace of the database.
        indexes: A dictionary of indexes, mapping index names to their corresponding Pinecone Index objects.
    """
    @staticmethod
    def _prepare_records(
        ids: list[str], metadata_records: list[dict], embeddings: list
    ) -> list:
        """
        Converts the input data into a list of records that can be inserted into a Pinecone index.

        Args:
            ids: A list of game IDs.
            metadata_records: A list of dictionaries, each containing metadata about a game.
            embeddings: A list of embeddings, each corresponding to a game.

        Returns:
            A list of records, each containing an ID, an embedding, and metadata.
        """
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

    def __init__(self, api_key: str, indexes: dict[str, int] = None) -> None:
        self._pinecone = Pinecone(api_key=api_key)
        self._namespace = "steam-games"
        self._indexes = dict()
        if indexes:
            for key, value in indexes.items():
                self._create_index(
                    index_name=key, dimension=value, metric=DEFAULT_METRIC)

    def describe_index(self, index_name: str) -> dict:
        """
        Retrieves a description of the specified index.

        Args:
            index_name: The name of the index.

        Returns:
            A dictionary containing information about the index.
        """
        return self._get_index(index_name).describe_index_stats()

    def get_by_id(self, index_name: str, id_: str) -> list:
        """
        Retrieves the record of a game by its ID.

        Args:
            index_name: The name of the index in which to search.
            id_: The ID of the game.

        Returns:
            The record of the game containing the id, embedding and metadata.
        """
        index = self._get_index(index_name)

        results = index.fetch(
            namespace=self._namespace,
            ids=[id_],
        )

        return results["vectors"][id_]

    def get_ids(self, index_name: str) -> list:
        """
        Retrieves all the IDs in the specified index.

        This may be a lenghty operation if the index contains a large number of records.

        Args:
            index_name: The name of the index.

        Returns:
            A list of all the IDs in the index.        
        """
        all_ids = []
        for page in list(self._get_index(index_name).list(namespace=self._namespace)):
            all_ids.extend(page)

        return all_ids

    def get_similar(self, index_name: str, embedding: np.ndarray, k: int = 1) -> list:
        """
        Retrieves the k most similar records to the specified embedding.

        Args:
            index_name: The name of the index.
            embedding: The embedding to compare against.
            k: The number of similar records to retrieve.

        Returns:
            A list of the k most similar records.
        """
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

    def get_similarity(self, index_name: str, name: str, embedding: np.ndarray) -> dict:
        """
        Retrieves the similarity for a specified game to a given embedding.

        Args:
            index_name: The name of the index in which to search.
            name: The name of the game.
            embedding: The embedding to compare against.

        Returns:
            A matching result containing the similarity score of the game and the record of the game.
        """
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

    def load_data(self, index_name: str, ids: list[str], data: list[dict], embeddings: list, slice_size: int = 100):
        """
        Loads data into the specified index.

        The data is inserted in batches of size slice_size as to not overstep the api 
        limiations of Pinecone.
        If the index already exists, it is cleared before inserting the new data. And if 
        it does not exist, it is created.

        Args:
            index_name: The name of the index.
            ids: A list of game IDs.
            data: A list of dictionaries, each containing metadata about a game.
            embeddings: A list of embeddings, each corresponding to a game.
            slice_size: The number of records to insert in each batch.
        """
        records = GameDatabase._prepare_records(ids, data, embeddings)
        if len(records) < 1:
            return

        self._clear_data(index_name=index_name)

        dimension = len(embeddings[0])
        index = self._create_index(
            index_name=index_name, dimension=dimension, metric=DEFAULT_METRIC)

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

    def _clear_data(self, index_name: str):
        self._delete_index(index_name=index_name)

    def _create_index(self, index_name: str, dimension: int, metric: str) -> Index:
        if not self._pinecone.has_index(index_name):
            self._pinecone.create_index(
                name=index_name,
                dimension=dimension,
                metric=metric,
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )

        while not self._pinecone.describe_index(index_name).status["ready"]:
            time.sleep(1)

        self._indexes[index_name] = self._pinecone.Index(index_name)
        return self._get_index(index_name)

    def _delete_index(self, index_name: str):
        if not self._pinecone.has_index(index_name):
            return
        self._pinecone.delete_index(index_name)

    def _get_index(self, index_name: str) -> Index:
        return self._indexes[index_name]

    def _upsert_records(self, namespace: str, index: Index, records: list[dict]):
        index.upsert(vectors=records, namespace=namespace)
