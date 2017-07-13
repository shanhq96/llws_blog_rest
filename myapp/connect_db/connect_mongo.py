# coding=utf-8
from pymongo import MongoClient
from bson.objectid import ObjectId


class ConnectMongoDB():
    """连接MongoDB,且提供插入,更新,删除,查询的操作"""

    def __init__(self, host='localhost', port=27017):
        """建立MongoDB数据库连接    默认为localhost,端口为27017"""
        self.client = MongoClient(host, port)
        dbName = 'blog'  # 数据库名称
        self.db = self.client[dbName]  # 连接所需数据库,test为数据库名

    def get_collection(self, tableName):
        """获得表的集合collection;tableName为表名"""
        return self.db[tableName]  # 连接所用集合，也就是我们通常所说的表，test为表名

    def insert_list(self, collection, list2save):
        """将数据列表插入到数据库中"""
        print('向%s中插入数据%s' % (collection.name, list2save))
        return collection.insert(list2save)

    def update_data(self, collection, condition, newData,upsert=False,multi=False):
        """根据条件更新表中数据"""
        print('更新%s中数据;条件:%s;新数据:%s' % (collection, condition, newData))
        return collection.update(condition, newData,upsert=upsert,multi=multi)

    def find_data(self, collection, condition={}):
        """根据条件筛选数据库"""
        return collection.find(condition)

    def find_one_data(self, collection, _id):
        return collection.find_one({"_id": ObjectId(_id)})

    def remove_all_data(self, collection):
        print('删除全部数据')
        return collection.remove()

    def remove_one_data(self,collection,condition):
        print('删除:%s条件:%s' % (collection, condition))
        return collection.remove(condition)