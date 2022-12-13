
class presureSensor:
    values = []
    newValues = []
    value = 0
    counter = 0

    def __init__(self, adcPin):
        self.adc = ADC(adcPin)

    def read(self):
        return self.adc.read_u16()

    def readAvarage(self, N):
        if(len(self.values) < N):
            self.values.append(self.adc.read_u16())
            self.value = self.adc.read_u16()
        else:
            self.values[0:N-1] = self.values[1:N]
            self.values[N-1] = self.adc.read_u16()
            self.value = int(sum(self.values)/N)
        return self.value