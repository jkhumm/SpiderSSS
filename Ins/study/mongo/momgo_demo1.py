import pymongo as pymongo

#client = pymongo.MongoClient('192.168.1.148',27017)
from bson import ObjectId

client = pymongo.MongoClient('mongodb://root:root_123456@192.168.1.148:27017')
# 指定数据库
myDb = client['demo1']
# 存放数据的数据库表名
first_collection = myDb['my_first_collection']

# data1 = {"id":"10086","name":"heian",'age':1}
#
# data_list = [{"id":"10086","name":"heian",'age':2},{"id":"10086","name":"heian",'age':3}]
# # 数据库或者表不存在会自动创建
# _id = first_collection.insert_one(data1)
# print(_id) # <pymongo.results.InsertOneResult object at 0x00000245589FFB88>
# res = first_collection.insert_many(data_list)
# print(res) # <pymongo.results.InsertManyResult object at 0x0000024558A3A708>
# data1 = {"id":"10086","name":"heian",'age':4}
# res = first_collection.insert(data1) # 619f51f1fa9b48019c230120 打印的是返回的_id
# print(res)

#查询
# res = first_collection.find({"name":"heian","age":{"$gte": 3}})
# for i in res:
#     print(i)
#
# one = first_collection.find_one({"_id": ObjectId('619f51f1fa9b48019c230120')})
# print(one)

# 删除
# print(first_collection.remove({"age":4})) #{'n': 1, 'ok': 1.0}

# 修改
query_condition = {"_id": ObjectId('619f515afa9b486140e53db2')}
update_condition = {"$set":{"age":28}}

re = first_collection.update_one(query_condition, update_condition)
print(re) #<pymongo.results.UpdateResult object at 0x000001AB634AEBD0>





