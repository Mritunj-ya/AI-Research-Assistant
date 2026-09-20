import faiss


class VectorStore:

    def __init__(self):
        self.dimension = 384
        self.reset()

    def reset(self):
        self.index = faiss.IndexFlatL2(self.dimension)
        self.chunks = []

    def add_embeddings(self, chunks, embeddings):
        self.chunks.extend(chunks)
        self.index.add(embeddings)

    def search(self, query_embedding, k=8):

        if self.index.ntotal == 0:
            return []

        if len(query_embedding.shape) == 1:
            query_embedding = query_embedding.reshape(1, -1)

        k = min(k, self.index.ntotal)

        distances, indices = self.index.search(
            query_embedding,
            k
        )

        retrieved_chunks = [
            self.chunks[i]
            for i in indices[0]
            if i != -1
        ]

        return retrieved_chunks