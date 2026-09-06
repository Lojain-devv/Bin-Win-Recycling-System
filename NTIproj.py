# Bin&Win - Recycling System 

#Person
import re

class Person:

    def __init__(self, username, password, phone):
        self._username = username
        self.__password = password
        self._phone = phone

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self.__password
    
    @property
    def phone(self):
        return self._phone

    def check_password(self, password):
        return self.__password == password

#Person : User

class User(Person):

    def __init__(self, username, password, phone, email, address, points=0):
        super().__init__(username, password, phone)

        self.__email = email
        self.__address = address
        self.__points = points

    @property
    def email(self):
        return self.__email

    @property
    def address(self):
        return self.__address

    @property
    def points(self):
        return self.__points
  

    def add_points(self, points):
        if points > 0:
            self.__points += points

    def deduct_points(self, points):
      if points > 0:
        self.__points -= points


    def show_profile(self):
        print('\n---- PROFILE ----')
        print('\nUsername:', self.username)
        print('Phone:', self.phone)
        print('Email:', self.email)
        print('Address:', self.address)
        print('Points:', self.points)

    def redeem_reward(self, rewards):

        print('\n---- REWARDS ----\n')

        try:
            for number, reward in rewards.items():
                print(f"{number}. {reward.name} -> {reward.points} points")

            choice = int(input("\nEnter reward number: "))

            if choice not in rewards:
                print("\nInvalid choice!")
                return

            reward = rewards[choice]

            if self.points >= reward.points:
                self.deduct_points(reward.points)

                print("\nCongratulations!")
                print(f"You redeemed: {reward.name}")
                print(f"Remaining points: {self.points}")

            else:
                print("\nYou don't have enough points!")

        except ValueError:
            print("\nPlease enter a number.")

    def recycling_request(self, system):

        print("\n---- MACHINE RECYCLING ----")

        waste_name = system.choose_waste_type()

        if waste_name is None:
            return

        quantity = system.enter_quantity()

        if quantity is None:
            return

        points = system.calculate_points(waste_name, quantity)

        request = RecyclingRequest(self.username, waste_name, quantity, points, "Machine")

        system.recycling_requests.append(request)

        request_number = len(system.recycling_requests)

        print("\n---- MACHINE REQUEST ----")
        print("Request created successfully")
        print(f"Request number: {request_number}")
        print(f"Waste type: {waste_name}")
        print(f"Quantity: {quantity}")
        print(f"Possible points: {points}")
        print("Request type: Machine")
        print("Status: Pending")


    def delivery_request(self, system):

        print("\n---- DELIVERY REQUEST ----")

        waste_name = system.choose_waste_type()

        if waste_name is None:
            return

        quantity = system.enter_quantity()

        if quantity is None:
            return

        points = system.calculate_points(waste_name, quantity)

        request = RecyclingRequest(self.username, waste_name, quantity, points, "Delivery", self.phone, self.address)

        system.recycling_requests.append(request)

        request_number = len(system.recycling_requests)

        print("\n---- DELIVERY REQUEST ----")
        print("Request created successfully")
        print(f"Request number: {request_number}")
        print(f"Waste type: {waste_name}")
        print(f"Quantity: {quantity}")
        print(f"Possible points: {points}")
        print("Request type: Delivery")
        print("Status: Pending")


    def confirm_machine_request(self, system):

        print("\n---- CONFIRM MACHINE REQUEST ----")

        found = False

        for i in range(len(system.recycling_requests)):

            request = system.recycling_requests[i]

            if (request.user == self.username
                    and request.request_type == "Machine"
                    and request.status == "Pending"):

                found = True
                request.show_request(i + 1)

        if not found:
            print("\nThere are no pending machine requests.")
            return

        try:

            request_number = int(input("\nEnter request number to confirm: "))

            index = request_number - 1

            if index < 0 or index >= len(system.recycling_requests):
                print("Invalid request number!")
                return

            request = system.recycling_requests[index]

            if request.user != self.username:
                print("This request does not belong to you!")
                return

            if request.request_type != "Machine":
                print("This is not a machine request!")
                return

            if request.status != "Pending":
                print("This request is not pending!")
                return

            request.update_status("Collected")
            self.add_points(request.points)

            print("\n---- RECYCLING CONFIRMED ----")
            print(f"Points added: {request.points}")
            print(f"Total points: {self.points}")

        except ValueError:
            print("Please, enter a number.")


    def view_requests(self, system):

        print("\n---- MY REQUESTS ----")

        found = False

        for i in range(len(system.recycling_requests)):

            request = system.recycling_requests[i]

            if request.user == self.username:
                found = True

                request.show_request(i + 1)

        if not found:
            print("\nYou have no requests.")


    def user_history(self, system):

        print("\n---- USER HISTORY ----")

        found = False

        for i in range(len(system.recycling_requests)):

            request = system.recycling_requests[i]

            if request.user == self.username:

                found = True

                print(f"{i + 1}. {request.waste_type} - {request.quantity} pieces - {request.status}")

        if not found:
            print("\nNo history found.")


