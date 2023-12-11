class callHelp:
    def __init__(self):
        self.callStatus = False

    def call(self):
        self.callStatus = True
        print('Calling Help...')

    def resetCall(self):
        self.callStatus = False

    def isCall(self):
        return self.callStatus
