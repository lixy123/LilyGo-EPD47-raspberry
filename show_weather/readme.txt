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