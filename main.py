# Name: Justin Banal
# Student ID: 010682100
# C950 WGUPS Routing Program

import csv
import datetime


# HashTable class using chaining.
class HashTable:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.

    def __init__(self, initial_capacity=100):

        # initialize the hash table with empty bucket list entries.
        self.list = []
        for i in range(initial_capacity):
            self.list.append([])

    # Inserts a new item into the hash table.
    def insert(self, key, item):  # does both insert and update

        # Get the bucket list where this item will go.
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]

        # Update key if it is already in the bucket
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        # If not, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    def search(self, key):

        # Get the bucket list where this key would be.
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]

        # Search for the key in the bucket list
        for pair in bucket_list:
            if key == pair[0]:
                return pair[1]  # value
        return None

    # Removes an item with matching key from the hash table.
    def remove_hash(self, key):

        # Get the bucket list where this item will be removed from.
        slot = hash(key) % len(self.list)
        slot_list = self.list[slot]

        # Remove the item from the bucket list if it is present.
        if key in slot_list:
            slot_list.remove(key)


# Class for Packages
class Package:
    def __init__(self, p_id, address, city, state, zipcode, deadline, weight, status):
        self.p_id = p_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.depart_time = None
        self.deliver_time = None
        self.truck_num = None

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.p_id, self.address, self.city, self.state, self.zipcode,
                                                           self.deadline, self.weight, self.deliver_time, self.status,
                                                           self.truck_num)

    def status_update(self, convert_timedelta):
        if self.deliver_time < convert_timedelta:
            self.status = "Delivered"
        elif self.depart_time > convert_timedelta:
            self.status = "En route"
        else:
            self.status = "At hub"


# Class for Trucks
class Truck:
    def __init__(self, truck_num, capacity, speed, load, packages, mileage, address, departure_time):
        self.truck_num = truck_num
        self.capacity = capacity
        self.speed = speed
        self.load = load
        self.packages = packages
        self.mileage = mileage
        self.address = address
        self.departure_time = departure_time
        self.time = departure_time

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (self.truck_num, self.capacity, self.speed, self.load, self.packages,
                                                   self.mileage, self.address, self.departure_time)


# Read from distance csv file
with open("distanceCSV.csv") as csv_distance:
    distance_file = csv.reader(csv_distance)
    distance_file = list(distance_file)

# Read from address csv file
with open("addressCSV.csv") as csv_address:
    address_file = csv.reader(csv_address)
    address_file = list(address_file)

# Read from package csv file
with open("packageCSV.csv") as csv_package:
    package_file = csv.reader(csv_package)
    package_file = list(package_file)


# Create package objects from csv file then load to hash table
def load_package_data(pack_file, hash_package):
    with open(pack_file, 'r', encoding='utf-8-sig') as p_info:
        package_data = csv.reader(p_info)
        for package in package_data:
            package_id = int(package[0])
            package_address = package[1]
            package_city = package[2]
            package_state = package[3]
            package_zipcode = package[4]
            package_deadline = package[5]
            package_weight = package[6]
            package_status = "At hub"

            # Package objects
            package_object = Package(package_id, package_address, package_city, package_state, package_zipcode,
                                     package_deadline, package_weight, package_status)

            # Insert objects to hash table
            hash_package.insert(package_id, package_object)


# Find distance between two addresses
def distance_between(address1, address2):
    distance = distance_file[address1][address2]
    if distance == '':
        distance = distance_file[address2][address1]

    return float(distance)


# Get address number from the address string
def get_address_num(address):
    for num in address_file:
        if address in num[2]:
            return int(num[0])


# Create truck objects
truck1 = Truck("truck 1", 16, 18, None, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], 0.0,
               "4001 South 700 East", datetime.timedelta(hours=8))
truck2 = Truck("truck 2", 16, 18, None, [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39],
               0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))
truck3 = Truck("truck 3", 16, 18, None, [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33], 0.0,
               "4001 South 700 East", datetime.timedelta(hours=9, minutes=5))

# Hash table instance
hash_package = HashTable()

# Load package to hash Table
load_package_data("packageCSV.csv", hash_package)


# Ordering packages on the truck using nearest neighbor algorithm
def deliver_package(truck):
    # Not delivered packages added to an array
    undelivered = []
    for pack_id in truck.packages:
        package = hash_package.search(pack_id)
        undelivered.append(package)

    # Clear package list to be able to load back to the truck
    truck.packages.clear()

    # Loop until each object in the list is delivered
    # Add nearest package to list one at a time
    while len(undelivered) > 0:
        next_address = 2000
        next_package = None
        for package in undelivered:
            if distance_between(get_address_num(truck.address), get_address_num(package.address)) <= next_address:
                next_address = distance_between(get_address_num(truck.address), get_address_num(package.address))
                next_package = package

        # Add nearest package to list
        truck.packages.append(next_package.p_id)

        # Remove from undelivered list
        undelivered.remove(next_package)

        # Add mileage to truck mileage
        truck.mileage += next_address

        # Update current address of truck to current address
        truck.address = next_package.address

        # Update time to time taken by truck to drive to the address
        truck.time += datetime.timedelta(hours=next_address / 18)
        next_package.deliver_time = truck.time
        next_package.depart_time = truck.departure_time
        next_package.truck_num = truck.truck_num


# Start loading process
deliver_package(truck1)
deliver_package(truck2)

# Start truck3 package delivery once either truck1 or truck2 is done delivering
truck3.departure_time = min(truck1.time, truck2.time)
deliver_package(truck3)


class Main:
    # User interface for the program
    print('Western Governor University Parcel Service (WGUPS) Routing Program')

    # Show total mileage for all trucks
    print(f'Total route mileage: {round(truck1.mileage + truck2.mileage + truck3.mileage, 2)} miles')

    # Ask user to type the word 'start' to start the program
    initial_text = input("Please type the word 'start'. Anything else will quit the program.   ")
    if initial_text == "start":
        try:
            # Ask user to type in HH:MM:SS format to check status of delivery
            time_info = input("Enter time in format of HH:MM:SS to check the status of a package.   ")
            (h, m, s) = time_info.split(":")
            convert_timedelta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

            target_time = "10:19:00"
            (h, m, s) = target_time.split(":")
            converted_target = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))

            package_nine = hash_package.search(9)

            if convert_timedelta > converted_target:
                package_nine.address = "410 S State St"
                package_nine.city = "Salt Lake City"
                package_nine.state = "UT"
                package_nine.zipcode = "84111"

            # Ask if user wants to check one package or all packages
            ask_package = input("Type 'one' to check status of one package or type 'all' to check all packages.   ")
            print('')
            if ask_package == "one":
                try:
                    # Ask user to input package ID
                    one_input = input("Enter package ID:   ")
                    package = hash_package.search(int(one_input))
                    package.status_update(convert_timedelta)
                    print(str(package))
                except ValueError:
                    print('Invalid entry. Program will now exit.')
                    exit()
            elif ask_package == "all":
                try:
                    for pack_id in range(1, 41):
                        package = hash_package.search(pack_id)
                        package.status_update(convert_timedelta)
                        print(str(package))
                except ValueError:
                    print("Invalid entry. Program will now exit.")
                    exit()
            else:
                exit()
        except ValueError:
            print("Invalid entry. Program will now exit.")
            exit()
    else:
        print("Invalid entry. Program will now exit.")
        exit()
