import os
def dir2json(dir):
    def dir2json_(dir,dicts):
        for path in os.listdir(dir):
            if os.path.isfile(os.path.join(dir,path)):
                with open(os.path.join(dir,path),'rb') as f:
                    returns[path] = f.read(-1)
            else:
                dicts[path] = {}
                ret = dicts[path]
                dir2json_(os.path.join(dir,path),ret)
    dirs = {'/':{}}
    returns = dirs['/']
    dir2json_(dir,returns)
    return {'/':returns}