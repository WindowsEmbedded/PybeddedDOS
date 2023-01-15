"""
	Exit Status Code				Description
	0x0(0)								  无异常
	0x1(1)								未知错误
	0x60(96)							按下了^C
	0x61(97)							内存溢出
	0x62(98)					无权限读/写某文件
	0x7e(126)							指令错误

"""
import sys
import json
VER = "0.11-alpha"
USERNAME = "root"
PWD = "/usr/%s/home"
dirs = { 
	"/": {
		"system/":{},
		"usr/": {
			"fakeroot/":""
		},
		"bin/":"你没有权限"
	}
}

def GetDirectoryContents(dirname=str()) -> dict: #获取某目录的文件
	global dirs
	dictdir = ['/']
	dictdires = dirs["/"]
	for i in dirname.split("/"):
		if i == '': continue
		dictdir.append(i)
		dictdires = dictdires["%s/"%i]
	return dictdires

def IsaDirectory(filename) -> bool: return '/' in filename #判断是否为文件夹 

def main():
	global VER
	global PWD
	while True: #死循环
		command = input("%s@localhost %s$ "%(USERNAME,PWD)).split()
		try:
			if command[0] == "print":
				for i in range(1,len(command)):
					print(
						command[i].replace("$VER",VER) ,
						end=" "
					)
				else:
					print() #打印换行
			elif(command[0] == "exit" or
				 command[0] == "shutdown" or
				 command[0] == "quit"
			):
				exit(0)
			elif command[0] == "var":
				if command[1]=="$VER": VER=command[2]
				else:print("Isn't a var")
			elif command[0] == "ls":
				for key,value in GetDirectoryContents(PWD).items():
					if '/' in key: print("\033[34m%s\033[0m"%key.replace("/",""),end="	")
					else: print(key,end="	")
				print()
					
			else:
				print("Unknown command")
		except IndexError:
			print(end="")

def init():
	global dirs
	global USERNAME
	global PWD
	try:
		with open("path.json") as f:
			dirs = json.load(f)
			usrname = input("Username: ")
			if "%s/"%usrname in dirs['/']['usr/']:
				USERNAME = usrname
				PWD = "/usr/%s/home/"%USERNAME
				return
			else: print("%s's path is not found"%usrname)
			sys.exit(0xff)
			#except SystemExit: pass
	except PermissionError:
		print("path.json:Permission denied")
		sys.exit(0x62)
	except FileNotFoundError:
		print("Warning: path.json is not found")
		with open("path.json",'w') as f:
			f.write(json.dumps(dirs))
			f.close()
		init()


if __name__ == "__main__":
	init()
	try:
		main()
	except KeyboardInterrupt:
		print("You're pressed ^C")
		sys.exit(0x60)
	except MemoryError:
		sys.exit(0x61)
