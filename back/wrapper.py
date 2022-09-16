"""
包装函数
"""
from threading import Thread


__all__ = [
    "async_function"
]


def async_function(f):
    """
    异步装饰器
    :param f: 函数
    :return: 包装之后的函数
    """

    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper
