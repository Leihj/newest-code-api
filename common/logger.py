# -*- coding: utf-8 -*-
# @File    : logger.PY
# @Date    : 2019/7/9-11:19
# @Author  : leihuijuan
# @Emali   : huijuan_lei@163.com

import logging
import time
from common import contants_path


def get_log(log_name):
    logger=logging.getLogger(log_name)
    logger.setLevel("DEBUG")
    # logger.setLevel(logging.INFO)

    # 获取时间戳
    # get_timestamp=time.strftime("%Y-%m-%d-%H-%M-%S".format(time.localtime(time.time())))
    #
    # 设置全部的log日志级别的文件名
    all_log_name=contants_path.all_log+"/{}.log".format(time.strftime('%Y%m%d%H%M%S'))

    #设置error的log日志级别的文件名
    error_log_name=contants_path.err_log+"/{}.log".format(time.strftime('%Y%m%d%H%M%S'))

    # 创建输出渠道
    # 设置一个收集所以日志的文件渠道
    fh=logging.FileHandler(all_log_name,encoding="utf-8")
    fh.setLevel("DEBUG")


    #设置一个收集error日志的文件渠道
    eh=logging.FileHandler(error_log_name,encoding="utf-8")
    eh.setLevel("ERROR")


    #设置有一个输出到控制台的渠道
    console=logging.StreamHandler()
    console.setLevel("DEBUG")

    #设置输出日志的格式
    fmt='%(asctime)s -%(name)s -%(levelname)s -%(message)s -[%(filename)s:%(lineno)d]'
    formatter=logging.Formatter(fmt=fmt)
    #设置fh文件收集的格式
    fh.setFormatter(formatter)
    # 设置eh文件收集的格式
    eh.setFormatter(formatter)
    #设置console文件收集的格式
    console.setFormatter(formatter)

    #给logger添加渠道
    logger.addHandler(fh)
    logger.addHandler(eh)
    logger.addHandler(console)

    # 把logger返回
    return logger


if __name__ == '__main__':
    log=get_log(__file__)
    log.debug("debug")
    log.info("info信息")
    log.warning("warning信息")
    log.error("error信息")
    log.critical("critical信息")