#Person : Collector  

class Collector(Person):
    Penalty = 10

    def __init__(self, username, password, phone):
        super().__init__(username, password, phone)

    def view_pending_requests(self, system):
        print("\n---- PENDING REQUESTS ----")
        found = False
        for r in range(len(system.recycling_requests)):
            request = system.recycling_requests[r]
            if request.status == "Pending":
                found = True
                print(f"Request {r + 1}")
                print(f"User: {request.user}")
                print(f"Waste type: {request.waste_type}")
                print(f"Quantity: {request.quantity}")
                print(f"Points: {request.points}")
                print(f"Request type: {request.request_type}")

                if request.request_type == "Delivery":
                    print(f"Phone: {request.phone}")
                    print(f"Address: {request.address}")
                print(f"Status: {request.status}")
                
        if not found:
            print("\nThere are no pending requests.")
            return False
        return True


    def add_points_after_confirmation(self, system, request):

        username = request.user
        user = system.users[username]

        user.add_points(request.points)

        print(f"Points added to {username}: {request.points}")
        print(f"Total points: {user.points}")


    def confirm_request(self, system):

        print("\n---- CONFIRM DELIVERY REQUEST ----")

        if not self.view_pending_requests(system):
            return

        try:

            request_number = int(
                input("\nEnter request number to confirm: ")
            )

            index = request_number - 1

            if index < 0 or index >= len(system.recycling_requests):
                print("Invalid request number!")
                return

            request = system.recycling_requests[index]

            if request.status != "Pending":
                print("This request is not pending!")
                return

            if request.request_type != "Delivery":
                print("This is not a delivery request!")
                return

            request.update_status("Collected")

            print("---- DELIVERY CONFIRMED ----")
            print(f"Waste received from: {request.user}")
            print(f"Address: {request.address}")

            self.add_points_after_confirmation(system, request)

        except ValueError:
            print("Please, enter a number.")


    def reject_request(self, system):

        print("\n---- REJECT REQUEST ----")

        if not self.view_pending_requests(system):
            return

        try:

            request_number = int(
                input("\nEnter request number to reject: ")
            )

            index = request_number - 1

            if index < 0 or index >= len(system.recycling_requests):
                print("Invalid request number!")
                return

            request = system.recycling_requests[index]

            if request.status != "Pending":
                print("This request is not pending!")
                return

            if request.request_type != "Delivery":
                print("Only delivery requests can be rejected!")
                return

            request.update_status("Rejected")

            user = system.users[request.user]

            user.deduct_points(self.Penalty)

            print("---- REQUEST REJECTED ----")
            print("Waste information was incorrect.")
            print(f"User: {request.user}")
            print(f"Penalty: {self.Penalty}")
            print(f"Remaining points: {user.points}")

        except ValueError:
            print("Please, enter a number.")

#Rewards

class Reward:
    def __init__(self, number, name, points):
        self.__number = number
        self.__name = name
        self.__points = points

    @property
    def number(self):
        return self.__number

    @property
    def name(self):
        return self.__name

    @property
    def points(self):
        return self.__points

    def show(self):
        print(f"{self.name} -> {self.points} points")

#Wastes

class Waste:
    def __init__(self, name, points_per_piece):
        self.__name = name
        self.__points_per_piece = points_per_piece

    @property
    def name(self):
        return self.__name

    @property
    def points_per_piece(self):
        return self.__points_per_piece

    def calculate_points(self, quantity):
        return self.points_per_piece * quantity

#Requests

