# import logging

from rest_framework import exceptions, status

from django.conf import settings
from django.http import Http404
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
from rest_framework.settings import api_settings

from django.core.exceptions import PermissionDenied
# from .httpRequest import HttpRequest
from .errorCode import CommonError, ErrorCode
# from apps.rbac.permissions import CommonBasePermission
# from customFilterBackend import CustomSearchFilter

# logger = logging.getLogger('custom')


class BaseResponse:

    def make_response(self, exception=None, errno=0, errmsg='', data=None, **kwargs):
        ret = {
            "errno": 0,
            "errmsg": "",
            "data": {}
        }
        if data is None:
            data = dict()
        # if kwargs is not None and isinstance(kwargs, dict) and len(kwargs) > 0:
        #     data.update(kwargs)
        self.ret = {
            "errno": 0,
            "errmsg": "",
            "data": {}
        }

        if 'status' in kwargs:
            del kwargs['status']
        if exception is not None and isinstance(exception, CommonError):
            self.ret["errno"] = exception.errno
            self.ret["errmsg"] = exception.errmsg
            self.ret["data"] = data
            return Response(self.ret)
        self.ret["errno"] = errno
        self.ret["errmsg"] = errmsg
        self.ret["data"] = data
        return Response(self.ret, **kwargs)


class BaseApiView(BaseResponse, GenericAPIView):

    # filter_backends = [CustomSearchFilter]

    # def __init__(self, *args, **kwargs):
    #     if len(self.permission_classes) > 0 and AllowAny in self.permission_classes:
    #         pass
    #     else:
    #         permission_classes = [i for i in self.permission_classes]
    #         permission_classes.insert(0, CommonBasePermission)
    #         self.permission_classes = permission_classes
    #     super(BaseApiView, self).__init__(*args, **kwargs)

    # def initial(self, request, *args, **kwargs):
    #     super(BaseApiView, self).initial(request, *args, **kwargs)
    #     # init http server with header
    #     token = request.META.get("HTTP_AUTHORIZATION")
    #     http_request = HttpRequest.get_singleton()
    #     http_request.set_token(token)

    def handle_exception(self, exc):
        if isinstance(exc, CommonError):
            return self.make_response(exc)
        # if isinstance(exc, (exceptions.NotAuthenticated,
        #                     exceptions.AuthenticationFailed)):
        #     # WWW-Authenticate header for 401 responses, else coerce to 403
        #     auth_header = self.get_authenticate_header(self.request)

        #     if auth_header:
        #         exc.auth_header = auth_header
        #     else:
        #         exc.status_code = status.HTTP_403_FORBIDDEN

        # exception_handler = self.get_exception_handler()

        context = self.get_exception_handler_context()
        response = self.exception_handler(exc, context)

        if response is None:
            self.raise_uncaught_exception(exc)
            return self.make_response(CommonError(ErrorCode.INTERFACE_INNER_INVOKE_ERROR, '未知内部错误'))
        response.exception = True
        return response

    def raise_uncaught_exception(self, exc):
        if settings.DEBUG:
            request = self.request
            renderer_format = getattr(request.accepted_renderer, 'format')
            use_plaintext_traceback = renderer_format not in ('html', 'api', 'admin')
            request.force_plaintext_errors(use_plaintext_traceback)
        # logger.exception(exc)

    def exception_handler(self, exc, context):
        errno = ErrorCode.SUCCESS
        if isinstance(exc, Http404):
            exc = exceptions.NotFound()
            errno = ErrorCode.INTERFACE_ADDRESS_INVALID
        elif isinstance(exc, PermissionDenied):
            exc = exceptions.PermissionDenied()
            errno = ErrorCode.USER_AUTH_NOT_ALLOWED

        if isinstance(exc, exceptions.APIException):
            headers = {}
            if getattr(exc, 'auth_header', None):
                headers['WWW-Authenticate'] = exc.auth_header
            if getattr(exc, 'wait', None):
                headers['Retry-After'] = '%d' % exc.wait

            if isinstance(exc, exceptions.NotAuthenticated):
                errno = ErrorCode.USER_NOT_LOGGED_IN

            if isinstance(exc, exceptions.AuthenticationFailed):
                errno = ErrorCode.USER_AUTH_NOT_ALLOWED

            if isinstance(exc.detail, (list, dict)):
                data = exc.detail
            else:
                data = {'detail': exc.detail}
            if errno == ErrorCode.SUCCESS:
                errno = ErrorCode.INTERFACE_INNER_INVOKE_ERROR
            errmsg = ''
            if isinstance(data, dict):
                for info in data:
                    errmsg += '{} : {}。'.format(info, data[info])
            else:
                for info in data:
                    errmsg += '{}。'.format(data[info])

            return self.make_response(errno=errno, errmsg=errmsg, data=data, status=exc.status_code, headers=headers)

        return None


class CreateModelMixin:

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return self.make_response(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class ListModelMixin:

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.make_response(data=self.get_paginated_response(serializer.data).data)

        serializer = self.get_serializer(queryset, many=True)
        return self.make_response(data=serializer.data)


class RetrieveModelMixin:

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return self.make_response(data=serializer.data)


class UpdateModelMixin:

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return self.make_response(data=serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin:

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return self.make_response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class BaseCreate(CreateModelMixin):

    def _post(self, request, *args, **kwargs):
        return request, args, kwargs

    def post(self, request, *args, **kwargs):
        request, args, kwargs = self._post(request, *args, **kwargs)
        return self.create(request, *args, **kwargs)


class BaseList(ListModelMixin):

    def _get(self, request, *args, **kwargs):
        return request, args, kwargs

    def get(self, request, *args, **kwargs):
        request, args, kwargs = self._get(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)


class BaseRetrieve(RetrieveModelMixin):

    def _get(self, request, *args, **kwargs):
        return request, args, kwargs

    def get(self, request, *args, **kwargs):
        request, args, kwargs = self._get(request, *args, **kwargs)
        return self.retrieve(request, *args, **kwargs)


class BaseDestroy(DestroyModelMixin):

    def _delete(self, request, *args, **kwargs):
        return request, args, kwargs

    def delete(self, request, *args, **kwargs):
        request, args, kwargs = self._delete(request, *args, **kwargs)
        return self.destroy(request, *args, **kwargs)


class BaseUpdate(UpdateModelMixin):

    def _put(self, request, *args, **kwargs):
        return request, args, kwargs

    def put(self, request, *args, **kwargs):
        request, args, kwargs = self._put(request, *args, **kwargs)
        return self.update(request, *args, **kwargs)

    def _patch(self, request, *args, **kwargs):
        return request, args, kwargs

    def patch(self, request, *args, **kwargs):
        request, args, kwargs = self._patch(request, *args, **kwargs)
        return self.partial_update(request, *args, **kwargs)


class CreateAPIView(BaseCreate, BaseApiView):
    pass


class ListAPIView(BaseList, BaseApiView):
    pass


class RetrieveAPIView(BaseRetrieve, BaseApiView):
    pass


class DestroyAPIView(BaseDestroy, BaseApiView):
    pass


class UpdateAPIView(BaseUpdate, BaseApiView):
    pass


class ListCreateAPIView(BaseList, BaseCreate, BaseApiView):
    pass


class RetrieveUpdateAPIView(BaseRetrieve, BaseUpdate, BaseApiView):
    pass


class RetrieveDestroyAPIView(BaseRetrieve, BaseDestroy,  BaseApiView):
    pass


class RetrieveUpdateDestroyAPIView(BaseRetrieve,  BaseUpdate, BaseDestroy, BaseApiView):
    pass
