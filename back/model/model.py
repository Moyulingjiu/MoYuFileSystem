"""
模型
"""
from datetime import datetime

from model.vo import Result
from exception import ReturnObjectReturnCodeNotFound

__all__ = [
    "ReturnObject", "User"
]


class ReturnObject:
    """
    返回类
    """
    code_list = {
        200: 'success',
        201: 'created',
        403: 'forbidden',
        404: 'not found',
        500: 'internal error'
    }

    def __init__(self, code: int = 200, msg: str = 'success', data=None):
        if data is None:
            data = {}
        self.code = code
        self.msg = msg
        self.data = data

    def change_code(self, code: int):
        """
        改变状态码
        :param code:
        :return:
        """
        if code not in self.code_list:
            raise ReturnObjectReturnCodeNotFound('code（%d）未找到' % code)
        self.code = code
        self.msg = self.code_list[code]

    def generate(self):
        """
        生成返回对象
        :return:
        """
        if self.msg == '' and self.code in self.code_list:
            self.msg = self.code_list[self.code]
        return Result(code=self.code, msg=self.msg, data=self.data, timestamp=datetime.now())


class User:
    """
    用户类
    """

    def __init__(self):
        self.username: str = ''  # 用户名
        self.password: str = ''  # 加密后的密码
        self.nickname: str = ''  # 昵称
        self.avatar: str = ''  # 头像
        self.create: datetime = datetime.now()  # 创建时间

        self.admin: bool = False  # 是否是管理员（只有管理员能够创建账户）

    def __setattr__(self, key, value):
        # 对于参数设置必须类型相同才行，避免出现类型错误
        if key in self.__dict__:
            if type(self.__dict__[key]) == type(value):
                self.__dict__[key] = value
        else:
            self.__dict__[key] = value
