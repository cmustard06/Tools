#!/usr/bin/env python
# @Author: cmustard
# @Description: 用于编码或者解码URL，hex，md5，Base64的工具

import base64
import urllib.parse
import binascii
import hashlib
import logging
import tkinter
from functools import partial


def getLogger():
    "获取一个日志处理器，用于记录文件错误"
    logger = logging.Logger("encode")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    fh = logging.FileHandler("encodeLog.log")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger


class Encoding(object):
    def __init__(self, raw_data):
        self._logger_ = getLogger()
        self._raw_data_ = raw_data

    # url编码
    def url_encode(self):
        "url 编码"
        try:
            url_encode_data = urllib.parse.quote(self._raw_data_, ":/?=")
        except Exception as e:
            self._logger_.error("url_encode an error occurred:" + str(e))
            url_encode_data = "None"
        # print(url_encode_data)
        return url_encode_data

    # url解码
    def url_decode(self):
        "url解码"
        try:
            url_decode_data = urllib.parse.unquote(self._raw_data_)
        except Exception as e:
            self._logger_.error("url_decode an error occurred:" + str(e))
            url_decode_data = "None"

        return url_decode_data

    # 十六进制编码
    def hex_encode(self):
        " 十六进制编码 "
        try:
            hex_encode_data = binascii.b2a_hex(self._raw_data_.encode("utf-8"))

            hex_encode_data = "0x".encode("utf-8") + hex_encode_data

        except Exception as e:
            self._logger_.error("hex_encode an error occurred:" + str(e))
            hex_encode_data = b"None"
        return hex_encode_data.decode("utf-8")

    def hex_decode(self):
        "十六进制解码"
        try:
            if self._raw_data_.startswith("0x"):
                self._raw_data_ = self._raw_data_[2:]

            hex_decode_data = binascii.a2b_hex(self._raw_data_.encode("utf-8"))

            hex_decode_data = hex_decode_data.decode("utf-8")
        except Exception as e:
            self._logger_.error("hex_decode en error occurred:" + str(e))
            hex_decode_data = "None"
        return hex_decode_data

    def md5_encry(self):
        "md5 加密"
        try:
            hash = hashlib.md5()
            hash.update(self._raw_data_.encode("utf-8"))
            md5_encry_data = hash.hexdigest()
        except Exception as e:
            self._logger_.error("md5_encry an errors occurred:" + str(e))
            md5_encry_data = "None"
        return md5_encry_data

    def bs64_encode(self):
        "base64 加密"
        try:
            bs64_encode_data = base64.b64encode(self._raw_data_.encode("utf-8")).decode("utf-8")

        except Exception as e:
            self._logger_.error("bs64_encode an errors occurred:" + str(e))
            bs64_encode_data = "None"
        return bs64_encode_data

    def bs64_decode(self):
        "base64 解码"
        try:
            bs64_decode_data = base64.b64decode(self._raw_data_.encode("utf-8")).decode("utf-8")

        except Exception as e:
            self._logger_.error("bs64_decode an errors occurred:" + str(e))
            bs64_decode_data = "None"
        return bs64_decode_data


