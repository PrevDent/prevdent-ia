import pymongo
import json
from datetime import datetime
import os
from bson import ObjectId
from bson.json_util import dumps


MONGO_URI = "mongodb://localhost:27017/"  
DATABASE_NAME = "Banco"  
OUTPUT_DIR = "../outputs/MongoDB/"  


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)

def export_collection_to_json(collection, output_path):
    
    try:
        cursor = collection.find({})
        documents = list(cursor)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(documents, f, cls=JSONEncoder, indent=4, ensure_ascii=False)
        
        print(f"✅ Coleção '{collection.name}' exportada com sucesso: {output_path}")
        return True
    
    except Exception as e:
        print(f"❌ Erro ao exportar coleção '{collection.name}': {str(e)}")
        return False

def main():
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    try:
        
        print("🔌 Conectando ao MongoDB...")
        client = pymongo.MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        
        
        collections = db.list_collection_names()
        print(f"Coleções encontradas: {', '.join(collections)}")
        
        
        for collection_name in collections:
            collection = db[collection_name]
            output_file = os.path.join(OUTPUT_DIR, f"{collection_name}.json")
            export_collection_to_json(collection, output_file)
            
        print("Exportação concluída com sucesso!")
        
    except Exception as e:
        print(f"Erro na conexão com o MongoDB: {str(e)}")
    finally:
        if 'client' in locals():
            client.close()
            print("Conexão com MongoDB encerrada.")

if __name__ == "__main__":
    main()