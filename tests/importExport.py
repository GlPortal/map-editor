import bpy
import os
import subprocess
import sys
import unittest

import toGlPortalXml

from testfixtures import TempDirectory


class ImportEportTest(unittest.TestCase):
  referenceMapPath = 'data/maps/importExportTest.xml'
  referenceData = ""
  directory = None

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
    self.directory = TempDirectory()

  def tearDown(self):
    self.directory.cleanup()

  def testImportExport(self):
    self.referenceData = self.readFile(self.referenceMapPath)

    importer = toGlPortalXml.importer.Importer(self.referenceMapPath, True)
    importer.execute(bpy.context)

    filepath = os.path.join(self.directory.path, "importExportTest.xml")
    self.copyMaterials(filepath)

    exporter = toGlPortalXml.Exporter.Exporter(filepath)
    exporter.execute(bpy.context)

    testData = self.readFile(filepath)

    self.assertEqual(testData, self.referenceData, "Files are not equal.\n")


if __name__ == '__main__':
  unittest.main(
    argv=[sys.argv[0]]
  )
