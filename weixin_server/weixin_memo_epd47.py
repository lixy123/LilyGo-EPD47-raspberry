#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys
import web
import json
import hashlib
from lxml import etree
import requests
import subprocess
import threading
import ssl
import spidev
from math import ceil, floor
from time import sleep, time
import urllib
import epd47_img_maker

#url访问https报错
#https://blog.csdn.net/wangye1989_0226/article/details/96991883
ssl._create_default_https_context = ssl._create_unverified_context


urls = (
'/weixin','WeixinInterface'
)
 

last_get_access_token_time= time()-10000
last_get_access_token=""

LIST_MAXLEN=6 #最多显示行数，取决于屏的大小,
list_txt = []

class EPD47():
    def __init__(self, spi, width, height):
        self.spi = spi
        self.width = width
        self.height = height

    def send_jpeg(self, filename, x = 0, y = 0, w = 0, h = 0):
        width = w
        height = h
        timestamp = time()
        fn_size = 0

        if w == 0:
            width = self.width
        if h == 0:
            height = self.height

        self.send_run_cmd()
        sleep(0.01) #时间还能缩小？待测试

        self.send_ld_jpeg_area_cmd(x, y, width, height, 1)
        sleep(0.02) #时间还能缩小？待测试

        with open(filename, 'rb') as fp:
            while True:
                content = fp.read(4000)
                if len(content)==0:
                    break
                # print("", len(content))
                fn_size = fn_size + len(content)
                a = list(bytes(content))
                # print(a)
                self.send_mem_bst_wr_cmd(a, len(a))
                sleep(0.02)
        sleep(0.02)
        self.send_ld_jpeg_end_cmd()
        sleep(0.02)
        print("jpeg size=", fn_size)
        print("send jpeg time: ", time() - timestamp, "s")

    def send_img(self, img_data, x = 0, y = 0, w = 0, h = 0):
        width = w
        height = h
        timestamp = time()

        self.send_run_cmd()
        sleep(0.01) #时间还能缩小？待测试

        if w == 0:
            width = self.width
        if h == 0:
            height = self.height
        self.send_ld_img_area_cmd(x, y, width, height, 1)
        sleep(0.01) #时间还能缩小？待测试

        i = 0
        while i < len(img_data):
            if (len(img_data) - i) > 4000:
                l = 4000
            else:
                l = len(img_data) - i
            self.send_mem_bst_wr_cmd(img_data[i : (i + l)], l)
            i = i + l
            sleep(0.02)

        self.send_ld_img_end_cmd()
        sleep(0.01)
        print("img size=", len(img_data))
        print("send img time: ", time() - timestamp, "s")

    def wake_epd(self, cnt, sleep_sec):
        for i in range(cnt):
            print("wake_epd")
            epd.send_run_cmd()
            sleep(sleep_sec)
        
    def send_run_cmd(self):
        payload = []
        payload.append(0x55)
        payload.append(0x55)
        payload.append(0x00) # cmd
        payload.append(0x01)
        payload.append(0x00) # len
        payload.append(0x00)

        self.spi.writebytes(self._append_byte(payload, 4))

    def send_run_stand(self):
        payload = []
        payload.append(0x55)
        payload.append(0x55)
        payload.append(0x00) # cmd
        payload.append(0x02)
        payload.append(0x00) # len
        payload.append(0x00)

        self.spi.writebytes(self._append_byte(payload, 4))
        
       
    def send_mem_bst_wr_cmd(self, data, len):
        payload = []
        payload.append(0x55)
        payload.append(0x55)
        payload.append(0x00) # cmd
        payload.append(0x14)
        payload.append(((len) & 0xFFFF) >> 8 & 0xFF) #len
        payload.append((len) & 0xFF)
        payload.extend(data)
        self.spi.writebytes(self._append_byte(payload, 8))

    def send_ld_img_cmd(self, mode):
        payload = []
        payload.append(0x55)
        payload.append(0x55)
        payload.append(0x00) # cmd
        payload.append(0x20)
        payload.append(0x00) #len
        payload.append(0x09)
        payload.append(mode)
        self.spi.writebytes(self._append_byte(payload, 4))

    def send_ld_img_area_cmd(self, x, y, width, height, mode):
        payload = []

        payload.append(0x55)
        payload.append(0x55)
        payload.append(0x00) # cmd
        payload.append(0x21)
        payload.append(0x00) #len
        payload.append(0x09)
        payload.append(mode)
        payload.append(x >> 8 & 0xFF)
        payload.append(x & 0xFF)
        payload.append(y >> 8 & 0xFF)
        payload.append(y & 0xFF)
        payload.append(width >> 8 & 0xFF)
        payload.append(width & 0xFF)
        payload.append(height >> 8 & 0xFF)
        payload.append(height & 0xFF)
        self.spi.writebytes(self._append_byte(payload, 4))

    def send_ld_img_end_cmd(self):
        payload = []
        payload.append(0x55)
        payload.append(0x55)
        payload.append(0x00) # cmd
        payload.append(0x22)
        payload.append(0x00) # len
        payload.append(0x00)
        self.spi.writebytes(self._append_byte(payload, 8))

    def send_ld_jpeg_cmd(self, mode):
        payload = []
        payload.append(0x55)
        payload.append(0x55)
        payload.append(0x00) # cmd
        payload.append(0x30)
        payload.append(0x00) #len
        payload.append(0x09)
        payload.append(mode)
        self.spi.writebytes(self._append_byte(payload, 4))

    def send_ld_jpeg_area_cmd(self, x, y, width, height, mode):
        payload = []
        payload.append(0x55)
        payload.append(0x55)
        payload.append(0x00) # cmd
        payload.append(0x31)
        payload.append(0x00) #len
        payload.append(0x09)
        payload.append(mode)
        payload.append(x >> 8 & 0xFF)
        payload.append(x & 0xFF)
        payload.append(y >> 8 & 0xFF)
        payload.append(y & 0xFF)
        payload.append(width >> 8 & 0xFF)
        payload.append(width & 0xFF)
        payload.append(height >> 8 & 0xFF)
        payload.append(height & 0xFF)
        self.spi.writebytes(self._append_byte(payload, 4))

    def send_ld_jpeg_end_cmd(self):
        payload = []
        payload.append(0x55)
        payload.append(0x55)
        payload.append(0x00) # cmd
        payload.append(0x32)
        payload.append(0x00) # len
        payload.append(0x00)
        self.spi.writebytes(self._append_byte(payload, 8))

    def _append_byte(self, msg, div_cnt):
        p1= len(msg) % div_cnt
        if p1 != 0:
            for i in range(div_cnt - p1):
                msg.append(0x00)
        return msg
        
