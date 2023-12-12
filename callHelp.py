class callHelp:
    def __init__(self):
        self.callStatus = False

    def call(self):
        self.callStatus = True
        print(
            '==================================================================', end='\n\n')
        print('Calling Help...', end='\n\n')
        print('==================================================================')

    def resetCall(self):
        self.callStatus = False

    def isCall(self):
        return self.callStatus
