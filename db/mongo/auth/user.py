from db.mongo import ton_db

user_collection = ton_db.get_collection("users")
user_collection.create_index("tele_id", unique=True)
