from pymongo import MongoClient

# db_client = MongoClient().local | localhost

db_client = MongoClient("mongodb+srv://gustavonievas1:gus123@cluster0.mfxwxdn.mongodb.net/Cluster0?retryWrites=true&w=majority").test