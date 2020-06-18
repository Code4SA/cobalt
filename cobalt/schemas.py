import os

from lxml import etree


SCHEMAS = {
    'http://docs.oasis-open.org/legaldocml/ns/akn/3.0': 'akomantoso30.xsd',
    'http://docs.oasis-open.org/legaldocml/ns/akn/3.0-lenient': 'akomantoso30-lenient.xsd',
}

_schemas = {}


def validate(akn_doc, strict=False):
    """ Validate this AKN document against its schema. if `strict` is True,
    then also validate the uniqueness of eId attributes. Returns a (validates, errors)
    tuple.
    """
    schema = get_schema(akn_doc.namespace, strict)
    return validate_xml(akn_doc.root, schema)


def validate_xml(root, schema):
    """ Validate an XML tree against a schema, returning a (validates, errors) tuple.
    """
    validates = schema(root)
    if not validates:
        errors = schema.error_log
    else:
        errors = []
    return validates, errors


def get_schema(namespace, strict):
    """ Get an XML schema for a namespace.
    """
    if not strict:
        namespace = namespace + '-lenient'

    if namespace not in _schemas:
        fname = os.path.join(os.path.dirname(__file__), 'xsd', SCHEMAS[namespace])
        with open(fname) as f:
            _schemas[namespace] = etree.XMLSchema(etree.parse(f))

    return _schemas[namespace]


def assert_validates(akn_doc, strict=False):
    """ Assert that this AKN document validates against the AKN schema.
    Raises `lxml.etree.DocumentInvalid' if validation fails.
    """
    schema = get_schema(akn_doc.namespace, strict)
    schema.assertValid(akn_doc.root)
