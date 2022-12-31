import sys
VER = "0.1-alpha"
dirs = { #目录
	"/": {
		"system/":"你没有权限",
		"usr/": {
			"fakeroot/":""
		},
		"bin/":"你没有权限"
	}
}
def main():
	while True: #死循环
		command = input("fakeroot@localhost $").split()
		if command[0] == "print":
			for i in range(1,len(command)):
				print(
					command[i].replace("$ver",VER),
					end=" "
				)
			else:
				print() #打印换行
		elif(command[0] == "exit" or
			 command[0] == "shutdown" or
			 command[0] == "quit"
		):
			exit(0)
		else:
			print("Unknown command")

if __name__ == "__main__":
	main()
