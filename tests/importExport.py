import bpy
import os
import re
import subprocess
import sys
import unittest

import toGlPortalXml

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

  def copyMaterials(self, filepath):
    command = "grep -E 'materials|material |map>' '" + self.referenceMapPath + "' > '" + filepath + "'"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    process.communicate()

  def setUp(self):
    print(self.id())
    self.d = TempDirectory()

  def tearDown(self):
    self.d.cleanup()

  def test_import_export(self):
    self.referenceData = self.readFile(self.referenceMapPath)

    importer = toGlPortalXml.importer.Importer(self.referenceMapPath, True)
    importer.mapFormatRadix = True
    importer.execute(bpy.context)

    filepath = os.path.join(self.d.path, "importExportTest.xml")
    self.copyMaterials(filepath)

    exporter = toGlPortalXml.Exporter.Exporter(filepath)
    exporter.mapFormatRadix = True
    exporter.execute(bpy.context)

    testData = self.readFile(filepath)

    self.assertEqual(testData, self.referenceData, "Files are not equal.\n")

if __name__ == '__main__':
  import xmlrunner
  unittest.main(
    argv=[sys.argv[0]]
  )
