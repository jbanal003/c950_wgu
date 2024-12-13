class Package:
    def __init__(self, package_id, address, deadline, city, zipcode, weight, status):
        self.package_id = package_id
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zipcode = zipcode
        self.weight = weight
        self.status = status
        self.time_depart = None
        self.time_deliver = None

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.package_id, self.address, self.deadline, self.city, self.zipcode,
                                               self.weight, self.status)

    def status_update(self, time):
        if self.time_deliver < time:
            self.status = "Delivered"
        elif self.time_depart > time:
            self.status = "En route"
        else:
            self.status = "At the hub"