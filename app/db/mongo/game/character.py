from app.db.mongo import ton_db

character_collection = ton_db.get_collection("character")
# character_collection.create_index("code", unique=True)
