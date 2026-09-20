class ChunkService:
    def chunk_text(self,text, chunk_size=500,overlap=100):
        chunks=[]
        start=0
        while start<len(text):
            chunk=text[start:start+chunk_size]
            chunks.append(chunk)
            start=start+(chunk_size-overlap)
        return chunks
