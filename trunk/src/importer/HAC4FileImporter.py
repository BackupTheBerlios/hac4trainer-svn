from HAC4Importer import HAC4Importer

import logging

class HAC4FileImporter(HAC4Importer):
    """A HAC4Importer that uses a file as it's source"""

    def __init__(self, filename):
        self._filename = filename
        
    def _readFile(self):
        try:
            datafile = file(self._filename, 'rb')
        except IOError, error:
            logging.error("Unable to open file %s: %s" % (self._filename, error.strerror))
            raise
        
        self.setRawData(datafile.read())
        datafile.close()
    
    def doImport(self):
        logging.debug('FileImporter: starting import')
        self._readFile()
        return HAC4Importer.doImport(self)

if __name__ == '__main__':
    import sys
    sys.path.append('..')
    importer = HAC4FileImporter("../data/testdatafile.dat")
    tours = importer.doImport()
    print tours
    print len(tours)
    #print importer.getRawData()
    