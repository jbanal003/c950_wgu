class Truck:
    def __init__(self, capacity, load, speed, packages, miles, address, time_depart):
        self.capacity = capacity
        self.load = load
        self.speed = speed
        self.packages = packages
        self.miles = miles
        self.address = address
        self.time_depart = time_depart

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.capacity, self.load, self.speed, self.packages, self.miles,
                                                   self.address, self.time_depart)