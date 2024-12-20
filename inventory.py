#**************welcome to inventory.py Capstone project task*******************
# Importing the tabulate function from the tabulate library
from tabulate import tabulate


class Shoe:
    """
    A class to represent a shoe product.

    Attributes:
    ----------
    country : str
        The country where the shoe is manufactured.
    code : str
        The product code of the shoe.
    product : str
        The name of the shoe product.
    cost : float
        The cost price of the shoe.
    quantity : int
        The number of shoes available in stock.
    """

    def __init__(self, country, code, product, cost, quantity):
        """
        Initialize the shoe object with its attributes: country, code,
        product, cost, and quantity.
        The code and product are stored in lowercase to allow
        case-insensitive comparisons.
        """
        self.country = country
        self.code = code.lower()  # Convert code to lowercase for consistent comparisons
        self.product = product.lower()  # Convert product name to lowercase for consistency
        self.cost = float(
            cost)  # Convert cost to a float to handle prices correctly
        self.quantity = int(
            quantity)  # Convert quantity to an integer to handle stock

    def get_cost(self):
        """
        Returns the cost of the shoe.
        """
        return self.cost

    def get_quantity(self):
        """
        Returns the quantity of shoes in stock.
        """
        return self.quantity

    def __str__(self):
        """
        Returns a string representation of the shoe object.
        Formats the data to display the country, code, product name,
        cost, and quantity in a readable format.
        """
        return (f"{self.country} | {self.code.upper()} | "
                f"{self.product.capitalize()} | {self.cost} | "
                f"{self.quantity}")


# List to store all shoe objects
shoe_list = []


