from pymongo import MongoClient
from typing import List, Dict, Any
import dotenv
import os

dotenv.load_dotenv()


MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

class VPExperimentPersonService():
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.collection = self.db[COLLECTION_NAME]

    def semantic_vp_search(self, normalized_role: str, summary_vector: List[float], batch_size: int = 5000) -> List[Dict[str, Any]]:
        """
        Perform semantic search for VP experiment people and return results with cosine similarity scores.
        
        Args:
            normalized_role: The normalized role to filter by (e.g., "VP")
            summary_vector: The query vector for similarity search
            batch_size: Maximum number of results to return
            
        Returns:
            List of dictionaries containing person data with cosine similarity scores
        """
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "personRoleVector",
                    "filter": {
                        "personNormalizedRole": normalized_role
                    },
                    "queryVector": summary_vector,
                    "numCandidates": batch_size,
                    "limit": batch_size
                }
            },
            {
                "$addFields": {
                    "cosineScore": {
                        "$meta": "vectorSearchScore"
                    }
                }
            },
            {
                "$project": {
                    "personName": 1,
                    "personRole": 1,
                    "cosineScore": 1,
                    "_id": 0
                }
            }
        ]
        
        try:
            # Execute the aggregation pipeline synchronously
            cursor = self.collection.aggregate(pipeline)
            results = []
            
            for document in cursor:
                results.append(document)
            
            return results
            
        except Exception as e:
            print(f"Error in semantic_vp_search: {e}")
            return []
    
    def create_and_push_person(self, person_data: dict):
        """
        Inserts a single person document into the MongoDB collection.
        
        Args:
            person_data: A dictionary representing the VPExperimentPerson object.
        """
        try:
            self.collection.insert_one(person_data)
        except Exception as e:
            print(f"Failed to insert document into MongoDB: {e}")