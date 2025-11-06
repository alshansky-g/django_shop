import sys

from loguru import logger

logger.remove()
fmt = '<g>{time:YYYY-MM-DD HH:mm:ss}</> | <c>{module}</> | <level>{level}</> | <level>{message}</>'
logger.add(sys.stdout, format=fmt, level='DEBUG')