def read_shoes_data():
    """
    Reads data from the inventory.txt file and populates the shoe_list
    with Shoe objects. Each line in the file is split into the respective
    attributes needed to create a Shoe object.

    The first line is skipped as it contains headers.

    Error Handling:
    ---------------
    FileNotFoundError:
        Catches the error if the inventory.txt file is not found.
    """
    try:
        with open("inventory.txt", "r") as file:
            file.readline()  # Skip the header line
            # For each line, split the data and create a Shoe object
            for line in file:
                country, code, product, cost, quantity = line.strip().split(
                    ',')
                shoe = Shoe(country, code, product, cost, quantity)
                shoe_list.append(shoe)
    except FileNotFoundError:
        print("Error: inventory.txt file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def capture_shoes():
    """
    Captures new shoe data from the user and adds it to the shoe_list.
    Uses helper functions to validate inputs for text, float, and integers.
    After capturing the data, the shoe_list is updated in the inventory file.
    """
    country = get_valid_text_input("Enter the country: ")
    code = get_valid_text_input("Enter the code: ")
    product = get_valid_text_input("Enter the product name: ")
    cost = get_valid_float_input("Enter the cost: ")
    quantity = get_valid_int_input("Enter the quantity: ")
    shoe = Shoe(country, code, product, cost, quantity)  # Create Shoe object
    shoe_list.append(shoe)  # Add the new shoe to the shoe list
    update_inventory_file()  # Update the inventory.txt file with the new shoe


def get_valid_text_input(prompt):
    """
    Repeatedly prompts the user until they provide a valid alphabetic
    string input. Ensures no numbers or special characters are entered.
    """
    while True:
        user_input = input(prompt)
        if user_input.isalpha():  # Check if input contains only letters
            return user_input
        else:
            print("Invalid input! Please enter letters only (no numbers).")


def get_valid_float_input(prompt):
    """
    Prompts the user for a valid floating-point number, ensuring
    that the value is non-negative. It loops until a valid number is given.
    """
    while True:
        try:
            value = float(input(prompt))  # Try to convert input to float
            if value >= 0:  # Ensure the value is non-negative
                return value
            else:
                print(
                    "Cost cannot be negative. Please enter a positive number.")
        except ValueError:
            print("Invalid input! Please enter a valid number.")


def get_valid_int_input(prompt):
    """
    Prompts the user for a valid integer input, ensuring that
    the value is non-negative. Loops until valid input is provided.
    """
    while True:
        try:
            value = int(input(prompt))  # Try to convert input to integer
            if value >= 0:  # Ensuring value is non-negative
                return value
            else:
                print(
                    "Quantity cannot be negative. Please enter a positive number.")
        except ValueError:
            print("Invalid input! Please enter a valid integer.")


def view_all():
    """
    Displays all shoes in the inventory in a tabular format. If no shoes
    are found in the list, it displays a message. Uses the tabulate function
    to neatly display the list of shoes as a table.
    """
    if not shoe_list:
        print("No shoes in inventory.")
        return
    # Prepare the data for tabulation by extracting shoe attributes into a list
    table = [[shoe.country, shoe.code.upper(), shoe.product.capitalize(),
              shoe.cost, shoe.quantity] for shoe in shoe_list]

    # Display the data as a grid using the tabulate function
    print(tabulate(table, headers=["Country", "Code", "Product", "Cost",
                                   "Quantity"], tablefmt="grid"))


def re_stock():
    """
    Identifies the shoe with the lowest quantity in stock and allows
    the user to add more stock. The user is prompted to input how much
    to restock, and the inventory is updated accordingly.
    """
    if not shoe_list:
        print("No shoes in inventory.")
        return
    # Find the shoe with the lowest quantity using the min function
    lowest_qty_shoe = min(shoe_list, key=lambda x: x.get_quantity())
    print(f"Product with the lowest quantity: {lowest_qty_shoe}")

    # Ask the user how much to restock for the selected shoe
    add_quantity = get_valid_int_input(
        f"Enter quantity to restock for {lowest_qty_shoe.product.capitalize()}: ")

    # Update the shoe's quantity and write the changes to the file
    lowest_qty_shoe.quantity += add_quantity
    update_inventory_file()


def search_shoe():
    """
    Searches for a shoe by its product code. The user is prompted to enter
    a product code, and the search is case-insensitive. If the shoe is found,
    its details are printed. If not, a message is displayed.
    """
    code = input(
        "Enter the product code: ").lower()  # Input the code to search for
    for shoe in shoe_list:
        if shoe.code == code:  # Compare code in lowercase for case-insensitivity
            print(shoe)
            return
    print(f"No product found with code {code.upper()}.")


def value_per_item():
    """
    Calculates the total value for each shoe using the formula:
    value = cost * quantity. The results are displayed in a tabular format.
    """
    table = []
    # Calculate the total value of each shoe and prepare data for the table
    for shoe in shoe_list:
        value = shoe.get_cost() * shoe.get_quantity()
        table.append([shoe.country, shoe.code.upper(),
                      shoe.product.capitalize(), shoe.cost,
                      shoe.quantity, value])

    # Display the table using the tabulate function
    print(tabulate(table, headers=["Country", "Code", "Product", "Cost",
                                   "Quantity", "Value"], tablefmt="grid"))


def highest_qty():
    """
    Identifies the shoe with the highest quantity in stock and displays
    it as being "For Sale." If no shoes are in stock, a message is displayed.
    """
    if not shoe_list:
        print("No shoes in inventory.")
        return
    # Find the shoe with the highest quantity using the max function
    highest_qty_shoe = max(shoe_list, key=lambda x: x.get_quantity())
    print(f"Product with the highest quantity (For Sale): "
          f"{highest_qty_shoe.product.capitalize()}")


def update_inventory_file():
    """
    Updates the inventory.txt file with the current state of the shoe_list.
    Writes each shoe's data back to the file in CSV format.
    """
    try:
        with open("inventory.txt", "w") as file:
            # Write headers first
            file.write("Country,Code,Product,Cost,Quantity\n")
            # Write each shoe's attributes to the file
            for shoe in shoe_list:
                file.write(f"{shoe.country},{shoe.code},{shoe.product},"
                           f"{shoe.cost},{shoe.quantity}\n")
    except Exception as e:
        print(f"An error occurred while updating the file: {e}")


def main_menu():
    """
    Displays the main menu of the Shoe Inventory Management System.
    The menu allows the user to view all shoes, search by code, restock,
    calculate value, or capture a new shoe. The menu keeps prompting until
    the user chooses to exit.
    """
    # Read data from the file once at the start of the program
    read_shoes_data()

    while True:
        # Display the main menu options
        print("\nShoe Inventory Management System")
        print("1. View All Shoes")
        print("2. Search Shoe by Code")
        print("3. Restock Shoes with Lowest Quantity")
        print("4. Calculate Value per Item")
        print("5. Show Shoes with Highest Quantity (For Sale)")
        print("6. Capture New Shoe")
        print("7. Exit")

        # Get the user's choice
        choice = input("Enter your choice: ").lower()
        if choice == '1':
            view_all()
        elif choice == '2':
            search_shoe()
        elif choice == '3':
            re_stock()
        elif choice == '4':
            value_per_item()
        elif choice == '5':
            highest_qty()
        elif choice == '6':
            capture_shoes()
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


# Run the menu if the script is run directly
if __name__ == "__main__":
    main_menu()

#*****************************END OF PROGRAM***********************************

