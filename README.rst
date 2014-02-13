This is a fork of bpython for use with Hy (http://docs.hylang.org/en/latest/).

Not the real bpython - see https://bitbucket.org/bobf/bpython for that.

bpython-hy - bpython for hy!

bpython-curtsies - bypython with native terminal scrolling!

Install with
`pip install git+https://github.com/thomasballinger/bpython.git@curtsies greenlet curtsies`
then use the command `bpython-curtsies`

.. image:: http://ballingt.com/assets/bpython-curtsies-scroll-demo-large.gif

It also has send-to-editor (F7 by default) and an improved version of
good old bpython rewind: `raw_input` prompts are saved so they don't need
to be entered again, and a new environment is used instead of the old one,
so variable bindings are actually undone.

.. image:: http://ballingt.com/assets/bpython-curtsies-undo-editor-prompt-save-demo.gif

Since it's not limited to keys curses can detect, there are more keybinds:

.. image:: http://ballingt.com/assets/bpython-curtsies-demo-large.gif

See http://bitbucket.org/bobf/bpython/ for the real bpython.

See http://ballingt.com/2013/12/21/bpython-curtsies.html for more.

