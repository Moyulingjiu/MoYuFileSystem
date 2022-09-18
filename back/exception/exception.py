"""
异常类
"""

__all__ = [
    "ReturnObjectReturnCodeNotFound"
]


class FileServerBaseException(Exception):
    """
    基础类
    """

    def __init__(self, msg):
        super.__init__(msg)


class ReturnObjectReturnCodeNotFound(FileServerBaseException):
    """
    返回类未找到返回代码
    """

    def __init__(self, msg):
        super.__init__(msg)
