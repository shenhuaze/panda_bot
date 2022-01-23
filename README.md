# panda_bot

服务启动方法：
1.打开一个新的终端，运行"elasticsearch"
2.打开一个新的终端，进入rasa_server目录，先用命令"conda activate rasa-1.10.3"进入"rasa-1.10.3"环境，然后运行"rasa run actions"
3.打开一个新的终端，进入rasa_server目录，先用命令"conda activate rasa-1.10.3"进入"rasa-1.10.3"环境，然后运行"rasa run"
4.打开一个新的终端，进入message_server目录，运行"python run_web.py 80"
5.打开一个新的终端，进入message_server目录，运行"./natapp -authtoken=4618c8c1c83f124e"
6.进入微信公众平台->登录->设置与开发->基本配置->服务器配置->修改配置，将上一步生成的动态网址，
例如"http://bf5pbs.natappfree.cc"，替换掉微信公众平台网页上的"URL"框中的对应网址，点击提交，看是否显示"提交成功"


测试服务是否正常启动的方法：
1.进入rasa_server目录，运行"python demo_rasa_server.py"，看打印结果是否正常
2.进入rasa_server目录，运行"python demo_web.py"，看打印结果是否正常
3.进入微信公众号"胖达机器人"，进入对话界面，给公众号发送消息，看是否有回应