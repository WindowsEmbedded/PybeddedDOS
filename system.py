import sys
VER = "0.11-alpha"
dirs = { 
	"/": {
		"system/":"你没有权限",
		"usr/": {
			"fakeroot/":""
		},
		"bin/":"你没有权限"
	}
}
def main():
	global VER
	while True: #死循环
		command = input("fakeroot@localhost $").split()
		try:
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
			elif command[0] == "var":
				if command[1]=="$VER": VER=command[2]
				else:print("Isn't a var")
			else:
				print("Unknown command")
		except IndexError:
			print(end="")

if __name__ == "__main__":
	main()
