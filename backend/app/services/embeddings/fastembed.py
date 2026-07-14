from fastembed import TextEmbedding


class EmbeddingService:

    def __init__(self):
        # Downloads automatically the first time
        self.model = TextEmbedding(
            model_name="BAAI/bge-small-en-v1.5"
        )

    def embed_document(self, text: str):
        return list(self.model.embed([text]))[0].tolist()

    def embed_query(self, text: str):
        return list(self.model.query_embed(text))[0].tolist()