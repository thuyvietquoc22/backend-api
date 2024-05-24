from app.db.mongo import ton_db

root_character_collection = ton_db.get_collection("root_character")
root_character_collection.create_index("code", unique=True)
