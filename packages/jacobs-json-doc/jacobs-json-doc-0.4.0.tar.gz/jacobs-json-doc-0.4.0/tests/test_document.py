import unittest
from collections import UserDict
from jacobsjsondoc.loader import PrepopulatedLoader
from jacobsjsondoc.resolver import PassThroughResolver
from jacobsjsondoc.document import Document, RefResolutionMode, DocReference, DocValue, DocObject, CircularDependencyError

SIMPLE_YAML = """
jacob:
    brunson:
        - 1
        - 2
        - true
        - isa:
            nice guy
    food:
        true
def:
    foo: "this is a foo string"
"""

YAML_WITH_REF = """
house:
    var: "this is the value of the var"
    local:
        $ref: "#/house/var"
    remote:
        $ref: "remote#/def/foo"
"""

ANOTHER_YAML_WITH_REF = """
colorado:
    denver: 1
    springs: 
        $ref: "middle#/house"
"""

YAML_TYPES = """
myobject:
    myint: 10
    myfloat: 3.14159
    mystring: string
    mytrue: true
    myfalse: false
    mynull: null
"""


class TestDocument(unittest.TestCase):

    def test_lines(self):
        ppl = PrepopulatedLoader()
        ppl.prepopulate(None, SIMPLE_YAML)
        doc = Document(uri=None, resolver=None, loader=ppl)
        
        self.assertEqual(doc['jacob'].line, 2)
        self.assertEqual(doc['jacob']['brunson'].line, 3)
        self.assertEquals(doc['jacob']['brunson'][0].value, 1)
        self.assertEqual(doc['jacob']['brunson'][0].line, 3)

    def test_local_ref_use_reference_objects(self):
        ppl = PrepopulatedLoader()
        ppl.prepopulate("yaml_with_ref", YAML_WITH_REF)
        doc = Document(uri="yaml_with_ref", resolver=None, loader=ppl, ref_resolution=RefResolutionMode.USE_REFERENCES_OBJECTS)
        self.assertIsInstance(doc['house']['local'], DocReference)
        node = doc['house']['local'].resolve()
        self.assertIsInstance(node, DocValue)
        self.assertEqual(node.value, "this is the value of the var")

    def test_local_ref_resolve_references(self):
        ppl = PrepopulatedLoader()
        ppl.prepopulate("local", YAML_WITH_REF)
        ppl.prepopulate("remote", SIMPLE_YAML)
        doc = Document(uri="local", resolver=PassThroughResolver(), loader=ppl, ref_resolution=RefResolutionMode.RESOLVE_REFERENCES)
        self.assertIsInstance(doc['house']['local'], DocValue)
        self.assertEqual(doc['house']['local'].value, "this is the value of the var")

    def test_remote_ref_use_reference_objects(self):
        ppl = PrepopulatedLoader()
        ppl.prepopulate("local", YAML_WITH_REF)
        ppl.prepopulate("remote", SIMPLE_YAML)
        doc = Document(uri="local", resolver=PassThroughResolver(), loader=ppl, ref_resolution=RefResolutionMode.USE_REFERENCES_OBJECTS)
        self.assertIsInstance(doc['house']['remote'], DocReference)
        node = doc['house']['remote'].resolve()
        self.assertIsInstance(node, DocValue)
        self.assertEqual(node.value, "this is a foo string")
        self.assertEqual(node.line, 11)

    def test_remote_ref_resolve_references(self):
        ppl = PrepopulatedLoader()
        ppl.prepopulate("local", YAML_WITH_REF)
        ppl.prepopulate("remote", SIMPLE_YAML)
        doc = Document(uri="local", resolver=PassThroughResolver(), loader=ppl, ref_resolution=RefResolutionMode.RESOLVE_REFERENCES)
        self.assertIsInstance(doc['house']['remote'], DocValue)
        self.assertEqual(doc['house']['remote'].value, "this is a foo string")

    def test_3_layer_resolve_references(self):
        ppl = PrepopulatedLoader()
        ppl.prepopulate("middle", YAML_WITH_REF)
        ppl.prepopulate("remote", SIMPLE_YAML)
        ppl.prepopulate("local", ANOTHER_YAML_WITH_REF)
        doc = Document(uri="local", resolver=PassThroughResolver(), loader=ppl, ref_resolution=RefResolutionMode.RESOLVE_REFERENCES)
        self.assertIsInstance(doc['colorado']['springs'], DocObject)
        self.assertIsInstance(doc['colorado']['springs']['var'], DocValue)
        self.assertEqual(doc['colorado']['springs']['var'].value, "this is the value of the var")
        self.assertEqual(doc['colorado']['springs']['var'].uri_line, "middle:2")
        self.assertIsInstance(doc['colorado']['springs']['remote'], DocValue)
        self.assertEqual(doc['colorado']['springs']['remote'].value, "this is a foo string")
        self.assertEqual(doc['colorado']['springs']['remote'].uri_line, "remote:11")

    def test_circular_dependency(self):
        yaml1 = """
        outer:
            inner:
                $ref: "two#/foo"
        """
        yaml2 = """
        foo:
            bar:
                $ref: "one#/outer"
        """
        ppl = PrepopulatedLoader()
        ppl.prepopulate("one", yaml1)
        ppl.prepopulate("two", yaml2)
        with self.assertRaises(CircularDependencyError):
            doc = Document(uri="one", resolver=PassThroughResolver(), loader=ppl, ref_resolution=RefResolutionMode.RESOLVE_REFERENCES)


class TestDocumentTypes(unittest.TestCase):

    def setUp(self):
        ppl = PrepopulatedLoader()
        ppl.prepopulate(None, YAML_TYPES)
        self.doc = Document(uri=None, resolver=None, loader=ppl)

    def test_userdict(self):
        self.assertIsInstance(self.doc['myobject'], UserDict)

    def test_integer(self):
        self.assertEqual(self.doc['myobject']['myint'], 10)
        self.assertIsInstance(self.doc['myobject']['myint'], int)
        self.assertEqual(self.doc['myobject']['myint'].line, 2)

    def test_float(self):
        self.assertEqual(self.doc['myobject']['myfloat'], 3.14159)
        self.assertIsInstance(self.doc['myobject']['myfloat'], float)
        self.assertEqual(self.doc['myobject']['myfloat'].line, 3)

    def test_string(self):
        self.assertEqual(self.doc['myobject']['mystring'], "string")
        self.assertIsInstance(self.doc['myobject']['mystring'], str)
        self.assertEqual(self.doc['myobject']['mystring'].line, 4)

    def test_boolean_true(self):
        self.assertEqual(self.doc['myobject']['mytrue'], True)
        self.assertEqual(self.doc['myobject']['mytrue'].line, 5)

    def test_boolean_false(self):
        self.assertEqual(self.doc['myobject']['myfalse'], False)
        self.assertEqual(self.doc['myobject']['myfalse'].line, 6)

    def test_null(self):
        self.assertEqual(self.doc['myobject']['mynull'].value, None)
        self.assertIsInstance(self.doc['myobject']['mynull'].value, type(None))
        self.assertEqual(self.doc['myobject']['mynull'].line, 7)

if __name__ == '__main__':
    unittest.main()