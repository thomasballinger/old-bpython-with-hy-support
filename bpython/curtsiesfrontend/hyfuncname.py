
from pygments.token import Token

from pygments.lexers import get_lexer_by_name

def split_tokens(tokens):
    out_tokens = []
    for token_type, value in tokens:
        if token_type is Token.Operator and len(value) > 1:
            out_tokens.extend((token_type, v) for v in value)
        else:
            out_tokens.append((token_type, value))
    return out_tokens

def get_name_of_current_hy_function(current_line):

    # Get the name of the current function and where we are in
    # the arguments
    class Group(object):
        def __init__(self, opening, name=None, argnum=-1, name_is_complete=False):
            self.name = name
            self.argnum = argnum
            self.opening = opening
            self.name_is_complete = name_is_complete
        def __repr__(self):
            return '%s%s%s %s' % (self.opening, self.name if self.name else '???', self.argnum, '___ '*(max(self.argnum - 1, 0)) + 'CURARG)')
    stack = []
    # stack frames are: [firstname, argnum, openchar]
    try:
        tokens = get_lexer_by_name('hy').get_tokens(current_line)
        tokens = split_tokens(tokens)
        tokens = tokens[:-1] # there's always a newline at the end that we don't want
        prev_token, prev_value = Token.Text, ''
        for (token, value) in tokens:
            if (((token is Token.Name.Attribute) or
                   (token is Token.Operator and value == '.')) and
                  not stack[-1].name_is_complete):
                stack[-1].name += value
            elif token is Token.Operator:
                if value in '([{':
                    stack.append(Group(value))
                elif value in ')]}':
                    stack.pop()
                else:
                    pass # let's assume it's a valid identifier
                    print "found a surprising operator token: %r" % value
            elif token is Token.Text:
                if not value.strip():
                    stack[-1].name_is_complete = True
                    try:
                        stack[-1].argnum += 1
                    except TypeError:
                        stack[-1].argnum = ''
                else:
                    print "found a surprising text token: %r" % value
            elif (token is Token.Name or
                  token in Token.Name.subtypes or
                  token in Token.Keyword.subtypes):
                if stack[-1].name is None:
                    stack[-1].name = value
                else:
                    pass
            elif (token is Token.Literal.Number.Integer or
                  token is Token.Name):
                pass
            else:
                print 'found a surprising token: %r %r' % (token, value)
            prev_token, prev_value = token, value
        while stack[-1].opening in '[{':
            stack.pop()
        frame = stack.pop()
        func, arg_number = frame.name, frame.argnum
    except IndexError:
        return False
    if not func:
        return False
    return func, arg_number
