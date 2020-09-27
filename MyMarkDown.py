#coding:utf-8

import re
import markdown

class MyMarkDown:
    __table = None
    __header = """
|Log Name|Log Type|Sub Log Type|Description|
|-|-|-|-|
"""

    __line = "|%s|`%s`|%s|%s|\n"

    __log_enum_pattern = re.compile('^([a-zA-Z0-9_]+)\s*\(\s*([0-9]+)\s*,\s*([0-9]+)\s*,\s*[a-zA-Z0-9_]+\s*,\s*"(.+)"\s*[\),\s]+$')

    __exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite','markdown.extensions.tables','markdown.extensions.toc']

    def __init__(self):
        """构造方法"""
        self.__table = self.__header
        pass

    def addLine(self, name, type_name, sub_type="", desc=""):
        """添加一行"""
        self.__table = self.__table + self.__line % (name, type_name, sub_type, desc)
        pass

    def addLineByString(self, data):
        """添加一行，入参是原始字符串，自行切割、解析
        data=AROUNDAPI_DEL_SUBWAY_LINE(39002, 2000, ERROR_SUB_LOG_TYPE, "水星API-删除地铁线")
        """

        m = self.__log_enum_pattern.match(data)
        if m:
            self.addLine(m.group(1), m.group(2), m.group(3), m.group(4))
        else:
            pass

    def getAll(self):
        html_text = markdown.markdown(self.__table, extensions=self.__exts)
        return html_text

if __name__ == '__main__':
    s = MyMarkDown()
    s.addLine("avc", "xxx", "x22", "asdasd")
    s.addLine("a222vc", "xxx", "x22", "asdasd")
    # s.addLineByString('AROUNDAPI_DEL_SUBWAY_LINE(39002, 2000, ERROR_SUB_LOG_TYPE, "test for show")')
    print(s.getAll())