import sys
import pjsua as pj
import time

# Logging callback
def log_cb(level, str, len):
    print str,

# Callback to receive events from Call
class MyCallCallback(pj.CallCallback):
    def __init__(self, call=None):
        pj.CallCallback.__init__(self, call)

    # Notification when call state has changed
    def on_state(self):
        print "Call is ", self.call.info().state_text,
        print "last code =", self.call.info().last_code, 
        print "(" + self.call.info().last_reason + ")"
        if self.call.info().state == pj.CallState.DISCONNECTED:
            lib.player_destroy(self._player)
        
    # Notification when call's media state has changed.
    def on_media_state(self):
        global lib
        if self.call.info().media_state == pj.MediaState.ACTIVE:
            # Connect the call to sound device
            call_slot = self.call.info().conf_slot
            self._player = lib.create_player("man2_64.wav", loop=True)
            player_slot = lib.player_get_slot(self._player)
            #lib.conf_connect(call_slot, 0)
            #lib.conf_connect(0, call_slot)
            lib.conf_connect(player_slot, call_slot)
            #lib.conf_connect(call_slot, player_slot)
            lib.conf_connect(player_slot, 0)
            print "Hello world, I can talk!"


# Check command line argument
if len(sys.argv) != 4:
    print "Usage: call.py <dst-URI> <ext> <pass>"
    sys.exit(1)

try:
    uc = pj.UAConfig()
    #uc.max_calls = 20
    # Create library instance
    lib = pj.Lib()

    # Init library with default config
    log_config = pj.LogConfig(level=5, callback=log_cb)
    log_config.msg_logging = False
    lib.init(ua_cfg = uc, log_cfg = log_config)


    # Create UDP transport which listens to any available port
    transport = lib.create_transport(pj.TransportType.UDP)
    
    # Start the library
    lib.start()

    # Build the account configuration
    acc_cfg = pj.AccountConfig("10.10.10.1", sys.argv[2], sys.argv[3])

    # Create local/user-less account
    acc = lib.create_account(acc_cfg)

    # Make call
    call1 = acc.make_call(sys.argv[1], MyCallCallback())
    #time.sleep(1)
    #call2 = acc.make_call(sys.argv[1], MyCallCallback())
    #time.sleep(1)
    #call3 = acc.make_call(sys.argv[1], MyCallCallback())
    #time.sleep(1)
    time.sleep(30)
    call1.hangup()
    #time.sleep(1)
    #call2.hangup()
    #time.sleep(1)
    #call3.hangup()
    time.sleep(11)
    
    # We're done, shutdown the library
    lib.destroy()
    lib = None

    sys.exit(1)

except pj.Error, e:
    print "Exception: " + str(e)
    lib.destroy()
    lib = None
    sys.exit(1)
