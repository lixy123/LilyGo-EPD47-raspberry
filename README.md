# LilyGo-EPD47-raspberry
LilyGo-EPD47 树莓派版本的python脚本

功能：运行在树莓派上的两个演示程序,显示天气，微信公众号操作树莓派.
硬件：lilygo的4.7寸墨水屏的树莓派接口版本


目录show_weather

功能:
墨水屏显示天气

墨水屏烧录此处程序:
https://github.com/Xinyuan-LilyGO/LilyGo-EPD47/tree/master/examples/spi_driver

树莓派安装：
1.所有文件拷入树莓派 /home/pi目录
2.打开https://www.jisuapi.com/api/weather/ 
3.申请免费天气key,  替换文件 weatherAPI_jishuapi.py  appkey后的***
4.cityid 换成本地城市ID
5.epd47_img_maker.py 中用的中文字体，通过如下命令安装中文字体
sudo apt-getinstall fonts-wqy-zenhei  

树莓派上运行：
python3 epd_weather.py


自动定时运行:
crontab -e
设定时间自动执行 python3 epd_weather.py


目录weixin_server

功能：
微信公众号后台
运行后手机打开微信关注公众号，给公众号发送clock, weather, calender等文字显示相应内容，
见文件 weixin_memo_epd47.py  查询关键字 dowithcmd
注：树莓派上怎么用python运行微信公众号查百度。

墨水屏烧录此处程序:
https://github.com/Xinyuan-LilyGO/LilyGo-EPD47/tree/master/examples/spi_driver

树莓派安装：
1.所有文件拷入树莓派 /home/pi目录
2.打开https://www.jisuapi.com/api/weather/ 
3.申请免费天气key,  替换文件 weatherAPI_jishuapi.py  appkey后的***
4.cityid 换成本地城市ID
5.epd47_img_maker.py 中用的中文字体，通过如下命令安装中文字体
sudo apt-getinstall fonts-wqy-zenhei  
6. 配置用树莓派搭建微信公众号的环境，参考:
https://www.h3399.cn/201712/523858.html
注: 大部分人一般没有公网IP, 可以用frp软件内网穿透

树莓派上运行：
frp工具将本地端口 7005印射到微信公众号的域名
python3 weixin_memo_epd47.py frp端口号


自动定时运行:
crontab -e
设定时间自动执行 python3 epd_weather.py
