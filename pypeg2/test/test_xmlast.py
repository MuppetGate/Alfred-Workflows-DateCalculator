from __future__ import unicode_literals
try:
    str = unicode
except NameError:
    pass

import unittest
import re, sys
import pypeg2, pypeg2.xmlast

class Another(object):
    grammar = pypeg2.name(), "=", pypeg2.attr("value")

class Something(pypeg2.List):
    grammar = pypeg2.name(), pypeg2.some(Another), str

class Thing2etreeTestCase1(unittest.TestCase):
    def runTest(self):
        s = Something()
        s.name = "hello"
        a1 = Another()
        a1.name = "bla"
        a1.value = "blub"
        a2 = Another()
        a2.name = "foo"
        a2.value = "bar"
        s.append(a1)
        s.append(a2)
        s.append("hello, world")

        root = pypeg2.xmlast.create_tree(s)

        self.assertEqual(root.tag, "Something")
        self.assertEqual(root.attrib["name"], "hello")
 
        try:
            import lxml
        except ImportError:
            self.assertEqual(pypeg2.xmlast.etree.tostring(root), b'<Something name="hello"><Another name="bla" value="blub" /><Another name="foo" value="bar" />hello, world</Something>')
        else:
            self.assertEqual(pypeg2.xmlast.etree.tostring(root), b'<Something name="hello"><Another name="bla" value="blub"/><Another name="foo" value="bar"/>hello, world</Something>')

class SomethingElse(pypeg2.Namespace):
    grammar = pypeg2.name(), pypeg2.some(Another)

class Thing2etreeTestCase2(unittest.TestCase):
    def runTest(self):
        s = SomethingElse()
        s.name = "hello"
        a1 = Another()
        a1.name = "bla"
        a1.value = "blub"
        a2 = Another()
        a2.name = "foo"
        a2.value = "bar"
        s[a1.name] = a1
        s[a2.name] = a2

        root = pypeg2.xmlast.create_tree(s)

        self.assertEqual(root.tag, "SomethingElse")
        self.assertEqual(root.attrib["name"], "hello")
 
        try:
            import lxml
        except ImportError:
            self.assertEqual(pypeg2.xmlast.etree.tostring(root), b'<SomethingElse name="hello"><Another name="bla" value="blub" /><Another name="foo" value="bar" /></SomethingElse>')
        else:
            self.assertEqual(pypeg2.xmlast.etree.tostring(root), b'<SomethingElse name="hello"><Another name="bla" value="blub"/><Another name="foo" value="bar"/></SomethingElse>')

class Thing2XMLTestCase3(unittest.TestCase):
    class C1(str):
        grammar = pypeg2.ignore("!"), pypeg2.restline
    def runTest(self):
        r = pypeg2.parse("!all", type(self).C1)
        xml = pypeg2.xmlast.thing2xml(r)
        self.assertEqual(xml, b"<C1>all</C1>")

class Key(str):
    grammar = pypeg2.name(), "=", pypeg2.restline

class XML2ThingTestCase1(unittest.TestCase):
    def runTest(self):
        xml = b'<Key name="foo">bar</Key>'
        thing = pypeg2.xmlast.xml2thing(xml, globals())
        self.assertEqual(thing.name, pypeg2.Symbol("foo"))
        self.assertEqual(thing, "bar")

class Instruction(str): pass

class Parameter(object):
    grammar = pypeg2.attr("typing", str), pypeg2.name()

class Parameters(pypeg2.Namespace):
    grammar = pypeg2.optional(pypeg2.csl(Parameter))

class Function(pypeg2.List):
    grammar = pypeg2.name(), pypeg2.attr("parms", Parameters), "{", pypeg2.maybe_some(Instruction), "}"

class XML2ThingTestCase2(unittest.TestCase):
    def runTest(self):
        xml = b'<Function name="f"><Parameters><Parameter name="a" typing="int"/></Parameters><Instruction>do_this</Instruction></Function>'
        f = pypeg2.xmlast.xml2thing(xml, globals())
        self.assertEqual(f.name, pypeg2.Symbol("f"))
        self.assertEqual(f.parms["a"].name, pypeg2.Symbol("a"))
        self.assertEqual(f.parms["a"].typing, pypeg2.Symbol("int"))
        self.assertEqual(f[0], "do_this")

if __name__ == '__main__':
    unittest.main()
