from odi.core.types import Evidence, KnowledgeItem

class KnowledgeFabric:
    def __init__(self) -> None:
        self._items: dict[str, KnowledgeItem] = {}
        self._evidence: dict[str, Evidence] = {}

    def add_knowledge(self, item: KnowledgeItem) -> None:
        self._items[item.id] = item

    def add_evidence(self, evidence: Evidence) -> None:
        self._evidence[evidence.id] = evidence

    def get(self, item_id: str) -> KnowledgeItem:
        return self._items[item_id]

    def evidence(self, evidence_id: str) -> Evidence:
        return self._evidence[evidence_id]

    def search(self, topic: str) -> tuple[KnowledgeItem, ...]:
        q = topic.lower()
        return tuple(i for i in self._items.values() if q in i.topic.lower() or q in str(i.content).lower())
