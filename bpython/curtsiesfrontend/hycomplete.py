import __builtin__
import rlcompleter
import re
from bpython import inspection
import hy.compiler
import hy.macros
import hy.core.language
import hy.core.macros
import hy.core.bootstrap

try:
    import abc
    abc.ABCMeta
    has_abc = True
except (ImportError, AttributeError):
    has_abc = False

# Autocomplete modes
SIMPLE = 'simple'

class Autocomplete(rlcompleter.Completer):

    def __init__(self, namespace = None, config = None):
        rlcompleter.Completer.__init__(self, namespace)
        self.locals = namespace
        if hasattr(config, 'autocomplete_mode'):
            self.autocomplete_mode = config.autocomplete_mode
        else:
            self.autocomplete_mode = SIMPLE

    def attr_matches(self, text):
        """Overrides rlcompleter.Completer.attr_matches, used to complete
        """

        # Gna, Py 2.6's rlcompleter searches for __call__ inside the
        # instance instead of the type, so we monkeypatch to prevent
        # side-effects (__getattr__/__getattribute__)
        m = re.match(r"(\w+(\.\w+)*)\.(\w*)", text)
        if not m:
            return []

        expr, attr = m.group(1, 3)
        if expr.isdigit():
            # Special case: float literal, using attrs here will result in
            # a SyntaxError
            return []
        obj = eval(expr, self.locals)
        with inspection.AttrCleaner(obj):
            matches = self.attr_lookup(obj, expr, attr)
        return matches

    def attr_lookup(self, obj, expr, attr):
        """Second half of original attr_matches method factored out so it can
        be wrapped in a safe try/finally block in case anything bad happens to
        restore the original __getattribute__ method."""
        words = dir(obj)
        if hasattr(obj, '__class__'):
            words.append('__class__')
            words = words + rlcompleter.get_class_members(obj.__class__)
            if has_abc and not isinstance(obj.__class__, abc.ABCMeta):
                try:
                    words.remove('__abstractmethods__')
                except ValueError:
                    pass

        matches = []
        n = len(attr)
        for word in words:
            if self.method_match(word, n, attr) and word != "__builtins__":
                matches.append("%s.%s" % (expr, word))
        return matches

    def _callable_postfix(self, value, word):
        """rlcompleter's _callable_postfix done right."""
        with inspection.AttrCleaner(value):
            if inspection.is_callable(value):
                pass #word += ')'
        return word

    def global_matches(self, text):
        """Compute matches when text is a simple name.
        Return a list of all keywords, built-in functions and names currently
        defined in self.namespace that match.

        Overrides rlcompleter.Completer.global_matches
        """
        hash = {}
        for nspace in [__builtin__.__dict__, self.namespace,
                hy.compiler._compile_table, hy.macros._hy_macros, hy.macros._hy_reader]:
            for word, val in nspace.items():
                if not isinstance(word, str): continue
                if self.method_match(word, len(text), text) and word != "__builtins__":
                    hash[self._callable_postfix(val, word)] = 1
        for word in hy.core.language.EXPORTS:
            val = getattr(hy.core.language, word)
            if self.method_match(word, len(text), text) and word != "__builtins__":
                hash[self._callable_postfix(val, word)] = 1
        for name, d in hy.macros._hy_macros.items():
            if not d: continue
            for word, val in d.items():
                if self.method_match(word, len(text), text) and word != "__builtins__":
                    hash[self._callable_postfix(val, word)] = 1

        matches = hash.keys()
        matches.sort()
        return matches

    def method_match(self, word, size, text):
        if self.autocomplete_mode == SIMPLE:
            return word[:size] == text
        else:
            raise NotImplementedError("Only simple completion works (change your settings?)")

