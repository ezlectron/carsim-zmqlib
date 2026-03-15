

class ZmqBaseMessage():

    MSG_TYPE_REQUEST = "REQ"
    MSG_TYPE_RESPONSE = "RES"

    MSG_STATUS_CODE_OK = "OK"
    MSG_STATUS_CODE_FAIL = "FAIL"

    def __init__(self, type, status):
        self.type = type
        self.status = status

    def getMessageType(self):
        return self.type

    def getStatusCode(self):
        return self.status