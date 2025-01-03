import system
gglobals = {}
def get_shebang(script):
    if script[0] == "#" and script[1] == '!':
        i=2
        line=""
        while script[i] != '\n':
            line+=script[i]
        file,args = line.split(" ")
        return file,args
    else:
        return "",""
def open_o(file,mode):
    return 0
def run(script):
    try:
        files,args = get_shebang(script)
        if files == '':
            exec(script,gglobals)
        else:
            gglobals['args'] = args
            gglobals['args'] += script
            exec(system.ReadFile(system.getPathAndFilename(files)[1],system.getPathAndFilename(files)[0]),gglobals)
    except SystemExit as e:
        globals['exitstatus'] = e
    except Exception as e:
        print(e)
    

gglobals = {
    "VER":system.VER,
    "USERNAME":system.USERNAME,
    "PWD":system.PWD,
    "setenv":system.setenv,
    "open":open_o
}
gglobals.update(globals())