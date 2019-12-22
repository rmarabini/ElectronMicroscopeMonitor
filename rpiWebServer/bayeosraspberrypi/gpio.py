"""Raspberry GPIO class to simplify GPIO handling."""
import RPi.GPIO

class GPIO(object):
    """GPIO class to simplify GPIO handling."""
    def __init__(self, addr_pins, en_pin, data_pin):
        """Initializes GPIO board."""
        self.addr_pins = addr_pins;  # address pins
        self.en_pin = en_pin;  # enable pin
        self.data_pin = data_pin;  # data pin

        RPi.GPIO.setmode(RPi.GPIO.BOARD)
        try:
            # set address pins as output
            for pin in self.addr_pins:
                RPi.GPIO.setup(pin, RPi.GPIO.OUT)
                RPi.GPIO.output(pin, RPi.GPIO.LOW)

            # initialize enable pin
            RPi.GPIO.setup(self.en_pin, RPi.GPIO.OUT)
            RPi.GPIO.output(self.en_pin, RPi.GPIO.LOW)

            # initialize data pin
            RPi.GPIO.setup(self.data_pin, RPi.GPIO.OUT)
            RPi.GPIO.output(self.data_pin, RPi.GPIO.LOW)
        except KeyboardInterrupt:
            RPi.GPIO.cleanup()

    def enable(self):
        """Briefly invokes the enable pin. Thus, the data pin is set on the right address."""
        RPi.GPIO.output(self.en_pin, RPi.GPIO.HIGH);
        # print 'EN is high'
        RPi.GPIO.output(self.en_pin, RPi.GPIO.LOW);
        # print 'EN is low'

    def address(self, addr):
        """Right pins will be invoked for a given address.
        @addr: number between 0 and a certain max address
        """
        for i in range(0, 6):  # ADR[0]=11, ADR[1]=12...
            RPi.GPIO.output(self.addr_pins[i], ((1 << i) & addr))

    def set_addr(self, addr):
        """Invokes the right pins to a given address, activates the data pin and briefly invokes the enable pin.
        @addr: number between 0 and a certain max address
        """
        self.address(addr)  # Addresse anlegen"
        RPi.GPIO.output(self.data_pin, 1);  # Data auf 1 fuer Spuelen setzen
        self.enable()  # Data auf Adresse uebenehmen
        print "address: %d - %d" % (addr, 1)

    def reset(self):
        """Disables the data pin."""
        RPi.GPIO.output(self.data_pin, 0);  # Spuelvorgang beenden
        self.enable()  # Data auf Adresse uebenehmen
        print "address: %d - %d" % (0, 0)

    def cleanup(self):
        """Disables all pins."""
        RPi.GPIO.cleanup()