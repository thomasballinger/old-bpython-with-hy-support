import bpython.curtsies
import sys

def main(*args, **kwargs):
    kwargs['lang'] = 'hy'
    bpython.curtsies.main(*args, **kwargs)

if __name__ == '__main__':
    sys.exit(main)
