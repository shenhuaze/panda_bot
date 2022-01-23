# panda_bot

服务启动方法：
1.打开一个新的终端，运行"elasticsearch"
2.打开一个新的终端，进入message_server目录，运行"python run_web.py"
3.打开一个新的终端，进入rasa_server目录，先用命令"conda activate rasa-1.10.3"进入"rasa-1.10.3"环境，然后运行"rasa run actions"
4.打开一个新的终端，进入rasa_server目录，先用命令"conda activate rasa-1.10.3"进入"rasa-1.10.3"环境，然后运行"rasa run"

测试服务是否正常启动的方法：
1.进入rasa_server目录，运行"python demo_rasa_server.py"，看打印结果是否正常
2.进入rasa_server目录，运行"python demo_web.py"，看打印结果是否正常