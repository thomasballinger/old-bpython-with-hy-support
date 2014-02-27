
from pygments.token import Token

from pygments.lexers import get_lexer_by_name

def get_name_of_current_hy_function(current_line):

    # Get the name of the current function and where we are in
    # the arguments
    class Group(object):
        def __init__(self, opening, name='', argnum=-2):
            self.name = name
            self.argnum = argnum
            self.opening = opening
        def __repr__(self):
            return '%s%s%s %s' % (self.opening, self.name if self.name else '???', self.argnum, '___ '*(max(self.argnum - 1, 0)) + 'CURARG)')
    stack = []
    # stack frames are: [firstname, argnum, openchar]
    try:
        for (token, value) in get_lexer_by_name('hy').get_tokens(current_line):
            if token is Token.Operator:
                if value in '([{':
                    stack.append(Group(value))
                elif value in ')]}':
                    stack.pop()
                elif value == '[]':
                    pass
                else:
                    print "found a surprising operator token: %r" % value
            elif token is Token.Text:
                if not value.strip():
                    try:
                        stack[-1].argnum += 1
                    except TypeError:
                        stack[-1].argnum = ''
                else:
                    print "found a surprising text token: %r" % value
            elif (token is Token.Name or token in Token.Name.subtypes or
                  token is Token.Operator and value == '.'):
                stack[-1].name += value
            elif token is Token.Literal.Number.Integer:
                pass
            else:
                print 'found a surprising token: %r %r' % (token, value)
        while stack[-1].opening in '[{':
            stack.pop()
        frame = stack.pop()
        func, arg_number = frame.name, frame.argnum
    except IndexError:
        return False
    if not func:
        return False
    return func, arg_number
