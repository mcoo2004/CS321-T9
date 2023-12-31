import sqlite3
import random
import os
from datetime import datetime

# Author: Isaiah Harville
# Function: Creates Pseudo Data to Populate the Hotel.db Database to demonstrate functionality of the program.
# Note: This is slow, it generates ~100,000 < x < ~1,500,000 guests who each have a booking and belong to a room which belongs to a hotel.  
#       It is only used to populate the databse, not for production.


class DataGenerator:
    def __init__(self):
        path = os.path.dirname(__file__)
        self.DB = sqlite3.connect(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "Hotel.db")))

        # Init Variables
        self.guestNum = 0
        self.roomSize = 0
        self.hotelNum = 0
        self.roomAmount = 0

        # Data Files
        self.hotels = open("%s\\Data\\hotels.txt"%path, "r").read().splitlines()
        self.firstNames = open("%s\\Data\\firstnames.txt"%path, "r").read().splitlines()
        self.lastNames = open("%s\\Data\\lastnames.txt"%path, "r").read().splitlines()
        self.emails = open("%s\\Data\\emails.txt"%path, "r").read().splitlines()
        self.phoneNumbers = open("%s\\Data\\phonenumbers.txt"%path, "r").read().splitlines()

        # Input Options
        task = {
            "1" : self.createTables,
            "2": self.generatePseudoHotels, # there is a line of succession
            "3" : self.deleteDB,             # each function calls the next one because without the previous
            "4" : self.end                  # data, it would not exist.  so to start we call hotels.  
        }                                    

        self.menu() # print the menu

        while True:
            task[self.validInput(input("> "))]() # get the input call function
            print("\n")
        

    # Menu
    def menu(self):
        print("   Data Generator")
        print("1. Create Tables")
        print("2. Generate Data")
        print("3. Delete Hotel.db")
        print("4. Exit\n")


    # Input Validation
    def validInput(self, string, parameters=["1","2","3","4"]):
        inp = str(string).lower()
        while 1:
            if inp in parameters:
                return inp
            inp = str(input(str))


    # Delete Hotel.db
    def deleteDB(self):
        if self.validInput("Are you sure you want to delete Hotel.db? (y/n) ", ["y", "n"]) == "y":
            print("Deleting Hotel.db...")
            os.remove(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "Hotel.db")))
            print("Done.")
    
        return


    # Exit
    def end(self):
        print("\n\n\n\nClosing...")
        self.DB.close()
        exit()


    # Create Tables
    def createTables(self):
        print("Creating Tables...")
        self.DB.execute(
        """
            CREATE TABLE Hotel
            (
                hotel_No INT PRIMARY KEY,
                name VARCHAR(50),
                city VARCHAR(50)
            );
        """
        )

        self.DB.execute(
        """
            CREATE TABLE Room
            (
                room_No INT,
                hotel_No INT,
                size INT,
                smoking BOOLEAN,
                pet BOOLEAN,
                price INT,
                PRIMARY KEY (room_No, hotel_No),
                FOREIGN KEY (hotel_No) REFERENCES Hotel(hotel_No)
            );
        """
        )

        self.DB.execute(
        """
            CREATE TABLE Guest
            (
                guest_No INT PRIMARY KEY,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                email VARCHAR(50),
                phone VARCHAR(50)
            );
        """
        )

        self.DB.execute(
        """
            CREATE TABLE Booking
            (
                guest_No INT,
                hotel_No INT,
                room_No INT,
                check_in_date STRING,
                check_out_date STRING,
                --PRIMARY KEY (hotel_No, room_No, check_in_date),
                FOREIGN KEY (guest_No) REFERENCES Guest(guest_No),
                FOREIGN KEY (hotel_No) REFERENCES Hotel(hotel_No),
                FOREIGN KEY (room_No) REFERENCES Room(room_No)
            );
        """
        )
        print("Done.")
        self.DB.commit()
        return


    # Generate Pseudo Hotels from hotels.txt
    def generatePseudoHotels(self):
        print("Creating Hotels...", end="")
        for i in range(0, len(self.hotels), 2):
            self.hotelNum += 1
            self.DB.execute(f"INSERT INTO Hotel VALUES ({self.hotelNum}, '{self.hotels[i]}', '{self.hotels[i+1]}')")
            self.generatePsuedoRooms()

        
        self.DB.commit()
        return


    # Generate 1000-5000 Pseudo Rooms per hotel with random room attributes, called by generatePseudoHotels
    def generatePsuedoRooms(self):
        print(f"\n\nCreating Rooms for Hotel {self.hotelNum}...")
        self.roomAmount = random.choice([1000, 2000, 3000, 4000, 5000])
        for i in range(1, self.roomAmount):
            self.roomSize = random.choice([2,3,4,5])
            self.roomNumber = i
            self.DB.execute(f"INSERT INTO Room VALUES ({self.roomNumber}, {self.hotelNum}, {self.roomSize}, {random.choice([True, False])}, {random.choice([True, False])}, {random.randint(80,100) if self.roomSize == 2 else random.randint(110, 300)})")
            self.generatePsuedoGuests()
        print(f"Done. Created {self.roomAmount} Rooms for Hotel {self.hotelNum}.")
        self.DB.commit()
        return


    # Generate Psuedo Guests per room size and a booking for each guest, called by generatePseudoRooms
    def generatePsuedoGuests(self):
        if self.roomNumber % 1000 == 0:
            print(f"Creating Guests and Bookings for Room {self.roomNumber}...")

        # Guests in the same room--stay for the same days.
        month = random.randint(1,12)
        startDay = random.randint(1,27)

        for i in range(1, self.roomSize):
            # Guests
            self.guestNum += 1
            self.DB.execute(f"INSERT INTO Guest VALUES ({self.guestNum}, '{random.choice(self.firstNames)}', '{random.choice(self.lastNames)}', '{random.choice(self.emails)}', '{random.choice(self.phoneNumbers)}')")
            
            # Bookings
            # self.DB.execute(f"INSERT INTO Booking VALUES ({self.guestNum}, {self.hotelNum}, {self.roomNumber}, '2023-{month}-{startDay}', '2023-{month}-{startDay+random.randint(3,8 if 30-startDay > 8 else 30-startDay)}')")

        self.DB.commit()
        return

    
    def generatePsuedoBookings(self, startingBookedRate, bookedDecrement):
        guestNos = self.DB.execute('SELECT guest_No FROM Guest').fetchall()
        bookedRate = startingBookedRate
        today = datetime.date.today()

        totalRooms = self.DB.execute('SELECT COUNT(*) FROM Room').fetchone()[0]

        getAvaibleRoomsQuery = 'SELECT hotel_No, room_No FROM Room WHERE (hotel_No, room_No) NOT IN (SELECT hotel_No, room_No FROM Booking WHERE check_in_date <= ? AND check_out_date > ?)'
        while bookedRate > 0:
            availableRooms = self.DB.execute(getAvaibleRoomsQuery, (today, today)).fetchall()
            numOfAvailableRooms = len(availableRooms)
            roomsToBook = int(totalRooms * bookedRate) - totalRooms + numOfAvailableRooms
            
            for i in range(roomsToBook):
                guestNo = random.choice(guestNos)[0]
                ndx = random.randint(0, len(availableRooms) - 1)
                hotelNo, roomNo = availableRooms[ndx]
                checkInDate = today
                checkOutDate = checkInDate + datetime.timedelta(days = random.randint(1, 7))
                self.DB.execute('INSERT INTO Booking VALUES (?, ?, ?, ?, ?)', (guestNo, hotelNo, roomNo, checkInDate, checkOutDate))
                del availableRooms[ndx]

            bookedRate -= bookedDecrement
            today += datetime.timedelta(days = 1)


DataGenerator()
