from app.db.mongo import ton_db

user_collection = ton_db.get_collection("users_bag")
user_collection.create_index("user_id", unique=True)
