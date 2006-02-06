#Copyright (c) 2005, Ilja Booij (ibooij@gmail.com)
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without modification, 
#are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice, 
#    this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice, 
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#    * Neither the name of Ilja Booij nor the names of its contributors may be 
#    used to endorse or promote products derived from this software without 
#    specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
#ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#from HAC4Importer import HAC4Importer

import logging
import fcntl, os, errno

DEVICE = '/dev/ttyUSB0'
#DEVICE = '/tmp/testdatafile.dat'
# length of data from HAC4 is always 81930 bytes
DATA_LENGTH = 81930

class HAC4USBImporter:
    """implements importing from USB."""
    
    def __init__(self):
        self._progress = 0.0
        self.usb_port = file(DEVICE, 'rb')
        fcntl.fcntl(self.usb_port, fcntl.F_SETFL, os.O_NONBLOCK)
        
        self._data = ""
        self.ready = False
        
    def __del__(self):
        """cleans up the USB importer (closes connection with USB
           device)"""
        self.usb_port.close()
    
    def get_data(self):
        return "".join(self._data)
    
    
    def set_ready(self):
        self.ready = True
        
    def is_ready(self):
        return ready
        
    def attempt_read(self):
        """attempt to read from the usb port. If the read succeeds,
        the new bytes are added to the data. 
        
        This function will return True when reading is finished;
        False otherwise"""
        
        assert(len(self._data) < DATA_LENGTH)
        
        bytes_read = []
        while 1:
            try:
                data_read = self.usb_port.read(1024)
                 
            except IOError, e:
                if e.args[0] == errno.EAGAIN:
                    print 'EAGAIN'
                    break
                raise
            print 'read ', len(data_read), ' bytes.'
            bytes_read.append(data_read)
            if len(data_read) < 1024:
                break
       
        self._data += ''.join(bytes_read)
        
        # Post condition
        assert(len(self._data) <= DATA_LENGTH)
            
        if len(self._data) == DATA_LENGTH:
            return True
        else:
            return False
            
    def get_progress(self):
        return len(self._data) / float(DATA_LENGTH)
    
if __name__ == '__main__':
    # just a simple interactive test
    importer = HAC4USBImporter()
    import time
    start_time = time.time()
    importer.start()
    
    progress = importer.get_progress()
    while progress < 1.0:
        current_time = time.time()
        time.sleep(0.5)
        prev_progress = progress
        progress = importer.get_progress()
        print progress
        
        if (prev_progress == progress and progress > 0.0):
            importer.stop()
            break
        
    print importer.get_data()
    f = file('out.dat', 'wb')
    f.write(importer.get_data())
    f.close()
    
    importer.join()
    
    #print importer.get_data()
    
    
    
            
            
        
        