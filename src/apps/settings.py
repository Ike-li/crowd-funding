from datetime import timedelta

from cassandra.cluster import Cluster
from cassandra.query import dict_factory


##################################################
# 导入:
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()




##################################################


def create_cass_session():
    """
    :return:
    """
    # # 服务器的数据库
    # cluster = Cluster(["81.69.189.115"])
    # # 本地数据库
    # # cluster = Cluster(['127.0.0.1'])
    # # 备用数据库
    # # cluster = Cluster([''])
    # session = cluster.connect()
    # session.default_fetch_size = 1000  # 设置默认读取行数
    # session.row_factory = dict_factory  # 返回 rows 的数据格式为字典(dict)
    # return session

    # 初始化数据库连接:
    engine = create_engine("mysql+mysqlconnector://root:crowd@47.106.213.201:3306/user")
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)

    Base.metadata.create_all(engine)  # 创建表结构

    # 创建session对象:
    session = DBSession()
    return session


cass_session = create_cass_session()


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = "123qwe"

    PERMANENT_SESSION_LIFETIME = timedelta(
        minutes=20
    )  # 设置 session 持续时间（20分钟），默认 permanent 为 True
    SESSION_REFRESH_EACH_REQUEST = True  # session中存储的是字典时，修改字典内部元素时，会造成数据不更新，这时使用 SESSION_REFRESH__EACH_REQUEST = True


class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
