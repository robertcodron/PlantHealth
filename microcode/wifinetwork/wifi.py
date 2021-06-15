import network

class WifiConnect:
    def connect():
        #import network
        ssid      = "PlantHealth"
        password  =  "Sm0keyThisIsn0tVietnamThisIsB0wlingThereAreRules."
     
        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            print('connecting to network...')
            sta_if.active(True)
            sta_if.connect('PlantHealth', 'Sm0keyThisIsn0tVietnamThisIsB0wlingThereAreRules.')
            while not sta_if.isconnected():
                pass
        print("Connection successful")
        print(sta_if.ifconfig())

    def disconnect():
        import network
        sta_if = network.WLAN(network.STA_IF)
        sta_if.disconnect()
        sta_if.active(False)
