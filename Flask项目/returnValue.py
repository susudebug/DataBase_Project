
def success(data=None):
    ret = {"success":True,"data":data}
    return ret

def error(status:int,message:str):
    ret = {"success":False,"status":status,"message":message}
    return ret