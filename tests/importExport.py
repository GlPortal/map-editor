import bpy
import os
import sys
import unittest

import toGlPortalXml

from shutil import copyfile
from testfixtures import TempDirectory


class ImportEportTest(unittest.TestCase):
  referenceMapPath = 'data/maps/importExportTest.xml'
  referenceData = ""
  d = None


  def readFile(self, filePath):
    file = open(filePath)
    content = file.read()
    file.close()
    return content

  def setUp(self):
    print(self.id())

  def test_import_export(self):
    self.referenceData = self.readFile(self.referenceMapPath)

    d = TempDirectory()

    try:
      importer = toGlPortalXml.importer.Importer(self.referenceMapPath, True)
      importer.mapFormatRadix = True
      importer.execute(bpy.context)

      filepath = os.path.join(d.path, "importExportTest.xml")
      copyfile(self.referenceMapPath, filepath)

      exporter = toGlPortalXml.Exporter.Exporter(filepath)
      exporter.mapFormatRadix = True
      exporter.execute(bpy.context)

      testData = self.readFile(filepath)

      self.assertEqual(testData, self.referenceData, "Files are not equal.\n")
    finally:
      d.cleanup()

if __name__ == '__main__':
  import xmlrunner
  unittest.main(
    argv=[sys.argv[0]]
  )
