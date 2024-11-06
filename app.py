from flask import Flask
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec

app = Flask(__name__)
pc = Pinecone(api_key="3ba8f200-99a7-4b16-8d49-ba671878b6d9")


@app.route('/', methods=["GET"])
def hello_world():
    return str(pc.has_index("my-index"))