class RecyclingRequest:
    Statuses = ["Pending", "Collected", "Rejected"]

    def __init__(self, user, waste_type, quantity, points, request_type, phone=None, address=None):
        self.__user = user
        self.__waste_type = waste_type
        self.__quantity = quantity
        self.__points = points
        self.__status = "Pending"
        self.__request_type = request_type
        self.__phone = phone
        self.__address = address

    @property
    def user(self):
        return self.__user

    @property
    def waste_type(self):
        return self.__waste_type

    @property
    def quantity(self):
        return self.__quantity

    @property
    def points(self):
        return self.__points

    @property
    def status(self):
        return self.__status


    @property
    def request_type(self):
        return self.__request_type

    @property
    def phone(self):
        return self.__phone

    @property
    def address(self):
        return self.__address

    def update_status(self, status, show_message=True):
        self.__status = status
        if show_message:
            print("Request updated successfully!")
            print(f"New status: {self.status}")

    def show_request(self, request_number):
        print(f"Request {request_number}")
        print(f"User: {self.user}")
        print(f"Waste type: {self.waste_type}")
        print(f"Quantity: {self.quantity}")
        print(f"Points: {self.points}")
        print(f"Request type: {self.request_type}")
        if self.request_type == "Delivery":
            print(f"Phone: {self.phone}")
            print(f"Address: {self.address}")
        print(f"Status: {self.status}")


#System

