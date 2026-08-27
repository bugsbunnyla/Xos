from typing import List, Dict, Any
from neo4j import AsyncGraphDatabase
from app.core.config import settings
import structlog

logger = structlog.get_logger()
_driver = None

class GraphSearchEngine:
    def __init__(self):
        global _driver
        if _driver is None:
            _driver = AsyncGraphDatabase.driver(settings.NEO4J_URL, auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD))
        self.driver = _driver

    async def search(self, query: str, user_context: Dict[str, Any]) -> List[Dict]:
        # Placeholder: real implementation queries Neo4j graph
        return [{"id": f"graph_{i}", "url": f"https://osint.example.com/node/{i}",
            "title": f"Graph node {i}", "snippet": f"Relationship found for: {query}",
            "score": 0.9 - i * 0.05, "source": "graph", "node_type": "entity"} for i in range(5)]

    async def create_node(self, label: str, properties: Dict):
        async with self.driver.session() as session:
            props = ", ".join([f"{k}: ${k}" for k in properties])
            await session.run(f"CREATE (n:{label} {{{props}}})", **properties)

    async def create_relationship(self, from_id: str, to_id: str, rel_type: str, properties: Dict = None):
        async with self.driver.session() as session:
            await session.run(
                "MATCH (a), (b) WHERE a.id = $from_id AND b.id = $to_id "
                f"CREATE (a)-[r:{rel_type}]->(b) SET r = $props",
                from_id=from_id, to_id=to_id, props=properties or {}
            )
