import pymongo
from backend import settings
import gridfs
# import logging

# logger = logging.getLogger('custom')

Db_Design = 'db_design'
Cl_User = 'cl_user'

def get_mongo_client():
    host = settings.MONGO_DATABASE["HOST"]
    port = settings.MONGO_DATABASE["PORT"]
    username = settings.MONGO_DATABASE["USERNAME"]
    password = settings.MONGO_DATABASE["PASSWORD"]
    authentication_source = settings.MONGO_DATABASE["AUTHENTICATION_SOURCE"]
    client = pymongo.MongoClient(
        host=host,
        port=port,
        username=username,
        password=password,
        authSource=authentication_source
    )
    return client


# class BaseResponse:

#     def make_response(self, exception=None, errno=0, errmsg='', data=None, **kwargs):
#         ret = {
#             "errno": 0,
#             "errmsg": "",
#             "data": {}
#         }
#         if data is None:
#             data = dict()
#         # if kwargs is not None and isinstance(kwargs, dict) and len(kwargs) > 0:
#         #     data.update(kwargs)
#         self.ret = {
#             "errno": 0,
#             "errmsg": "",
#             "data": {}
#         }

#         if 'status' in kwargs:
#             del kwargs['status']
#         if exception is not None and isinstance(exception, CommonError):
#             self.ret["errno"] = exception.errno
#             self.ret["errmsg"] = exception.errmsg
#             self.ret["data"] = data
#             return Response(self.ret)
#         self.ret["errno"] = errno
#         self.ret["errmsg"] = errmsg
#         self.ret["data"] = data
#         return Response(self.ret, **kwargs)


class MongoPagination:
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page_number'
    max_page_size = 100

class MongoBase:
    mongo_client = None
    collection = None
    collection_fsfiles = None
    database = None
    unique = []

    def ping_mongo(self):
        res = self.mongo_client.admin.command('ping')
        return res and res['ok']

    def get_database(self):
        if not (self.mongo_client and self.ping_mongo()):
            self.mongo_client = get_mongo_client()
        db = self.mongo_client[self.database]
        return db

    def get_collection(self):
        if not (self.mongo_client and self.ping_mongo()):
            self.mongo_client = get_mongo_client()
        db = self.mongo_client[self.database]
        return db[self.collection]

    def get_gridfs(self):
        """ 文件操作 """
        if not (self.mongo_client and self.ping_mongo()):
            self.mongo_client = get_mongo_client()
        db = self.mongo_client[self.database]

        fs = gridfs.GridFS(db)
        return fs

    def get_fsfiles_collection(self):
        """fs.files collection"""
        if not (self.mongo_client and self.ping_mongo()):
            self.mongo_client = get_mongo_client()
        db = self.mongo_client[self.database]
        return db[self.collection_fsfiles]

    def get_custom_collection(self, collection):
        """获取自定义collection"""
        if not (self.mongo_client and self.ping_mongo()):
            self.mongo_client = get_mongo_client()
        db = self.mongo_client[self.database]
        return db[collection]


class CreateAPIView(BaseCreate, BaseApiView, MongoBase):
    pass


class ListAPIView(BaseList, BaseApiView, MongoBase):
    def get_filter(self):
        filter_params = dict()
        for key in self.request.query_params:
            filter_params[key] = self.request.query_params[key]
        return filter_params
    # pass


class RetrieveAPIView(BaseRetrieve, BaseApiView, MongoBase):
    def get_filter(self):
        filter_params = dict()
        for key in self.request.query_params:
            filter_params[key] = self.request.query_params[key]
        return filter_params
    # pass


class DestroyAPIView(BaseDestroy, BaseApiView, MongoBase):
    pass


class UpdateAPIView(BaseUpdate, BaseApiView, MongoBase):
    pass


class ListCreateAPIView(BaseList, BaseCreate, BaseApiView, MongoBase):
    def get_filter(self):
        filter_params = dict()
        for key in self.request.query_params:
            filter_params[key] = self.request.query_params[key]
        return filter_params
    pass


class RetrieveUpdateAPIView(BaseRetrieve, BaseUpdate, BaseApiView, MongoBase):
    def get_filter(self):
        filter_params = dict()
        for key in self.request.query_params:
            filter_params[key] = self.request.query_params[key]
        return filter_params
    pass


class RetrieveDestroyAPIView(BaseRetrieve, BaseDestroy, BaseApiView, MongoBase):
    def get_filter(self):
        filter_params = dict()
        for key in self.request.query_params:
            filter_params[key] = self.request.query_params[key]
        return filter_params
    pass


class RetrieveUpdateDestroyAPIView(BaseRetrieve, BaseUpdate, BaseDestroy, BaseApiView, MongoBase):
    def get_filter(self):
        filter_params = dict()
        for key in self.request.query_params:
            filter_params[key] = self.request.query_params[key]
        return filter_params
    pass