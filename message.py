
import user

messages = []

def SaveMessage(idm: str,idd: str,body: str)->(user.Result,dict):
    message ={
                'idm': idm,
                'idd': idd,
                'body': body
    }
    messages.append(message)
    return user.Result.OK, message

def findMessagebyIdm(idm: str):
    for message in messages:
        if message['idm'] == idm:
            return message
    return None
    
def GetMessagebyIdm(idd: str):
    M = []
    for message in messages:
        if message['idd'] == idd:
            M.append(message)
    return M

"""def GetMessage(idd:str):
    Messages = findMessagebyIdd(idd)
    return"""


"""def modifyMessage(bodyold:str,bodynew:str):"""
    

    