class RecyclingSystem:

    def __init__(self):
        self.users = {}
        self.collectors = {}
        self.rewards = {}
        self.waste_types = {}
        self.recycling_requests = []

        self.load_users()
        self.load_collectors()
        self.load_rewards()
        self.load_waste_types()


    def load_users(self):
        self.users = {"Ahmed": User("Ahmed", "A@12345a", "0654321",
                                    "Ahmed@gmail.com", "Cairo", 500),

                    "Aly": User("Aly", "A@56784a", "0123456",
                                "Aly@gmail.com", "Alex", 1000),

                    "Sherif": User("Sherif", "S@13144s", "0345678",
                                   "Sherif@gmail.com", "Aswan", 200)}


    def load_collectors(self):
        self.collectors = {"collector1": Collector("collector1", "C@10123c", "01234567891"),
                           "collector2": Collector("collector2", "C@20124c", "01234567892"),
                           "collector3": Collector("collector3", "C@30125c", "01234567893")}


    def load_rewards(self):
        self.rewards = {
            1: Reward(1, "Reusable Bag", 50),
            2: Reward(2, "10% Discount", 100),
            3: Reward(3, "20 EGP Voucher", 200),
            4: Reward(4, "Free Shipping", 500),
            5: Reward(5, "Gift Card", 1000)}


    def load_waste_types(self):
        self.waste_types = {"paper": Waste("paper", 2),
                            "plastic": Waste("plastic", 3),
                            "metal": Waste("metal", 6),
                            "glass": Waste("glass", 4)}


    def register(self):

        username = input("\nEnter username: ")

        if username in self.users:
            print("\nUsername already exists!")
            return

        password = input("Enter password: ")

        while not (
            len(password) >= 8
            and re.search(r'[A-Z]', password)
            and re.search(r'[a-z]', password)
            and re.search(r'\d', password)
            and re.search(r'[!@#$%^&*]', password)):

            print("\nPassword must be at least 8 characters, contain uppercase, lowercase, digit, and [!@#$%^&*].")

            password = input("Enter password again: ")

        phone = input("Enter phone number: ")

        while not phone.isdigit():

            print("\nInvalid phone number!")
            phone = input("Enter phone number again: ")

        email = input("Enter email: ")

        while "@" not in email or "." not in email:

            print("\nInvalid email!")
            email = input("Enter email again: ")

        address = input("Enter address: ")

        while not address.strip():

            print("\nAddress cannot be empty!")
            address = input("Enter address again: ")

        self.users[username] = User(username, password, phone, email, address)

        print("\nAccount created successfully at Bin&Win!\n")


    def login(self):

        username = input("\nEnter username: ")

        if username not in self.users:
            print("\nUsername not found!\n")
            return None

        user = self.users[username]

        max_attempts = 3
        attempts_made = 0

        print("\nYou have 3 attempts to enter your password")

        while attempts_made < max_attempts:

            password = input("Enter your password: ")
            attempts_made += 1

            if user.check_password(password):

                print("\nPassword accepted!")
                print("\nLogin successful! Hello", username)

                return user

            print("\nIncorrect password!")

            remaining = max_attempts - attempts_made

            if remaining > 0:
                print(f"\nYou have {remaining} attempts left.")

        print("You have reached maximum attempts. Access denied.\n")

        return None


    def collector_login(self):

        username = input("\nEnter your username: ")

        if username not in self.collectors:
            print("\nUser not found\n")
            return None

        collector = self.collectors[username]

        max_attempts = 3
        attempts_made = 0

        print("\nYou have 3 attempts to enter your password")

        while attempts_made < max_attempts:

            password = input("Enter your password: ")
            attempts_made += 1

            if collector.check_password(password):

                print("\nWelcome collector!")

                return collector

            print("\nIncorrect password!")

            remaining = max_attempts - attempts_made

            if remaining > 0:
                print(f"You have {remaining} attempts left.")

        print("You have reached maximum attempts. Access denied.\n")

        return None
    

    def choose_waste_type(self):

        print("\n=== WASTE TYPE ===\n")

        waste_list = list(self.waste_types.keys())

        for c in range(len(waste_list)):

            waste = self.waste_types[waste_list[c]]

            print(f"{c + 1} - {waste.name} -> {waste.points_per_piece} points/piece")

        try:

            choice = int(input("\nChoose waste type: "))

            if choice < 1 or choice > len(waste_list):
                print("\nInvalid waste type!")
                return None

            return waste_list[choice - 1]

        except ValueError:

            print("\nPlease, enter a number.")
            return None


    def enter_quantity(self):

        try:

            quantity = int(input("\nEnter quantity: "))

            if quantity <= 0:
                print("\nInvalid quantity!")
                return None

            return quantity

        except ValueError:

            print("\nPlease, enter a number.")
            return None


    def calculate_points(self, waste_name, quantity):

        return self.waste_types[waste_name].calculate_points(quantity)


    def show_rewards(self):

        print("\n---- REWARDS ----\n")

        for reward in self.rewards.values():
            reward.show()


    def recycling_menu(self, user):

        while True:

            print("\n---- RECYCLING MENU ----")

            print("\n1. Drop off waste at machine")
            print("2. Request collector for delivery")
            print("3. Confirm machine recycling")
            print("4. View requests")
            print("5. Back to user menu")

            choice = input("\nChoose: ")

            if choice == "1":
                user.recycling_request(self)

            elif choice == "2":
                user.delivery_request(self)

            elif choice == "3":
                user.confirm_machine_request(self)

            elif choice == "4":
                user.view_requests(self)

            elif choice == "5":
                break

            else:
                print("Invalid choice!")


    def user_menu(self, user):

        while True:

            print("\n---- USER MENU ----")

            print("\n1. Show Profile")
            print("2. Show Rewards")
            print("3. Redeem Reward")
            print("4. Recycling Menu")
            print("5. User History")
            print("6. Logout")

            choice = input("\nChoose: ")

            if choice == "1":
                user.show_profile()

            elif choice == "2":
                self.show_rewards()

            elif choice == "3":
                user.redeem_reward(self.rewards)

            elif choice == "4":
                self.recycling_menu(user)

            elif choice == "5":
                user.user_history(self)

            elif choice == "6":
                print("\nLogged out. Thank you for visiting!!\n")
                break

            else: print("Invalid choice!")


    def collector_menu(self, collector):

        while True:

            print("\n---- COLLECTOR MENU ----\n")

            print("1. View Pending Requests")
            print("2. Confirm Delivery Request")
            print("3. Reject Delivery Request")
            print("4. Logout")

            choice = input("\nChoose: ")

            if choice == "1":
                collector.view_pending_requests(self)

            elif choice == "2":
                collector.confirm_request(self)

            elif choice == "3":
                collector.reject_request(self)

            elif choice == "4":
                print("\nLogged out. Thank you!\n")
                break

            else: print("Invalid choice!")


    def run(self):

        while True:

            print("\n== Bin&Win ==\n")

            print("1. Register")
            print("2. Customer Login")
            print("3. Collector Login")
            print("4. Exit")

            choice = input("\nChoose Option: ")

            if choice == "1":

                self.register()

            elif choice == "2":

                user = self.login()

                if user is not None:
                    self.user_menu(user)

            elif choice == "3":

                collector = self.collector_login()

                if collector is not None:
                    self.collector_menu(collector)

            elif choice == "4":

                print("\nGoodbye! Thank you for visiting Bin&Win.")
                break

            else: print("\nInvalid choice!")

system = RecyclingSystem()
system.run()