class ToolUI(object):
    def __init__(self):
        self.tk = tkinter.Tk()

    def run(self):
        self.tk.title("数据编码解码工具  --by glamor")
        # 函数柯里化
        # 标签 可以显示文本和位图
        self._Label = partial(tkinter.Label, self.tk)
        # 文本  文本控件；用于显示多行文本
        self._Text = partial(tkinter.Text, self.tk)
        # 按钮控件；在程序中显示按钮。
        self._Button = partial(tkinter.Button, self.tk)
        # 输入文本
        self._Entry = partial(tkinter.Entry, self.tk)

        self.raw_data = tkinter.StringVar()  # 定义变量
        self.label_raw_data = self._Label(text="原始数据")
        self.entry_raw_data = self._Entry(textvariable=self.raw_data)

        # url解码
        self.label_url_decode = self._Label(text="URL解码结果")
        self.text_url_decode = self._Text(height="3", width=100)

        # base64解码
        self.label_bs64_decode = self._Label(text="Base64解码结果")
        self.text_bs64_decode = self._Text(height="3", width=100)

        # hex解码
        self.label_hex_decode = self._Label(text="Hex解码结果")
        self.text_hex_decode = self._Text(height="3", width=100)

        self.label_split = self._Label(text="编码", font=15)
        # 编码
        # url编码
        self.label_url_encode = self._Label(text="URL编码结果")
        self.text_url_encode = self._Text(height="3", width=100)

        # base64编码
        self.label_bs64_encode = self._Label(text="Base64编码结果")
        self.text_bs64_encode = self._Text(height="3", width=100)

        # hex编码
        self.label_hex_encode = self._Label(text="Hex编码结果")
        self.text_hex_encode = self._Text(height="3", width=100)

        # md5加密
        self.label_md5_encode = self._Label(text="MD5加密结果")
        self.text_md5_encode = self._Text(height="3", width=100)

        # 按钮
        self.button_encode = self._Button(text="编码", width=10, command=self.__encode)
        self.button_decode = self._Button(text="解码", width=10, command=self.__decode)
        # 原始数据网格
        self.label_raw_data.grid(row=0, column=0, padx=10, pady=10)
        self.entry_raw_data.grid(row=0, column=1, sticky="we")
        self.tk.grid_columnconfigure(0, weight=100)

        # 网格
        self.label_url_decode.grid(row=1, column=0, padx=5, pady=5)
        self.text_url_decode.grid(row=1, column=1, padx=5, pady=5)
        self.label_bs64_decode.grid(row=2, column=0, padx=5, pady=5)
        self.text_bs64_decode.grid(row=2, column=1, padx=5, pady=5)
        self.label_hex_decode.grid(row=3, column=0, padx=5, pady=5)
        self.text_hex_decode.grid(row=3, column=1, padx=5, pady=5)

        self.label_split.grid(row=4, column=0)

        self.label_url_encode.grid(row=5, column=0, padx=5, pady=5)
        self.text_url_encode.grid(row=5, column=1, padx=5, pady=5)
        self.label_bs64_encode.grid(row=6, column=0, padx=5, pady=5)
        self.text_bs64_encode.grid(row=6, column=1, padx=5, pady=5)
        self.label_hex_encode.grid(row=7, column=0, padx=5, pady=5)
        self.text_hex_encode.grid(row=7, column=1, padx=5, pady=5)
        self.label_md5_encode.grid(row=8, column=0, padx=5, pady=5)
        self.text_md5_encode.grid(row=8, column=1, padx=5, pady=5)

        self.button_encode.grid(row=9, column=0)
        self.button_decode.grid(row=9, column=1)

        self.tk.mainloop()

    def __decode(self):
        "将元数据解码后输出到对应的文本框中"
        raw_data = self.raw_data.get()
        de = Encoding(raw_data)
        print(self.text_url_decode)
        bs64_decode = de.bs64_decode()
        url_decode = de.url_decode()
        hex_decode = de.hex_decode()
        self.__get_result_(self.text_url_decode, url_decode)
        self.__get_result_(self.text_bs64_decode, bs64_decode)
        self.__get_result_(self.text_hex_decode, hex_decode)

    def __encode(self):
        "将元数据编码后输出到对应的文本框中"
        raw_data = self.raw_data.get()
        en = Encoding(raw_data)
        # print(self.text_url_decode)
        bs64_encode = en.bs64_encode()
        url_encode = en.url_encode()
        hex_encode = en.hex_encode()
        md5_encode = en.md5_encry()
        self.__get_result_(self.text_url_encode, url_encode)
        self.__get_result_(self.text_bs64_encode, bs64_encode)
        self.__get_result_(self.text_hex_encode, hex_encode)
        self.__get_result_(self.text_md5_encode, md5_encode)

    def __get_result_(self, text, data):
        "该函数用于将编码的结果返回给前端进行展示"
        # 清除text框中上一次编码的数据
        text.delete(0.0, tkinter.END)
        # #assert raw_data == '123456'
        text.insert(tkinter.END, data)
        text.see(tkinter.END)
        text.update()

    def __str__(self):
        return "工具UI"




if __name__ == '__main__':
    ui = ToolUI()
    ui.test()
    # ui.run()
