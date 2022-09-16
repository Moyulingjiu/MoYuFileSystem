"""
全局配置类
"""
import os
import yaml

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
                 init_admin_username: str = 'root', init_admin_password: str = '123456'):
        self.host = host  # fastapi运行的host
        self.port = port  # fastapi运行的端口

        self.data_path = data_path  # 数据目录
        self.log_path = log_path  # 日志目录
        self.log_reserve_days = log_reserve_days  # 日志保留的天数
        self.log_level = log_level  # 日志级别

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
        pass

    def debug(self, msg: str):
        pass

    def info(self, msg: str):
        pass

    def warning(self, msg: str):
        pass

    def error(self, msg: str):
        pass

    def critical(self, msg: str):
        pass


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

            if 'init_admin' in config_yaml['file_server']:
                if 'username' in config_yaml['file_server']['init_admin']:
                    config.init_admin_username = config_yaml['file_server']['init_admin']['username']
                if 'password' in config_yaml['file_server']['init_admin']:
                    config.init_admin_password = config_yaml['file_server']['init_admin']['password']


load_config()
