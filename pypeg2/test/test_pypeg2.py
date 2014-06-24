from __future__ import unicode_literals

import unittest
import pypeg2
import re

class GrammarTestCase1(unittest.TestCase):
    def runTest(self):
        x = pypeg2.some("thing")
        y = pypeg2.maybe_some("thing")
        z = pypeg2.optional("hello", "world")
        self.assertEqual(x, (-2, "thing"))
        self.assertEqual(y, (-1, "thing"))
        self.assertEqual(z, (0, ("hello", "world")))

class GrammarTestCase2(unittest.TestCase):
    def runTest(self):
        L1 = pypeg2.csl("thing")
        L2 = pypeg2.csl("hello", "world")
        self.assertEqual(L1, ("thing", -1, (",", pypeg2.blank, "thing")))
        self.assertEqual(L2, ("hello", "world", -1, (",", pypeg2.blank, "hello", "world")))

class ParserTestCase(unittest.TestCase): pass

class TypeErrorTestCase(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        with self.assertRaises(pypeg2.GrammarTypeError):
            parser.parse("hello, world", 23)

class ParseTerminalStringTestCase1(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hello, world", "hello")
        self.assertEqual(r, (", world", None))

class ParseTerminalStringTestCase2(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse("hello, world", "world")

class ParseKeywordTestCase1(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hallo, world", pypeg2.K("hallo"))
        self.assertEqual(r, (", world", None))
        pypeg2.Keyword.table[pypeg2.K("hallo")]

class ParseKeywordTestCase2(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse("hello, world", pypeg2.K("werld"))
        pypeg2.Keyword.table[pypeg2.K("werld")]

class ParseKeywordTestCase3(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse(", world", pypeg2.K("hallo"))
        pypeg2.Keyword.table[pypeg2.K("hallo")]

class ParseRegexTestCase1(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hello, world", re.compile(r"h.[lx]l\S", re.U))
        self.assertEqual(r, (", world", "hello"))

class ParseRegexTestCase2(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse("hello, world", re.compile(r"\d", re.U))

class ParseSymbolTestCase1(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hello, world", pypeg2.Symbol)
        self.assertEqual(r, (", world", pypeg2.Symbol("hello")))

class ParseSymbolTestCase2(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse(", world", pypeg2.Symbol)

class ParseAttributeTestCase(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hello, world", pypeg2.attr("some", pypeg2.Symbol))
        self.assertEqual(
            r,
            (
                ', world',
                pypeg2.attr.Class(name='some', thing=pypeg2.Symbol('hello'),
                    subtype=None)
            )
        )

class ParseTupleTestCase1(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hello, world", (pypeg2.name(), ",", pypeg2.name()))
        self.assertEqual(
            r,
            (
                '',
                [
                    pypeg2.attr.Class(name='name',
                        thing=pypeg2.Symbol('hello'), subtype=None),
                    pypeg2.attr.Class(name='name',
                        thing=pypeg2.Symbol('world'), subtype=None)
                ]
            )
        )

class ParseTupleTestCase2(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        with self.assertRaises(ValueError):
            parser.parse("hello, world", (-23, "x"))

class ParseSomeTestCase1(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hello, world", pypeg2.some(re.compile(r"\w", re.U)))
        self.assertEqual(r, (', world', ['h', 'e', 'l', 'l', 'o']))

class ParseSomeTestCase2(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse("hello, world", pypeg2.some(re.compile(r"\d", re.U)))

class ParseMaybeSomeTestCase1(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hello, world", pypeg2.maybe_some(re.compile(r"\w", re.U)))
        self.assertEqual(r, (', world', ['h', 'e', 'l', 'l', 'o']))

class ParseMaybeSomeTestCase2(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hello, world", pypeg2.maybe_some(re.compile(r"\d", re.U)))
        self.assertEqual(r, ('hello, world', []))

class ParseCardinalityTestCase1(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hello, world", (5, re.compile(r"\w", re.U)))
        self.assertEqual(r, (', world', ['h', 'e', 'l', 'l', 'o']))

class ParseCardinalityTestCase2(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse("hello, world", (6, re.compile(r"\w", re.U)))

class ParseOptionsTestCase1(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hello, world", [re.compile(r"\d+", re.U), pypeg2.word])
        self.assertEqual(r, (', world', 'hello'))

class ParseOptionsTestCase2(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse("hello, world", ["x", "y"])

class ParseListTestCase1(ParserTestCase):
    class Chars(pypeg2.List):
        grammar = pypeg2.some(re.compile(r"\w", re.U)), pypeg2.attr("comma", ",")

    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hello, world", ParseListTestCase1.Chars)
        self.assertEqual(r, (
            'world',
            ParseListTestCase1.Chars(['h', 'e', 'l', 'l', 'o']))
        )
        self.assertEqual(r[1].comma, None)

class ParseListTestCase2(ParserTestCase):
    class Digits(pypeg2.List):
        grammar = pypeg2.some(re.compile(r"\d", re.U))

    def runTest(self):
        parser = pypeg2.Parser()
        with self.assertRaises(SyntaxError):
            r = parser.parse("hello, world", ParseListTestCase2.Digits)

class ParseClassTestCase1(ParserTestCase):
    class Word(str):
        grammar = pypeg2.word
 
    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hello, world", ParseClassTestCase1.Word)
        self.assertEqual(type(r[1]), ParseClassTestCase1.Word)
        self.assertEqual(r[1], "hello")

class ParseClassTestCase2(ParserTestCase):
    class Word(str):
        grammar = pypeg2.word, pypeg2.attr("comma", ",")
        def __init__(self, data):
            self.polished = False
        def polish(self):
            self.polished = True
 
    def runTest(self):
        parser = pypeg2.Parser()
        r = parser.parse("hello, world", ParseClassTestCase2.Word)
        self.assertEqual(type(r[1]), ParseClassTestCase2.Word)
        self.assertEqual(r[1], "hello")
        self.assertTrue(r[1].polished)
        self.assertEqual(r[1].comma, None)

class Parm(object):
    grammar = pypeg2.name(), "=", pypeg2.attr("value", int)

class Parms(pypeg2.Namespace):
    grammar = (pypeg2.csl(Parm), pypeg2.flag("fullstop", "."),
            pypeg2.flag("semicolon", ";"))

class ParseNLTestCase1(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        parser.comment = pypeg2.comment_c
        t, parms = parser.parse("x=23 /* Illuminati */, y=42 /* the answer */;", Parms)
        self.assertEqual(parms["x"].value, 23)
        self.assertEqual(parms["y"].value, 42)
        self.assertEqual(parms.fullstop, False)
        self.assertEqual(parms.semicolon, True)

class EnumTest(pypeg2.Symbol):
    grammar = pypeg2.Enum( pypeg2.K("int"), pypeg2.K("long") )

class ParseEnumTestCase1(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        t, r = parser.parse("int", EnumTest)
        self.assertEqual(r, "int")

class ParseEnumTestCase2(ParserTestCase):
    def runTest(self):
        parser = pypeg2.Parser()
        with self.assertRaises(SyntaxError):
            t, r = parser.parse("float", EnumTest)

class ParseInvisibleTestCase(ParserTestCase):
    class C1(str):
        grammar = pypeg2.ignore("!"), pypeg2.restline
    def runTest(self):
        r = pypeg2.parse("!all", type(self).C1)
        self.assertEqual(str(r), "all")
        self.assertEqual(r._ignore1, None)

class ParseOmitTestCase(ParserTestCase):
    def runTest(self):
        r = pypeg2.parse("hello", pypeg2.omit(pypeg2.word))
        self.assertEqual(r, None)

class ComposeTestCase(unittest.TestCase): pass

class ComposeString(object):
    grammar = "something"

class ComposeStringTestCase(ComposeTestCase):
    def runTest(self):
        x = ComposeString()
        t = pypeg2.compose(x)
        self.assertEqual(t, "something")

class ComposeRegex(str):
    grammar = pypeg2.word

class ComposeRegexTestCase(ComposeTestCase):
    def runTest(self):
        x = ComposeRegex("something")
        t = pypeg2.compose(x)
        self.assertEqual(t, "something")

class ComposeKeyword(object):
    grammar = pypeg2.K("hallo")

class ComposeKeywordTestCase(ComposeTestCase):
    def runTest(self):
        x = ComposeKeyword()
        t = pypeg2.compose(x)
        self.assertEqual(t, "hallo")

class ComposeSymbol(pypeg2.Symbol): pass

class ComposeSymbolTestCase(ComposeTestCase):
    def runTest(self):
        x = ComposeSymbol("hello")
        t = pypeg2.compose(x)
        self.assertEqual(t, "hello")

class ComposeAttribute(object):
    grammar = pypeg2.name()

class ComposeAttributeTestCase(ComposeTestCase):
    def runTest(self):
        x = ComposeAttribute()
        x.name = pypeg2.Symbol("hello")
        t = pypeg2.compose(x)
        self.assertEqual(t, "hello")

class ComposeFlag(object):
    grammar = pypeg2.flag("mark", "MARK")

class ComposeFlagTestCase1(ComposeTestCase):
    def runTest(self):
        x = ComposeFlag()
        x.mark = True
        t = pypeg2.compose(x)
        self.assertEqual(t, "MARK")

class ComposeFlagTestCase2(ComposeTestCase):
    def runTest(self):
        x = ComposeFlag()
        x.mark = False
        t = pypeg2.compose(x)
        self.assertEqual(t, "")

class ComposeTuple(pypeg2.List):
    grammar = pypeg2.csl(pypeg2.word)

class ComposeTupleTestCase(ComposeTestCase):
    def runTest(self):
        x = ComposeTuple(["hello", "world"])
        t = pypeg2.compose(x)
        self.assertEqual(t, "hello, world")

class ComposeList(str):
    grammar = [ re.compile(r"\d+", re.U), pypeg2.word ]

class ComposeListTestCase(ComposeTestCase):
    def runTest(self):
        x = ComposeList("hello")
        t = pypeg2.compose(x)
        self.assertEqual(t, "hello")

class ComposeIntTestCase(ComposeTestCase):
    def runTest(self):
        x = pypeg2.compose(23, int)
        self.assertEqual(x, "23")

class C2(str):
    grammar = pypeg2.attr("some", "!"), pypeg2.restline

class ComposeInvisibleTestCase(ParserTestCase):
    def runTest(self):
        r = pypeg2.parse("!all", C2)
        self.assertEqual(str(r), "all")
        self.assertEqual(r.some, None)
        t = pypeg2.compose(r, C2)
        self.assertEqual(t, "!all")

class ComposeOmitTestCase(ParserTestCase):
    def runTest(self):
        t = pypeg2.compose('hello', pypeg2.omit(pypeg2.word))
        self.assertEqual(t, "")

class CslPython32Compatibility(ParserTestCase):
    def runTest(self):
        try:
            g = eval("pypeg2.csl('hello', 'world', separator=';')")
        except TypeError:
            return
        self.assertEqual(g, ("hello", "world", -1, (";", pypeg2.blank, "hello", "world")))

if __name__ == '__main__':
    unittest.main()
