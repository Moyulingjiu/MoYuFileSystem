"""
全局配置类
"""
import os
import threading
import time

import yaml
import traceback
from datetime import datetime

from wrapper import async_function

__all__ = [
    "Config", "Logger",
    "config", "logger"
]

log_level_debug: int = 0
log_level_info: int = 1
log_level_warning: int = 2
log_level_error: int = 3
log_level_critical: int = 3


class Config:
    """
    配置类
    """

    def __init__(self, host: str = '0.0.0.0', port: int = 8000,
                 data_path: str = 'data',
                 log_path: str = 'logs', log_reserve_days: int = 15, log_level: int = 0,
                 log_refresh_seconds: float = 0.1,   log_to_console: bool = True,
                 init_admin_username: str = 'root', init_admin_password: str = '123456'):
        self.host = host  # fastapi运行的host
        self.port = port  # fastapi运行的端口

        self.data_path = data_path  # 数据目录
        self.log_path = log_path  # 日志目录
        self.log_reserve_days = log_reserve_days  # 日志保留的天数
        self.log_level = log_level  # 日志级别
        self.log_refresh_seconds = log_refresh_seconds  # 日志的刷新周期
        self.log_to_console = log_to_console

        self.init_admin_username = init_admin_username  # 初始管理员用户名
        self.init_admin_password = init_admin_password  # 初始管理员密码

    def __setattr__(self, key, value):
        # 对于参数设置必须类型相同才行，避免出现类型错误
        if key in self.__dict__:
            if type(self.__dict__[key]) == type(value):
                self.__dict__[key] = value
        else:
            self.__dict__[key] = value


config: Config = Config()  # 配置


class Logger:
    """
    日志类
    """

    def __init__(self):
        self.lock = threading.RLock()  # 同步锁
        self.queue: list[str] = []  # 日志消息队列
        self.close_state: bool = False  # 是否要关闭服务了
        self.log_to_file()

    @async_function
    def log_to_file(self):
        while True:
            if self.close_state:
                break
            if not os.path.exists(config.log_path) or not os.path.isdir(config.log_path):
                self.info("创建日志目录：%s" % config.log_path)
                os.mkdir(config.log_path)
            self.lock.acquire()
            queue = self.queue
            self.queue = []
            self.lock.release()
            f = None
            date: str = ''
            for message in queue:
                log_date: str = message[:10]  # 获取日志写的日期
                if log_date != date:
                    if f is not None:
                        f.close()
                    f = open(os.path.join(config.log_path, log_date + '.log'), 'a', encoding='utf8')
                f.write(message + '\n')
                if config.log_to_console:
                    print(message)
            if f is not None:
                f.close()
            time.sleep(config.log_refresh_seconds)

    def log(self, level: str, msg: str):
        function_stack = traceback.extract_stack()
        last_call = function_stack[-3]
        call_info = '%s@%d' % (last_call.filename, last_call.lineno)
        log_message = '%s - [%-9s] %s: %s' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), level, call_info, msg)
        self.lock.acquire()
        self.queue.append(log_message)
        self.lock.release()

    def debug(self, msg: str):
        if config.log_level <= log_level_debug:
            self.log('debug', msg)

    def info(self, msg: str):
        if config.log_level <= log_level_info:
            self.log('info', msg)

    def warning(self, msg: str):
        if config.log_level <= log_level_warning:
            self.log('warning', msg)

    def error(self, msg: str):
        if config.log_level <= log_level_error:
            self.log('error', msg)

    def critical(self, msg: str):
        if config.log_level <= log_level_critical:
            self.log('critical', msg)


logger: Logger = Logger()  # 日志


def load_config():
    """
    加载配置
    :return:
    """
    global config
    with open('config.yml', 'r', encoding='utf8') as f:
        config_yaml = yaml.safe_load(f.read())
        if 'file_server' in config_yaml:
            if 'host' in config_yaml['file_server']:
                config.host = config_yaml['file_server']['host']
            if 'port' in config_yaml['file_server']:
                config.port = config_yaml['file_server']['port']
            if 'data_path' in config_yaml['file_server']:
                config.data_path = config_yaml['file_server']['data_path']
            if 'log_path' in config_yaml['file_server']:
                config.log_path = config_yaml['file_server']['log_path']
            if 'log_reserve_days' in config_yaml['file_server']:
                config.log_reserve_days = config_yaml['file_server']['log_reserve_days']
            if 'log_level' in config_yaml['file_server']:
                config.log_level = config_yaml['file_server']['log_level']
            if 'log_refresh_seconds' in config_yaml['file_server']:
                config.log_refresh_seconds = config_yaml['file_server']['log_refresh_seconds']
            if 'log_to_console' in config_yaml['file_server']:
                config.log_to_console = config_yaml['file_server']['log_to_console']

            if 'init_admin' in config_yaml['file_server']:
                if 'username' in config_yaml['file_server']['init_admin']:
                    config.init_admin_username = config_yaml['file_server']['init_admin']['username']
                if 'password' in config_yaml['file_server']['init_admin']:
                    config.init_admin_password = config_yaml['file_server']['init_admin']['password']
        if not os.path.exists(config.data_path) or not os.path.isdir(config.data_path):
            logger.info("创建数据目录：%s" % config.data_path)
            os.mkdir(config.data_path)
        if not os.path.exists(config.log_path) or not os.path.isdir(config.log_path):
            logger.info("创建日志目录：%s" % config.log_path)
            os.mkdir(config.log_path)


load_config()
