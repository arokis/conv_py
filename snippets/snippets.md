# Initialising Classes dynamically by name-call

"""
class Test(object):
    def __init__(self, t):
        self.test = t
    
    def hello(self):
        print self.test


a = {"Testing" : "Test"}
print(type(a['Testing']))

print(type(a['Testing']).__name__)

b = vars()[a['Testing']]('s')
b.hello()
"""
