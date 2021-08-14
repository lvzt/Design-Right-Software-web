from bson import objectid
from ..utils.utils import *
from ..utils.errorCode import CommonError, ErrorCode
from django.http import QueryDict

# logger = logging.getLogger('custom')    


class BMFileView(ListAPIView):
    database = Db_Design
    collection = Cl_User
    # permission_classes = [AllowAny]
    """添加face信息"""

    def get(self, request, *args, **kwargs):
        collection = self.get_collection()
        result = collection.find()
        result['id'] = str(result.pop('_id'))
        return self.make_response(data=result)

        # filter_list = self.get_filter()
        # # 处理分页
        # page_size, page_number = get_page_params(filter_list)
        # # 处理收索
        # search = filter_list.get("search")
        # filterParams = get_filter_params(search)
        # try:
        #     result = {}
        #     if filterParams:
        #         result = collection.find(filterParams).limit(page_size).skip(page_number)
        #     else:
        #         result = collection.find().limit(page_size).skip(page_number)
        #     if self.serializer_class:
        #         data = self.serializer_class(result, many=True).data
        #     else:
        #         data = list()
        #         for record in result:
        #             record['id'] = str(record.pop('_id'))
        #             if record['gridfsId']:
        #                 record['gridfsId'] = str(record.pop('gridfsId'))
        #             data.append(record)

        #     count = collection.count({})
        #     # count = collection.count(filterParams)
        # except CommonError as e:
        #     logger.debug('list error : {}'.format(e))
        #     raise e

        # resultData = {
        #     "count": count,
        #     "results": data,
        #     "page_number": page_number,
        #     "page_size": page_size,
        # }
        # return self.make_response(data=resultData)


class BMFileAddView(CreateAPIView):
    database = Db_Design
    collection = Cl_User
    # model = BMFileInfo
    # permission_classes = [AllowAny, ]
    # serializer_class = GroupSerializer
    """添加face信息"""

    def post(self, request, *args, **kwargs):
        data = request.data
        if self.serializer_class:
            data = self.serializer_class(data).mongo_data
        else:
            if isinstance(data, QueryDict):
                data = data.dict()

        collection = self.get_collection()
        result = collection.insert_one(data)
        # logger.debug(result)
        if result and result.inserted_id:
            return self.make_response(data={'id': str(result.inserted_id)})

        return self.make_response(errno=ErrorCode.SYSTEM_INNER_ERROR, errmsg='insert record failed')


class BMFileEditView(RetrieveUpdateAPIView):
    database = Db_Design
    collection = Cl_User
    # model = BMFileInfo
    # permission_classes = [AllowAny, ]
    """编辑face信息"""

    # def get(self, request, *args, **kwargs):
    #     pk = kwargs["pk"]
    #     fs = self.get_gridfs()
    #     if not fs.exists({"_id": objectid.ObjectId(pk)}):
    #         return self.make_response(errno=ErrorCode.RESULT_DATA_NONE, errmsg='没有该数据')
    #     data = fs.get(objectid.ObjectId(pk)).read()
    #     if data:
    #         result_data = base64.b64encode(data)
    #     return self.make_response(data={"content": result_data})

    # def get(self, request, *args, **kwargs):
    #     pk = kwargs["pk"]
    #     collection = self.get_connect()
    #     fs = self.get_gridfs()
    #     result = collection.find_one(objectid.ObjectId(pk))
    #     result['id'] = str(result.pop('_id'))
    #
    #     data = fs.get(result["gridfsId"]).read()
    #     # data = dumps(result)
    #     return BaseResponse().make_response(data=data)

    def put(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        try:
            collection = self.get_connect()
            result = collection.find_one(objectid.ObjectId(pk))
            if result is None:
                return self.make_response(errno=ErrorCode.PARAM_IS_INVALID, errmsg='param is invalid : {}'.format(pk))

            data = request.data
            if self.serializer_class:
                data = self.serializer_class(data).mongo_data
            else:
                if isinstance(data, QueryDict):
                    data = data.dict()

            collection.update_one({'_id': objectid.ObjectId(pk)}, {'$set': data})
        except CommonError as e:
            # logger.debug('update error : {}'.format(e))
            raise e
        return self.make_response(data=data)


class BMFileDelView(DestroyAPIView):
    database = Db_Design
    collection = Cl_User
    # model = BMFileInfo
    # permission_classes = [AllowAny, ]
    """删除face信息"""

    def delete(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        resultStr = ""
        try:
            collection = self.get_collection()
            collection.delete_one({'_id': objectid.ObjectId(pk)})
            resultStr = "删除成功"
        except CommonError as e:
            # logger.error('destroy error : {}'.format(e))
            resultStr = 'destroy error : {}'.format(e)
        return self.make_response(data={"id": pk, "msg": resultStr})