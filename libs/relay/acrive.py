try:
    import RPi.GPIO as GPIO
    class control_relay():
        def __init__(self) -> None:
            print("self 1")
            self.relay_ch = 21
            GPIO.setmode(GPIO.BCM)
            print("self2")
            GPIO.setwarnings(False)
            print("self3") 
            
            GPIO.setup(self.relay_ch,GPIO.OUT)
            GPIO.output(self.relay_ch,GPIO.HIGH)
 
        def start(self):
            print("start")
           
            GPIO.output(self.relay_ch, GPIO.HIGH)

        def stop(self):
            print("stop")
            GPIO.output(self.relay_ch, GPIO.LOW)
            GPIO.cleanup()
            

except ModuleNotFoundError as error:
    

    class control_relay():

        def __init__(self) -> None:
            self.relay_ch = 21
            
        def start(self):
           print("pass start")            
           pass

        def stop(self):
            print("pass stop")
            pass
