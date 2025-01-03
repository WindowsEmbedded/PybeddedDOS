#!/usr/bin/python3
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
#from exeux import *
import json
import getpass
import socket
import rpy
VER = "0.5"
USERNAME = "root"
PWD = "/usr/%s/home"
var = {}
s = socket.socket()
dirs = { 
	"/": {
		"system/":{
			"sysrc":"""

"""
		},
		"usr/": {
			"fakeroot/":{
				"home/":{}
			}
		},
		"bin/":{}
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
def getPathAndFilename(filename): #return:path,filename
	array = ["",""]
	array[1] = filename.split('/')[-1]
	array[0] = filename.strip("/%s"%array[1])
	return array
def IsaDirectory_t(filename):
	try:
		GetDirectoryContents(filename)
	except Exception:
		return False
	return True

def newdir(pathname=str(),dirname=str()):
	global dirs
	if dirname == "..":
		print("")
		return
	dires = GetDirectoryContents(pathname)
	dires["%s/"%dirname] = {} #新建空字典
	with open("path.json",'w') as f: #写入path.json
		f.write(json.dumps(dirs))
		f.close()
	#print(dirs)

def deldir(pathname=str(),dirname=str()): #原理和上面的差不多
	global dirs 
	dires = GetDirectoryContents(pathname)
	if not "%s/"%dirname in dires: #判断要删除的文件夹是否存在
		print("ERROR: %s isn't in %s"%(dirname,pathname))
	else:
		dires.pop("%s/"%dirname) #删除某字典
		with open("path.json",'w') as f: 
			f.write(json.dumps(dirs))
			f.close()

def ChangePWD(path,name): #改变PWD
	global dirs
	global PWD
	dires = GetDirectoryContents(path)
	if name != ".." and "%s/"%name not in dires: #检测目录是否存在
		print("path %s is not found"%name)
		return
	chgdir = "/"
	pwds = PWD.split("/")
	if name == "..":
		pwds.pop() 
		pwds.pop() #最后一个是空，删两次
	for i in pwds:
		if i=="": continue
		chgdir += "%s/"%i
	if name != "..": chgdir += "%s/"%name #不加这句会显示PWD/../
	#if name == "..":
		
	PWD = chgdir

def NewFile(filename,path):
	global dirs
	if filename == "..":print("");return
	if '/' in filename:print("");return
	dires = GetDirectoryContents(path)
	dires[filename] = "" #新建空字符串
	with open("path.json",'w') as f: #写入path.json
		f.write(json.dumps(dirs))
		f.close()

def ReadFile(filename,path):
	global dirs
	if '/' in filename: print();return #判断要读的是不是文件夹
	dires = GetDirectoryContents(path)
	if filename not in dires.keys(): #判断要读的文件是否存在
		print("%s is not found"%filename)
		return
	return dires[filename]
def WriteFile(filename,path,content):
	global dirs
	if '/' in filename: print();return
	dires = GetDirectoryContents(path)
	dires[filename] = content
	with open("path.json",'w') as f:
		f.write(json.dumps(dirs))
		f.close()

def CreateUser(username):
	global dirs
	if username == "..":
		print("Username '..' is not vaild")
		return
	dires = GetDirectoryContents("/usr")
	dires["%s/"%username] = {}
	dires["%s/"%username]["home/"] = {} #添加home目录
	with open("path.json",'w') as f: #写入path.json
		f.write(json.dumps(dirs))
		f.close()
	
def SwitchUser(username):
	global USERNAME
	USERNAME = username

def setenv(varname,value):
	try:
		var[varname] = value
	except Exception as e:
		print(e)
def getenv(varname):
	return var[varname]
def replaceEnv(command):
	varList = []
	dflag = 0
	bflag = 0
	varname = ""
	for i in range(len(command)):
		for j in range(len(command[i])):
			if bflag == 1 and dflag == 1 and command[i][j] != '}':varname += command[i][j]
			if command[i][j] == '$':dflag = 1
			if command[i][j] == '{' and dflag == 1:bflag = 1
			if command[i][j] == '}':dflag == 0;bflag == 0;varList.append(varname);varname = ''
			
		for k in varList:
			command[i] = command[i].replace("${%s}"%k,var[k])
		else:
			varList.clear()
	return command

def main():
	global VER
	global PWD
	while True: 
		command = input("\033[32m%s@%s\033[0m:\033[36m%s\033[0m$ "%(USERNAME,socket.gethostname(),PWD)).split()
		try:
			command = replaceEnv(command)
			if command[0] == "print":
				for i in range(1,len(command)):
					print(command[i],end='')
				else:
					print() #打印换行
			elif(command[0] == "exit" or
				 command[0] == "shutdown" or
				 command[0] == "quit"
			):
				exit(0)
			elif command[0] == "var":
				if len(command) < 3:
					print(var)
				else:
					setenv(command[1],command[2])
			elif command[0] == "ls":
				for key,value in sorted(GetDirectoryContents(PWD).items(),key=lambda x:x[0]):
					if '/' in key: print("\033[34m%s\033[0m"%key.replace("/",""),end="    ")
					else: print(key,end="	")
				print()
			elif(command[0] == "mkdir" or
				 command[0] == "md" #新建文件夹
			):
				#if command[3] == "--absolute-path": newdir(command[2],command[1])
				newdir(PWD,command[1])
			elif(command[0] == "rmdir" or
				 command[0] == "rd" #删除文件夹
			):
				#if command[3] == "--absoulute-path": deldir(command[2],command[1])
				deldir(PWD,command[1])
			elif command[0]=="cd":
				ChangePWD(PWD,command[1])
			elif command[0] == "touch": #新建文件/清空文件内容
				NewFile(command[1],PWD)
			elif command[0] == "cat": #读取文件内容
				print(ReadFile(command[1],PWD))
			elif command[0] == "newuser": #新建用户
				CreateUser(command[1])
			elif command[0] == "su": #切换用户
				SwitchUser(command[1])
			elif command[0] == "write": #写入
				if command[1] in GetDirectoryContents(PWD).keys():
					WriteFile(command[1],PWD,command[2])
			elif command[0] == "importFile":
				with open(command[1],'r') as f:
					WriteFile(command[2],PWD,f.read())
					f.close()
			elif command[0] == "exec":
				rpy.run(ReadFile(command[1],PWD))
			else:
				print("Unknown command")
		except IndexError:
			print("")

def init():
	global dirs
	global USERNAME
	global PWD
	try:
		with open("path.json") as f:
			dirs = json.load(f)
			usrname = input("Username: ")
			if ("%s/"%usrname in dirs['/']['usr/']):
				#pswd = getpass.getpass("Password: ")
				#if pswd == Decrypt(dirs['/']['usr/']['%s/'%usrname],26):
				if "home/" in dirs['/']['usr/']["%s/"%usrname]: #检测home文件夹是否存在，不存在时执行ls会报错
					USERNAME = usrname
					PWD = "/usr/%s/home/"%USERNAME
					return
				else: print("home path is not found")
				#else: print("Wrong password")
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
