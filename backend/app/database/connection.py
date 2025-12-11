import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "markguard_db")

# Mock data store
mock_scans = []

class MockCollection:
    async def count_documents(self, filter=None):
        if filter is None:
            return len(mock_scans)
        elif "$regex" in str(filter):
            # Count counterfeit items
            return sum(1 for scan in mock_scans if "FAIL" in scan.get('status', ''))
        return len(mock_scans)
    
    async def insert_one(self, doc):
        mock_scans.append(doc)
        return type('obj', (object,), {'inserted_id': doc.get('file_id')})()
    
    async def find(self, filter=None):
        return mock_scans

# Use mock collection by default
scan_collection = MockCollection()
