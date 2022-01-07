# LilyGo-EPD47-raspberry
LilyGo-EPD47 树莓派版本的python脚本 <br/>

<b>一.功能： </b> <br/>
运行在树莓派上的两个演示程序,显示天气，微信公众号操作树莓派. <br/>

<b>二.硬件： </b> <br/>
lilygo的4.7寸墨水屏的树莓派接口版本 <br/>

<img src= 'https://github.com/lixy123/LilyGo-EPD47-raspberry/blob/main/ink1.jpg?raw=true' /> <br/>
<img src= 'https://github.com/lixy123/LilyGo-EPD47-raspberry/blob/main/ink2.jpg?raw=true' /> <br/>

 演示视频<br/>
 https://github.com/lixy123/LilyGo-EPD47-raspberry/raw/main/ink.mp4<br/>

<b>三.演示程序</b>  <br/>
<b>(1)目录show_weather </b> <br/>

功能: <br/>
墨水屏显示天气 <br/>

墨水屏烧录此处程序: <br/>
https://github.com/Xinyuan-LilyGO/LilyGo-EPD47/tree/master/examples/spi_driver

树莓派安装： <br/>
1.所有文件拷入树莓派 /home/pi目录 <br/>
2.打开https://www.jisuapi.com/api/weather/  <br/>
3.申请免费天气key,  替换文件 weatherAPI_jishuapi.py  appkey后的*** <br/>
4.cityid 换成本地城市ID <br/>
5.epd47_img_maker.py 中用的中文字体，通过如下命令安装中文字体 <br/>
sudo apt-getinstall fonts-wqy-zenhei   <br/>

树莓派上运行： <br/>
python3 epd_weather.py <br/>


自动定时运行: <br/>
crontab -e <br/>
设定时间自动执行 python3 epd_weather.py <br/>


<b>(2) 目录weixin_server</b> <br/>

功能： <br/>
微信公众号后台 <br/>
运行后手机打开微信关注公众号，给公众号发送clock, weather, calender等文字显示相应内容， <br/>
见文件 weixin_memo_epd47.py  查询关键字 dowithcmd <br/>
注：树莓派上怎么用python运行微信公众号查百度。 <br/>

墨水屏烧录此处程序: <br/>
https://github.com/Xinyuan-LilyGO/LilyGo-EPD47/tree/master/examples/spi_driver <br/>

树莓派安装： <br/>
1.所有文件拷入树莓派 /home/pi目录 <br/>
2.打开https://www.jisuapi.com/api/weather/  <br/>
3.申请免费天气key,  替换文件 weatherAPI_jishuapi.py  appkey后的*** <br/>
4.cityid 换成本地城市ID <br/>
5.epd47_img_maker.py 中用的中文字体，通过如下命令安装中文字体 <br/>
sudo apt-getinstall fonts-wqy-zenhei   <br/>
6. 配置用树莓派搭建微信公众号的环境，参考: <br/>
https://www.h3399.cn/201712/523858.html <br/>
注: 大部分人一般没有公网IP, 可以用frp软件内网穿透 <br/>

树莓派上运行： <br/>
frp工具将本地端口 7005印射到微信公众号的域名 <br/>
python3 weixin_memo_epd47.py frp端口号 <br/>


自动定时运行: <br/
crontab -e <br/>
设定时间自动执行 python3 epd_weather.py <br/>
