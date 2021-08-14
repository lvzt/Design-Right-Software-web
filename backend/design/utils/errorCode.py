class ErrorCode:
    # 成功状态码
    SUCCESS = 0  # "成功"

    # 参数错误：10001-19999
    PARAM_IS_INVALID = 10001  # 参数无效
    PARAM_IS_BLANK = 10002  # 参数为空
    PARAM_TYPE_BIND_ERROR = 10003  # 参数类型错误
    PARAM_NOT_COMPLETE = 10004  # 参数缺失

    FILE_NAME_INVALID = 11001  # 文件名不合法
    FILE_IS_BLANK = 12001  # 文件不存在

    # 用户错误：20001-29999
    USER_NOT_LOGGED_IN = 20001  # 用户未登录
    USER_LOGIN_ERROR = 20002  # 账号不存在或密码错误
    USER_ACCOUNT_FORBIDDEN = 20003  # 账号已被禁用
    USER_NOT_EXIST = 20004  # 用户不存在
    USER_HAS_EXISTED = 20005  # 用户已存在
    USER_AUTH_NOT_ALLOWED = 20006  # 用户权限不足

    # 业务错误：30001-39999
    CLUSTER_NOT_EXIST = 30001  # 产品簇id不存在
    UTA_NOT_EXIST = 30002
    UTA_VERSION_NOT_EXIST = 30003
    COMPONENT_NOT_EXIST = 30004
    COMPONENT_VERSION_NOT_EXIST = 30005
    BUILD_NOT_EXIST = 30006
    CLUSTER_ID_NOT_MATCH_UTA = 30007
    UTA_ID_NOT_MATCH_UTA = 30008
    UTA_VERSION_NOT_MATCH_UTA = 30009
    COMPONENT_VERSION_NOT_MATCH_UTA = 30010
    BUILD_NOT_MATCH_UTA = 30011
    BUILD_NOT_MATCH_UTA_VERSION = 30012
    TESTER_NOT_EXIST = 30013
    DEVELOPER_NOT_EXIST = 30014
    PRODUCT_MANAGER_NOT_EXIST = 30015
    PROJECT_MANAGER_NOT_EXIST = 30016
    UTA_HAS_BEEN_USED = 30017

    MALL_BRAND_IS_IN_USE = 31001

    # 系统错误：40001-49999
    SYSTEM_INNER_ERROR = 40001  # 系统繁忙，请稍后重试

    # 数据错误：50001-599999
    RESULT_DATA_NONE = 50001  # 数据未找到
    DATA_IS_WRONG = 50002  # 数据有误
    DATA_ALREADY_EXISTED = 50003  # 数据已存在
    FIELD_NOT_EXIST = 50004  # 字段不存在
    TASK_ADD_FAIL = 50005  # 任务添加失败
    DATA_DEL_FAIL = 50006  # 数据删除失败

    # 接口错误：60001-69999
    INTERFACE_INNER_INVOKE_ERROR = 60001  # 内部系统接口调用异常
    INTERFACE_OUTER_INVOKE_ERROR = 60002  # 外部系统接口调用异常
    INTERFACE_FORBID_VISIT = 60003  # 该接口禁止访问
    INTERFACE_ADDRESS_INVALID = 60004  # 接口地址无效
    INTERFACE_REQUEST_TIMEOUT = 60005  # 接口请求超时
    INTERFACE_EXCEED_LOAD = 60006  # 接口负载过高

    ERROR_MSG_MAP = {
        SUCCESS: "success",
        CLUSTER_NOT_EXIST: "CLUSTER id not found",
        UTA_NOT_EXIST: "UTA id not found",
        UTA_VERSION_NOT_EXIST: "UTA Version id not found",
        COMPONENT_NOT_EXIST: "Component id not found",
        COMPONENT_VERSION_NOT_EXIST: "Component Version id not found",
        BUILD_NOT_EXIST: "Build id not found",
        CLUSTER_ID_NOT_MATCH_UTA: "Cluster id not matched with UTA id",
        UTA_ID_NOT_MATCH_UTA: "Uta id not matched with UTA id",
        UTA_VERSION_NOT_MATCH_UTA: "UTA id in UTA Version obj not matched with the one in UTA obj",
        COMPONENT_VERSION_NOT_MATCH_UTA: "UTA id in Component Version obj not matched with the one in UTA obj",
        BUILD_NOT_MATCH_UTA: "Build id not matched with UTA id",
        BUILD_NOT_MATCH_UTA_VERSION: "Build id not matched with UTA Version id",
        MALL_BRAND_IS_IN_USE: "Brand is in use, you should delete mall first",
        FILE_NAME_INVALID: "File name is invalid",
        FILE_IS_BLANK: "File is blank",
        USER_NOT_LOGGED_IN: "Please log in first",
    }

    @staticmethod
    def get_error_msg(error_code):
        return ErrorCode.ERROR_MSG_MAP[error_code]


class CommonError(Exception):
    errno = 0
    errmsg = 0

    def __init__(self, error_code, error_msg=0):
        super().__init__(self)
        self.errno = error_code
        print(error_msg)
        if error_msg != 0:
            self.errmsg = error_msg
        else:
            self.errmsg = ErrorCode.get_error_msg(error_code)

    def __str__(self):
        return 'errno: {},  errmsg: {}'.format(self.errno, self.errmsg)
