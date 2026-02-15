# arkhe/memory.py
import chromadb
from chromadb.utils import embedding_functions
import time
import json
from typing import List, Dict, Any, Optional

class CortexMemory:
    """
    O Vector DB como córtex permanente do Arkhe(n).
    Implementa memória semântica e aprendizado perpétuo.
    """
    COHERENCE_THRESHOLD = 0.8

    def __init__(self, path="./arkhe_memory"):
        self.client = chromadb.PersistentClient(path=path)
        self.ef = embedding_functions.DefaultEmbeddingFunction()

        # Coleção de insights principais
        self.insights = self.client.get_or_create_collection(
            name="insights",
            embedding_function=self.ef,
            metadata={"hnsw:space": "cosine"}
        )

        # Coleção de entidades e conceitos
        self.entities = self.client.get_or_create_collection(
            name="entities",
            embedding_function=self.ef,
            metadata={"hnsw:space": "cosine"}
        )

        # Coleção de histórico de conversas (para RAG de diálogo)
        self.conversations = self.client.get_or_create_collection(
            name="conversations",
            embedding_function=self.ef
        )

    def memorize_insight(self, topic: str, summary: str, confidence: float, doc_id: str, chunk_id: int = 0, related_nodes: List[str] = None):
        """
        Insere um insight no espaço vetorial se C > THRESHOLD.
        """
        if confidence < self.COHERENCE_THRESHOLD:
            return False

        self.insights.add(
            documents=[summary],
            metadatas=[{
                "topic": topic,
                "confidence": confidence,
                "source_doc": doc_id,
                "chunk_id": chunk_id,
                "timestamp": time.time(),
                "related_nodes": ",".join(related_nodes or [])
            }],
            ids=[f"{doc_id}_c{chunk_id}_{topic}_{int(time.time())}"]
        )
        return True

    def memorize_conversation(self, role: str, content: str, sources: List[str] = None):
        """Persiste turno de conversa."""
        msg_id = f"conv_{int(time.time())}_{role}"
        self.conversations.add(
            documents=[content],
            metadatas=[{
                "role": role,
                "sources": json.dumps(sources or []),
                "timestamp": time.time()
            }],
            ids=[msg_id]
        )

    def recall_for_rag(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """Recuperação semântica para augmentação de contexto."""
        results = self.insights.query(
            query_texts=[query],
            n_results=n_results,
            where={"confidence": {"$gte": self.COHERENCE_THRESHOLD}}
        )

        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        # Converter distância em similaridade (1 - distância normalizada)
        similarities = [1 - d for d in distances]

        context_blocks = []
        for doc, meta, sim in zip(docs, metas, similarities):
            topic = meta.get('topic', 'Unknown')
            source = meta.get('source_doc', 'Unknown')
            confidence = meta.get('confidence', 0)

            context_blocks.append(
                f"[Fonte: {source} | Tópico: {topic} | Confiança: {confidence:.2f} | Similaridade: {sim:.3f}]\n{doc}"
            )

        augmentation = "\n\n".join(context_blocks)

        return {
            "query": query,
            "documents": docs,
            "metadatas": metas,
            "similarities": similarities,
            "augmentation_prompt": f"CONTEXTO RECUPERADO DA MEMÓRIA:\n{augmentation}\n\n"
        }

    def get_stats(self):
        """Retorna estatísticas das coleções."""
        return {
            "insights": self.insights.count(),
            "entities": self.entities.count(),
            "conversations": self.conversations.count()
        }
