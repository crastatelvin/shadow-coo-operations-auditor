import chromadb
import os

class RAGManager:
    def __init__(self, db_path="./chroma_db"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection("business_sops")

    def ingest_sop(self, file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Simple split by heading for more granular RAG
        sections = content.split("##")
        for i, section in enumerate(sections):
            if section.strip():
                self.collection.add(
                    documents=[section],
                    metadatas=[{"source": file_path}],
                    ids=[f"{os.path.basename(file_path)}_{i}"]
                )

    def query_sops(self, query, n_results=2):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results['documents'][0]
