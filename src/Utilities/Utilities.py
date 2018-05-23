from sys import platform

LINE_END = '\r\n' if 'win' in platform.lower() else '\n'

class Enum:
    """Provides mechanism for 'enum' object"""

    counter = 0

    def __init__(self):
        self.value = Enum.counter
        Enum.counter += 1

    def __eq__(self, other):
        try:
            return self.value == other.value
        except:
            return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return str(self.value)

def printBanner(msg):
    """Prints msg in ASCII banner style"""
    bookend = '+%s+' % ('-' * (len(msg) + 2 * 1))
    print(bookend)
    print('| %s |' % msg)
    print(bookend)
