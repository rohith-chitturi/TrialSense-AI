from neo4j import GraphDatabase
import os
import logging

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "trialsense_password")

class KnowledgeGraph:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_patient_node(self, patient_id, fhir_id):
        with self.driver.session() as session:
            session.run(
                "MERGE (p:Patient {id: $patient_id, fhir_id: $fhir_id})",
                patient_id=str(patient_id), fhir_id=fhir_id
            )

    def create_disease_relationship(self, patient_id, icd10_code):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (p:Patient {id: $patient_id})
                MERGE (d:Disease {code: $icd10_code})
                MERGE (p)-[:HAS_DISEASE]->(d)
                """,
                patient_id=str(patient_id), icd10_code=icd10_code
            )

# Singleton instance for dependency injection
neo4j_kg = KnowledgeGraph(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
