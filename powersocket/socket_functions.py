class socket_control:
    GPIO = None
    time = None
    socket_control_enabled = True

    def __init__(self):
	try: 
	    #import the required modules 
	    print 'Configuring GPIO board and pins...' 
	    import RPi.GPIO
	    import time as modtime

            self.GPIO = RPi.GPIO
            self.time = modtime

	    # disable warnings about current pin setups
	    self.GPIO.setwarnings(False)

	    # set the pins numbering mode
	    self.GPIO.setmode(self.GPIO.BOARD)

	    # Select the GPIO pins used for the encoder K0-K3 data inputs
	    self.GPIO.setup(11, self.GPIO.OUT)
	    self.GPIO.setup(15, self.GPIO.OUT)
	    self.GPIO.setup(16, self.GPIO.OUT)
	    self.GPIO.setup(13, self.GPIO.OUT)

	    # Select the signal to select ASK/FSK
	    self.GPIO.setup(18, self.GPIO.OUT)

	    # Select the signal used to enable/disable the modulator
	    self.GPIO.setup(22, self.GPIO.OUT)

	    # Disable the modulator by setting CE pin lo
	    self.GPIO.output (22, False)

	    # Set the modulator to ASK for On Off Keying
	    # by setting MODSEL pin lo
	    self.GPIO.output (18, False)

	    # Initialise K0-K3 inputs of the encoder to 0000
	    self.GPIO.output (11, False)
	    self.GPIO.output (15, False)
	    self.GPIO.output (16, False)
	    self.GPIO.output (13, False)

	    # The On/Off code pairs correspond to the hand controller codes.
	    # True = '1', False ='0'
	except RuntimeError, e:  
	    print e.message  
	    print 'Error importing GPIO modules. Socket control disabled!'  
	    socket_control_enabled = False  
	    pass

    def socket_on(self,socket_id):
        if self.socket_control_enabled == False:
            print 'Cannot switch socket on as control is disabled due to error on startup!'
        else:
            self.select_socket(socket_id)
            self.GPIO.output (13, True)
            self.transmit()

    def socket_off(self,socket_id):
        if self.socket_control_enabled == False:
            print 'Cannot switch socket off as control is disabled due to error on startup!'
        else:
            self.select_socket(socket_id)
            self.GPIO.output (13, False)
            self.transmit()

    def socket_all_off(self):
        if self.socket_control_enabled == False:
            print 'Cannot switch all sockets off as control is disabled due to error on startup!'
        else:
            self.GPIO.output (11, True)
            self.GPIO.output (15, True)
            self.GPIO.output (16, False)
            self.GPIO.output (13, False)
            self.transmit()

    def socket_all_on(self):
        if self.socket_control_enabled == False:
            print 'Cannot switch all sockets on as control is disabled due to error on startup!'
        else:
            self.GPIO.output (11, True)
            self.GPIO.output (15, True)
            self.GPIO.output (16, False)
            self.GPIO.output (13, True)
            self.transmit()

    def transmit(self):
        print 'Transmiting change to socket...'
        self.time.sleep(0.1)

        # Enable the modulator
        self.GPIO.output (22, True)

        # keep enabled for a period
        self.time.sleep(0.25)

        # Disable the modulator
        self.GPIO.output (22, False)

        print 'Transmit complete...'


    def select_socket(self, socket_id):
        if socket_id == 1:
            print 'Selecting socket 1...'
            self.GPIO.output (11, True)
            self.GPIO.output (15, True)
            self.GPIO.output (16, True)
        elif socket_id == 2:
            print 'Selecting socket 2...'
            self.GPIO.output (11, False)
            self.GPIO.output (15, True)
            self.GPIO.output (16, True)
        elif socket_id == 3:
            print 'Selecting socket 3...'
            self.GPIO.output (11, True)
            self.GPIO.output (15, False)
            self.GPIO.output (16, True)
        elif socket_id == 4:
            print 'Selecting socket 4...'
            self.GPIO.output (11, True)
            self.GPIO.output (15, False)
            self.GPIO.output (16, False)
