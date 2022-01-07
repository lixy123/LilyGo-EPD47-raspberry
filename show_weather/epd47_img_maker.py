# -*- coding: utf-8 -*-
import sys
import time
import datetime
import os

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import math
import calendar
import weatherAPI_jishuapi 


ink_width=960
ink_height=540

#屏大小:960*540
class Ink_Img_maker:
  font = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",size=90)
  font30 = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",size=30)
  font70 = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",size=70)
  font220 = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",size=220)
  
  def __init__(self):
    self.WeatherValidation=False    
    self.Weather_lastTime=time.time()-100000
    self.Weather_jsonArr=None
    
  def ShowRec(self,ink_draw, x0,y0,x1,y1):
    ink_draw.rectangle((x0,y0,x1,y1),'white','black',width=2)
    
  def ShowRec_line(self,ink_draw, x0,y0,x1,y1):
    self.ShowLine(ink_draw,x0,y0,x1,y0)
    self.ShowLine(ink_draw,x0,y0,x0,y1)
    self.ShowLine(ink_draw,x1,y0,x1,y1)
    self.ShowLine(ink_draw,x0,y1,x1,y1)
    
  def ShowStr(self,ink_draw,mystring,x0,y0,font_char):  
    ink_draw.text((x0, y0), mystring, fill='black',font=font_char)    
            
  def ShowPicture(self,ink_img,picturepath,x0,y0):     
    source_img = Image.open(picturepath).convert("RGB")
    ink_img.paste(source_img,(int(x0),int(y0)))

  def ShowLine(self,ink_draw,x0,y0,x1,y1):
    ink_draw.line([(x0,y0),(x1,y1)],fill='black',width = 2)

  
  def get_duanluo(self, now_font, text):    
    txt_img = Image.new('RGB', (ink_width, ink_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_img)
    # 所有文字的段落
    duanluo = ""
    # 宽度总和
    sum_width = 0
    # 行数
    line_count = 1
    # 行高
    line_height = 0
    for char in text:
      now_width, now_height = draw.textsize(char, now_font)
      sum_width += now_width
      if sum_width > ink_width: # 超过预设宽度就修改段落 以及当前行数
        line_count += 1
        sum_width = now_width #注意此处不能传0,更正bug
        duanluo += '\n'
      duanluo += char
      line_height = max(now_height, line_height)
    if not duanluo.endswith('\n'):
      duanluo += '\n'
    return duanluo, line_height, line_count    
  
  #计算出此字体下显示文字的行数，拆解出每行显示文字列表  
  def split_text(self,now_font,text):
    text = text.replace('\\n','\n')  #处理回车  
    # 按规定宽度分组
    max_line_height, total_lines = 0, 0
    allText = []

    for text_now in text.split('\n'):
      duanluo, line_height, line_count = self.get_duanluo(now_font,text_now)
      print("duanluo=",duanluo,line_height,line_count)
      max_line_height = max(line_height, max_line_height)
      total_lines += line_count
      allText.append((duanluo, line_count))
    line_height = max_line_height
    total_height = total_lines * line_height
    return allText, total_height, line_height
    
  def draw_text(self,fn, now_font, text): 
    allText, total_height, line_height= self.split_text(now_font,text)
    img1 = Image.new("RGB", (ink_width,ink_height),(255,255,255))
    draw1 = ImageDraw.Draw(img1)  
    # 左上角开始
    x, y = 0, 0
    for duanluo, line_count in allText:
      #draw1.text((x, y), duanluo, fill=(255, 255, 255), font=ImgText.font)
      draw1.text((x, y), duanluo, fill=0, font=now_font)
      y += line_height * line_count

    img1 = img1.transpose(Image.ROTATE_180)    
    img1.save(fn,"JPEG")     
  
  def draw_weather(self,fn):  
    if self.WeatherValidation==True:
      #每小时重新获取天气
      if time.time()-self.Weather_lastTime>3600:
        self.WeatherValidation=False
    
    if self.WeatherValidation==False:
      Weather_json=weatherAPI_jishuapi.GetWeatherInfo()
      if Weather_json!=None :#记录请求数据时间
        #print(Weather_json)  
        if Weather_json["status"]!=0:
          print (Weather_json["msg"])
          self.WeatherValidation=False
        else:
          self.jsonArr=Weather_json["result"]
          self.WeatherValidation=True
          self.Weather_lastTime=time.time()
          print (self.jsonArr["city"],self.jsonArr["weather"],self.jsonArr["temp"],self.jsonArr["temphigh"],self.jsonArr["templow"])
    
    if self.WeatherValidation==False:
      print("Weather is not Validation")
      return
              
    AQI=self.jsonArr["aqi"]
    index=self.jsonArr["index"]
    index0=index[0]
    daily=self.jsonArr["daily"]
    day1=daily[1]#明天天气预报
    day2=daily[2]#明天天气预报
    day3=daily[3]#明天天气预报
    day4=daily[4]#明天天气预报 
        
    img1 = Image.new("RGB", (ink_width,ink_height),(255,255,255))
    draw1 = ImageDraw.Draw(img1)    
    
    self.ShowRec(draw1,10,10,ink_width-20,ink_height-8)
    
    self.ShowLine(draw1,10,ink_height/5,ink_width-20,ink_height/5)
    self.ShowLine(draw1,10,ink_height/5*3,ink_width-20,ink_height/5*3)
    self.ShowLine(draw1,10,ink_height-70,ink_width-20,ink_height-70)
      
    self.ShowLine(draw1,ink_width/2,ink_height/5,ink_width/2,ink_height-70)
    self.ShowLine(draw1,ink_width/4,ink_height/5*3,ink_width/4,ink_height-70)
    self.ShowLine(draw1,ink_width/4*3,ink_height/5*3,ink_width/4*3,ink_height-70)
    
    #time show                                                                   
    mylocaltime=time.localtime()
    myclock=time.strftime("%H:%M",mylocaltime)#13:15:03 2017-04-21
    mydate=time.strftime("%Y-%m-%d",mylocaltime)#2017-04-21
    self.ShowStr(draw1,mydate,20,15,self.font70)
    time_now = datetime.datetime.now()
    week_string = [u'星期一',u'星期二',u'星期三',u'星期四',u'星期五',u'星期六',u'星期日'][time_now.isoweekday() - 1]
    self.ShowStr(draw1,week_string,520,15,self.font70)
    
    # 室外温湿度
    self.ShowPicture(img1,"pictures_weather/"+self.jsonArr["img"]+".png",ink_width/16,ink_height/5+120)
    self.ShowStr(draw1,self.jsonArr["city"]+ " " +self.jsonArr["weather"], 20,ink_height/5+10,self.font70)
    #ShowStr(draw1,self.jsonArr["weather"],ink_width/32,ink_height/5*2+50,120)
    self.ShowStr(draw1,self.jsonArr["temp"],ink_width/4+140,ink_height/5+10,self.font70)
    
    self.ShowStr(draw1,"最高"+self.jsonArr["temphigh"]+" "+"最低"+self.jsonArr["templow"],ink_width/4-40,ink_height/5*2+5,self.font30)
    self.ShowStr(draw1,"湿度:"+self.jsonArr["humidity"]+"%",ink_width/4-40,ink_height/5*2+45,self.font30)
    
    self.ShowStr(draw1,self.jsonArr["winddirect"],ink_width/2+20,ink_height/5+10,self.font70)
    self.ShowStr(draw1,self.jsonArr["windpower"],ink_width/2+20,ink_height/5+100,self.font70)
    ## 空气质量

    self.ShowStr(draw1,"PM2.5:"+AQI["pm2_5"],     ink_width/2+190,ink_height/5*2+5,self.font30)
    self.ShowStr(draw1,"空气质量:"+AQI["quality"],ink_width/2+190,ink_height/5*2+45,self.font30)

    # 未来4天天气预报
    self.ShowStr(draw1,day1["date"],ink_width/32,ink_height/5*3+10,self.font30)
    self.ShowStr(draw1,day1["day"]["windpower"],ink_width/32+110,ink_height/5*3+50,self.font30)
    self.ShowStr(draw1,day1["night"]["templow"]+"~"+day1["day"]["temphigh"],ink_width/32+90,ink_height/5*3+90,self.font30)
    self.ShowPicture(img1,"pictures_weather/"+day1["day"]["img"]+".png",ink_width/32,ink_height/5*3+ink_height/10)

    self.ShowStr(draw1,day2["date"],(ink_width-30)/4+ink_width/32,ink_height/5*3+10,self.font30)
    self.ShowStr(draw1,day2["day"]["windpower"],(ink_width-30)/4+ink_width/32+110,ink_height/5*3+50,self.font30)
    self.ShowStr(draw1,day2["night"]["templow"]+"~"+day2["day"]["temphigh"],(ink_width-30)/4+ink_width/32+90,ink_height/5*3+90,self.font30)
    self.ShowPicture(img1,"pictures_weather/"+day2["day"]["img"]+".png",(ink_width-30)/4+ink_width/32,ink_height/5*3+ink_height/10)
   
    self.ShowStr(draw1,day3["date"],(ink_width-30)/4*2+ink_width/32,ink_height/5*3+10,self.font30)
    self.ShowStr(draw1,day3["day"]["windpower"],(ink_width-30)/4*2+ink_width/32+110,ink_height/5*3+50,self.font30)
    self.ShowStr(draw1,day3["night"]["templow"]+"~"+day2["day"]["temphigh"],(ink_width-30)/4*2+ink_width/32+90,ink_height/5*3+90,self.font30)
    self.ShowPicture(img1,"pictures_weather/"+day3["day"]["img"]+".png",(ink_width-30)/4*2+ink_width/32,ink_height/5*3+ink_height/10)
    
    self.ShowStr(draw1,day4["date"],(ink_width-30)/4*3+ink_width/32,ink_height/5*3+10,self.font30)
    self.ShowStr(draw1,day4["day"]["windpower"],(ink_width-30)/4*3+ink_width/32+110,ink_height/5*3+50,self.font30)
    self.ShowStr(draw1,day4["night"]["templow"]+"~"+day2["day"]["temphigh"],(ink_width-30)/4*3+ink_width/32+90,ink_height/5*3+90,self.font30)
    self.ShowPicture(img1,"pictures_weather/"+day4["day"]["img"]+".png",(ink_width-30)/4*3+ink_width/32,ink_height/5*3+ink_height/10)
   
    #记录请求数据时间
    self.ShowStr(draw1,"Last update:"+self.jsonArr["updatetime"],250,ink_height-55,self.font30)  
    img1 = img1.transpose(Image.ROTATE_180) 
    img1.save(fn,"JPEG") 
     
  #屏大小:960*540
  #https://hackaday.io/project/168668-paperdink/log/173710-release-v01
  #https://github.com/rgujju/paperdink/blob/master/Software/paperd.ink/GUI.cpp
  #days_of_month 本月总天数
  #day_offset 第一天是星期几  
  def draw_calender(self,fn):
    img1 = Image.new("RGB", (ink_width,ink_height),(255,255,255))
    draw1 = ImageDraw.Draw(img1)    
    
    myear=datetime.datetime.now().year 
    mmonth=datetime.datetime.now().month #当前月
    mday=datetime.datetime.now().day   #当前日
    monthRange = calendar.monthrange(myear,mmonth)
    days_of_month=monthRange[1] #本月总天数
    day_offset=monthRange[0]+1 #第一天是星期几 (0-6)
    
    #print(str(mmonth) + "," + str(mday) + "," + str(days_of_month) + "," + str(day_offset))
    
    now_x=0
    now_y=0

    num_offset=0
    print_valid = False
    day_now = 1 #待显示的天
  
    #日1-31 数字区左上坐标
    calender_base_x = 110
    calender_base_y = 95    

    #横块
    self.ShowRec(draw1,5,5 , ink_width-5, calender_base_y )  

    #竖块
    self.ShowRec(draw1,5,calender_base_y ,calender_base_x, ink_height-5)
  
  
    self.ShowLine(draw1,5,ink_height-5 , ink_width-5, ink_height-5) 
    self.ShowLine(draw1,ink_width-5,5 ,ink_width-5, ink_height-5) 

    x_offset = 10  #1-30个数字的X偏移
    y_offset = 0  #1-30个数字的y偏移
    
    title = "一二三四五六日"
    #self.ShowStr(draw1,title, calender_base_x+10, 10,self.font70)      
    j=0
    for every_char in title:
      now_x = calender_base_x + j *115 + x_offset
      self.ShowStr(draw1,every_char, now_x, 10,self.font70) 
      j=j+1
      
    #0-5 每周最多31天，5周
    for j in range(6):
      #1-7 7天
      for i in range(1,8):
        if day_now > days_of_month:
          continue
        if (j == 0 and  i == day_offset):
          print_valid = True

        if print_valid: 
          #日的左上坐标

          #每字70像素 (960-120)/7=120 每数字
          now_x = calender_base_x + (i - 1)*115 + x_offset
          now_y = calender_base_y + j *80 + y_offset          
          
          self.ShowStr(draw1, str(day_now), now_x, now_y,self.font70)
         
          if day_now == mday:
            self.ShowRec_line(draw1,now_x - 3,   now_y  + 3,  now_x+83,   now_y+83)
            self.ShowRec_line(draw1,now_x - 5,   now_y  + 5,  now_x+85,   now_y+85) 
            self.ShowRec_line(draw1,now_x - 7,   now_y  + 7,  now_x+87,   now_y+87)            
          day_now =day_now+ 1
  
    # display month
    self.ShowStr(draw1,str(mmonth) ,15, 140,self.font70)
    self.ShowStr(draw1,'月' ,15, 220,self.font70)
    
    # display day
    self.ShowStr(draw1,str(mday) ,15, 320,self.font70)
    self.ShowStr(draw1,'日',15, 400,self.font70)
    img1 = img1.transpose(Image.ROTATE_180) 
    img1.save(fn,"JPEG")    
  
  def draw_clock_digit(self,fn):
    #画布大小 
    #https://www.jb51.net/article/165539.htm
    #1位像素，黑和白，存成8位的像素
    #img1 = Image.new('1', (ink_width,ink_height),1)
    #3× 8位像素，真彩
    img1 = Image.new("RGB", (ink_width,ink_height),(255,255,255))
    draw1 = ImageDraw.Draw(img1)
    
    left_move=220
    top_move=20
    
    #圆心 250,250
    #面积 2,2,238,238  250*2

    # Draw clock face
    draw1.ellipse((left_move+250-248, top_move+250-248,left_move+250+248,top_move+250+248 ), fill = 'black');
    draw1.ellipse((left_move+250-240, top_move+250-240,left_move+250+240,top_move+250+240), fill = 'white');
  
    
    # Draw 12 lines
    for i in range(0, 360-1, 30):    
      sx = math.cos((i - 90) * 0.0174532925);
      sy = math.sin((i - 90) * 0.0174532925);
      x0 = sx * 244 + 250;
      yy0 = sy * 244 + 250;
      x1 = sx * 230 + 250;
      yy1 = sy * 230 + 250;  
      draw1.line([left_move+x0, top_move+yy0, left_move+x1, top_move+yy1], fill='black')

    # Draw 60 dots
    for i in range(0, 360-1, 6): 
      sx = math.cos((i - 90) * 0.0174532925);
      sy = math.sin((i - 90) * 0.0174532925);
      x0 = sx * 232 + 250;
      yy0 = sy * 232 + 250;
      # Draw minute markers
      draw1.ellipse((left_move+x0-2, top_move+yy0-2, left_move+x0+2,top_move+yy0+2),fill ='black')
  
      # Draw main quadrant dots
      if (i % 15 ==0) :
          draw1.ellipse((left_move+x0-8, top_move+yy0-8, left_move+x0+8,top_move+yy0+8 ),fill='black')
      if (i % 45 ==0) :
          draw1.ellipse((left_move+x0-16, top_move+yy0-16, left_move+x0+16,top_move+yy0+16),fill='black')
    #表盘心
    draw1.ellipse((left_move+250-8, top_move+250-8, left_move+250+8, top_move+250+8),fill='black')
    
    timestamp = datetime.datetime.now() 
    
    hh = timestamp.hour % 12
    mm = timestamp.minute
    ss = timestamp.second
    
    # 时针，分针端点坐标
    sdeg = ss * 6; 
    mdeg = mm * 6 + sdeg * 0.01666667; # 0-59 -> 0-360 - includes seconds
    hdeg = hh * 30 + mdeg * 0.0833333; # 0-11 -> 0-360 - includes minutes and seconds
    
    hx = math.cos((hdeg - 90) * 0.0174532925)
    hy = math.sin((hdeg - 90) * 0.0174532925)
    mx = math.cos((mdeg - 90) * 0.0174532925)
    my = math.sin((mdeg - 90) * 0.0174532925)
    #sx = cos((sdeg - 90) * 0.0174532925);
    #sy = sin((sdeg - 90) * 0.0174532925);    
    
    ohx = hx * 150 + 250;
    ohy = hy * 150 + 250;

    omx = mx * 190 + 250;
    omy = my * 190 + 251;      

    draw1.line((left_move+ohx, top_move+ohy, left_move+250,top_move+ 250),width = 20,fill='black')
    draw1.line((left_move+omx, top_move+omy, left_move+250,top_move+ 250),width = 8,fill='black')
    img1 = img1.transpose(Image.ROTATE_180) 
    img1.save(fn,"JPEG")     
     
  def draw_clock(self,fn):
    timestamp = datetime.datetime.now()   
    
    #画布大小 8b
    #1位像素，黑和白，存成8位的像素
    #img1 = Image.new('1', (ink_width,ink_height),1)
    #8位像素，黑白
    #img1 = Image.new('L', (ink_width,ink_height),1)
    #mode ='RGB' 24b 仅这种模式esp32能解析显示
    img1 = Image.new("RGB", (ink_width,ink_height),(255,255,255))
    
    draw1 = ImageDraw.Draw(img1)
    # 左上角开始
    x, y = 180, 0   
    lcd_txt= timestamp.strftime("%H:%M")    
    draw1.text((x,y), lcd_txt,fill=0,font=self.font220)
    x, y = 290, 250   
    lcd_txt= timestamp.strftime("%m月%d日")   
    #print(lcd_txt)    
    draw1.text((x,y), lcd_txt,fill=0,font=self.font)  
    x, y = 330, 400   
    lcd_txt= [u'星期一',u'星期二',u'星期三',u'星期四',u'星期五',u'星期六',u'星期日'][timestamp.isoweekday() - 1] 
    draw1.text((x,y), lcd_txt,fill=0,font=self.font)  
    img1 = img1.transpose(Image.ROTATE_180)    
    img1.save(fn,"JPEG") 

'''
Img_maker = Ink_Img_maker()
#一段文字，\\n特殊字符当作换行
Img_maker.draw_text("draw_text.jpg",Img_maker.font70,\
    u"感谢您为本站写下的评论，您的评论对其它用户来说具有重要的参考价值，\\n所以请认真填写. \\n感谢您为本站写下的评论，您的评论对其它用户来说具有重要的参考价值，\\n所以请认真填写.")
#月历
Img_maker.draw_calender("calender.jpg")
#天气
#Img_maker.draw_weather("weather.jpg")
#数字时钟
#Img_maker.draw_clock_digit("clock_digit.jpg")
#文字显示当前时间
#Img_maker.draw_clock("clock.jpg")
'''