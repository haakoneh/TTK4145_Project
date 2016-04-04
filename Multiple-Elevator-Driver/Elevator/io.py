from schlang import*
from channels import INPUT, OUTPUT
from ctypes import byref

class IO:
	def _init_(self):

    	self.it_g = comedi_open("/dev/comedi0")
    	if (self.it_g == NULL):
    	    return 0
 

    	int status = 0
    	for i in xrange(8):
    	    self.status |= comedi_dio_config(self.it_g, INPUT.PORT1, i, 0)
			self.status |= comedi_dio_config(self.it_g, OUTPUT.PORT2, i, 1)
			self.status |= comedi_dio_config(self.it_g, OUTPUT.PORT3, i + 8, 1)
			self.status |= comedi_dio_config(self.it_g, INPUT.PORT4, i + 16, 0)
        if self.status < 0:
            print 'Error in self.status'
            break
   

	def setBit(self, channel,value):
        if value not in (0, 1):
            print 'Invalid value:' + str(value)
            break
		if comedi_dio_write(self.it_g, channel >> 8, channel & 0xff, 1) < 0:
            print 'Error in setBit'

	def clearBit(self, channel):
		if comedi_dio_write(self.it_g, channel >> 8, channel & 0xff, 0) < 0:
            print 'Error in clearBit'

	def readBit(self, channel):
		data = 0
    	if comedi_dio_read(self.it_g, channel >> 8, channel & 0xff, & byref(data)) < 0:
            print 'Error in readBit'
    	return data

	def writAnalog(self, channel, value):
    	if comedi_data_write(self.it_g, channel >> 8, channel & 0xff, 0, AREF_GROUND, value) < 0:
            print 'Error in writeAnalog'

    def readAnalog(self, channel):
    	lsampl_t data = 0
    	if comedi_data_read(self.it_g, channel >> 8, channel & 0xff, 0, AREF_GROUND, & byref(data)) < 0:
            print 'Error in readAnalog'
    	return data

io = IO()
