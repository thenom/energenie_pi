socket_control_enabled = True

try:
   from energenie import switch_on, switch_off
except RuntimeError, e:
   print e.message
   print 'Error importing energenie modules. Socket control disabled!'
   socket_control_enabled = False
   pass

def socket_on(socket_id):
    if socket_control_enabled == False:
        print 'Cannot switch socket on as control is disabled due to error on startup!'
    else:
        switch_on(socket_id)

def socket_off(socket_id):
    if socket_control_enabled == False:
        print 'Cannot switch socket off as control is disabled due to error on startup!'
    else:
        switch_off(socket_id)

def socket_all_off():
    if socket_control_enabled == False:
        print 'Cannot switch all sockets off as control is disabled due to error on startup!'
    else:
        switch_off()

def socket_all_on():
    if socket_control_enabled == False:
        print 'Cannot switch all sockets on as control is disabled due to error on startup!'
    else:
        switch_on()
