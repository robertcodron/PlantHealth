# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
#from wifinetwork.wifi import WifiConnect
#import webrepl
#webrepl.start()
#gc.collect()
gc.disable() #garbage collector off

#WifiConnect.connect()