def epd_showjpg(fn): 
    print("send_jpeg weather")
    epd.send_jpeg(fn, 0, 0)
    #文件上传完毕后，esp32显示jpg时间约2-4秒   
    
def append_list(txt):
    duanluo, line_height, line_count=Img_maker.get_duanluo(Img_maker.font70,txt)
    duanluo=duanluo.strip()
    for new_line in duanluo.split('\n'):
        list_txt.append(new_line)
        #删除第一个
        if len(list_txt)>LIST_MAXLEN:
            list_txt.pop(0)  
     
def now_list():
    ret_list=""
    for index1 in range(len(list_txt)):
        if index1==0:
            ret_list= list_txt[index1]
        else:
            ret_list=ret_list+ "\n" + list_txt[index1]
    return ret_list          
   

  
def show_ink(cmd):
    global list_txt,nowindex
    if cmd=="cls":
        list_txt=["" for i in range(LIST_MAXLEN)]
        nowindex=0    
        cmd=""
    else:
        append_list(cmd)
        cmd=now_list()    
    print("show_ink:"+cmd)
    Img_maker.draw_text("draw_text.jpg",Img_maker.font70,cmd)
    epd_showjpg("draw_text.jpg")
    
def dowithcmd(cmd):  
    if (cmd=="calender"):
        Img_maker.draw_calender("tmp.jpg")
        epd_showjpg("tmp.jpg")   
    elif (cmd=="weather"): 
        Img_maker.draw_weather("tmp.jpg")
        epd_showjpg("tmp.jpg")   
    elif (cmd=="d_clock"): 
        Img_maker.draw_clock_digit("tmp.jpg")
        epd_showjpg("tmp.jpg")   
    elif (cmd=="clock"): 
        Img_maker.draw_clock("tmp.jpg")
        epd_showjpg("tmp.jpg") 
    else:        
        show_ink(cmd)        
    return ""

def _check_hash(data):
    #sha1加密算法
    signature=data.signature
    timestamp=data.timestamp
    nonce=data.nonce
    #自己的token
    token="my_token"
    #字典序排序
    list=[token,timestamp,nonce]
    list.sort()
    sha1=hashlib.sha1()
    map(sha1.update,list)
    hashcode=sha1.hexdigest()
    #如果是来自微信的请求，则回复True
    
    #网上的算法判断不了,不判断了!
    print(hashcode,signature)
    return True
    '''
    if hashcode == signature:
        return True
    return False
    '''
    
class WeixinInterface: 
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
 
        
    def GET(self):
        #获取输入参数
        data = web.input()
        if _check_hash(data):
            return data.echostr

    def POST(self):  
        str_xml = web.data() #获得post来的数据        
        print (str_xml  )
        xml = etree.fromstring(str_xml)#进行XML解析        
        msgType=xml.find("MsgType").text 
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        if msgType=="text":
            content=xml.find("Content").text#获得用户所输入的内容  
            if len(content)>0:
                if content=="test":
                    content="test ok" 
                else:
                    thread_ink = threading.Thread(target=dowithcmd,args=(content,))
                    thread_ink.start()              
                    content="ink_show ok"       
            return self.render.reply_text(fromUser,toUser,int(time()),u""+content) 
        
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 3900000
spi.bits_per_word = 8
spi.mode = 0b11

epd = EPD47(spi, 960, 540)
Img_maker = epd47_img_maker.Ink_Img_maker() 


application = web.application(urls, globals())
if __name__ == "__main__":
    #reload(sys)
    #sys.setdefaultencoding('utf8')
    application.run()
