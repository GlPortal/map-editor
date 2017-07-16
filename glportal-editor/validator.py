import os
from lxml import etree

schemaPath = "xml-schema"
schemas = {
  'map'      : 'map.xsd',
  'material' : 'material.xsd',
  'screen'   : 'screen.xsd'
}


def validate(filePath="" , type='map'):
  if not filePath or not os.path.isfile(filePath):
    print("File '" + filePath + "' does not exist !")
    return False;

  if not type in schemas:
    print("Schema '" + type + "' does not exist !")
    return False;

  try:
    xsdFile = os.path.join(schemaPath, schemas[type])
    schema = etree.XMLSchema(file=xsdFile)
    xmlparser = etree.XMLParser(schema=schema)

    with open(filePath, 'r') as f:
      etree.fromstring(f.read(), xmlparser)

    return True
  except etree.XMLSchemaError:
    print("File is not valid")
    return False
