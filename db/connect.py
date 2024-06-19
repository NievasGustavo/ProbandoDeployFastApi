from pymongo import MongoClient

# db_client = MongoClient().local | localhost

db_client = MongoClient("mongodb+srv://gustavonievas1:gus123@cluster0.mfxwxdn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&ssl=true").test
