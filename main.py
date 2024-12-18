'''
  File Name: Tuibuen_ISPShoppingList
  Author: Joshua T
  Email Address: tuibuej002@tcdsb.ca
  Date Created: 4/14/2024
  Description: A program that creates, edits and downloads shopping lists. 
'''
from typing import List, Dict
import time
import instructions

running = True
subtotal = 0.0
totalCost = 0.0
fileName = ""

class CreateShoppingList:
    """ A class for creating the shopping list. 

    Attributes:
      subtotal (float): The subtotal for the current products in the list.
      totalCost (float): The total cost for the current products in the list.

    Methods:
      __init__(self, subtotal, totalCost, fileName): 
          Constructs the attributes: subtotal, totalCost and fileName which is set to self.

      createLists(self):
          Creates the shopping list for the user, by appending the input values to the
          price/item/count lists and filtering any duplicates. 

      getItemPrice(self):
          A getter method that gets the individual item cost (without tax).

      getSubtotal(self):
          A getter method that returns the subtotal of the list.

      getTotalCost(self):
          A getter method that returns the total cost of the list.

      getItemListLength(self):
          A getter method that returns the item list's length.

    """
    # Constant Class Field
    ONTARIO_SALES_TAX = 1.13

    # Variable Class Fields
    itemList: List[str] = [] # The item list
    individualItemPrice: List[float] = [] # Costs for each individual item
    countOfItem: List[int] = [] # Counts for each item

    def __init__(self, subtotal, totalCost) -> None:
        """ Initializes the current attributes of the CreateShoppingList class.

        Args:
          subtotal (float): The subtotal of the list created by the user
          totalCost (float): The total cost of the list creater by the user.
          itemPrice (float): The cost of each item inputted by the user (without tax).
          itemCount (int): The count of each item inputted by the user.
          items (str): The items specified to place in the list.

        Returns:
          None

        """
        try:
            self.subtotal = subtotal
            self.totalCost = totalCost

            """
                Implement input methods for the user to add their own items to the list.
                Error checks for any invalid values that show up. 
            """

            # Item Input
            self.items = input("\nEnter Your Item: ").lower()

            # Keyword for exiting this class, and moving on to the shopping list menu
            if self.items == "exit":
                self.itemCount = 0 # Set to 0, because nothing else should be instantiated for "exit"
                self.itemPrice = 0.0
                return

            # Price Input
            self.itemPrice = float(input("Enter Your Price (CAD$): "))
            while (self.itemPrice < 0):
                self.itemPrice = float(input("Try Again ($0.00 or More!): "))

            # Item Count Input 
            self.itemCount = int(input("How Many: "))
            while (self.itemCount <= 0):
                self.itemCount = int(input("Try Again (1 Item or More!): "))

            print("\nItem Successfully Added. ")
            print("To exit, type 'exit' in the item field!")

        except Exception as err:
            """
                Tag to indicate an incomplete addition.
                def createLists() will check for this tag and purge any entries 
                corresponding to it.
            """
            self.items = "NOT_EXISTENT"

            print("\n**")
            print("Adding the item was unsuccessful.")
            print("Please enter valid values next time!")
            print(f"\nERROR LOG: {err}") 

    def createLists(self) -> bool:
        """ Initializes the current attributes of the CreateShoppingList class. 

        Args:
          None

        Returns:
          bool: Returns False if certain processes have ended, returning the program to the
          shopping list menu.

        """
        while True:
            try:
                individualCost = self.getItemPrice() # Call the getter method for item pricing
                self.itemList.append(self.items) # Append the items to the item list
                self.individualItemPrice.append(individualCost) # Append these costs from the getter method
                self.countOfItem.append(self.itemCount) # Append the item count to the item count list

                """
                    For the index and item in the list, check if "exit" or 
                    "NON_EXISTENT" is in it.

                     - Both indexes for 'itemlist', 'individualItemPrice', 'countOfItem' correspond 
                       to each other.
                     - Ex. If "Apple", "9", "2" are at index 0, then that is the item, its 
                       corresponding price, and count.
                """

                for i, item in enumerate(self.itemList):
                    if "NOT_EXISTENT" in item:
                        del self.itemList[i] # Delete position of "NON_EXISTENT"
                        del self.individualItemPrice[i] # Delete price of "NON_EXISTENT"
                        del self.countOfItem[i] # Delete count of "NON_EXISTENT"

                    if "exit" in item:
                        del self.itemList[i] # Delete the position of "exit"
                        del self.individualItemPrice[i] # Delete the price of "exit"
                        del self.countOfItem[i] # Delete the count of "exit"

                        # Initialize variables for the two-pointer method
                        pointerA = 0 # Start at list[0], referred as the "left pointer"
                        pointerB = (len(self.itemList) - 1) # Start at the end of the list, referred as "right pointer"

                        """
                            Implements a two-pointer approach for duplicate items.
                            This algorithm allows to compare all the values 
                            to a given index, starting at index 0.

                            e.g. Given a list, where indices of list are [0, 1, ... 5]

                                 List[0] (Left Pointer) is compared to List[5, 4, ..., 1] (Right Pointer)
                                 List[1] is compared to List[5, 4, ..., 2] and so on.

                            So when two pointers are equal in this case, merge
                            any integer values together, i.e. Count, price, and remove
                            the the entry from the pointer on the right hand side of
                            the list.
                        """
                        while (pointerA < (len(self.itemList)) - 1): # This is constant, the reason why it doesn't equal the left.
                            while pointerA < pointerB: # Left pointer is constantly being deducted until right increases.

                                # Equality check, get similar indices
                                if self.itemList[pointerA] == self.itemList[pointerB]:

                                    # Merge the prices of the right pointer to the left one
                                    self.individualItemPrice[pointerA] = (self.individualItemPrice[pointerA]
                                                                          + self.individualItemPrice[pointerB])

                                    # Merge the count of the right pointer to the left one
                                    self.countOfItem[int(pointerA)] = (self.countOfItem[pointerA]
                                                                       + self.countOfItem[pointerB])

                                    """
                                        Fully deletes the indexes where the rightmost pointer 
                                        has already verified the equality above.
                                    """
                                    del self.itemList[pointerB] 
                                    del self.individualItemPrice[pointerB]
                                    del self.countOfItem[pointerB]

                            # Subtract left pointer index until left <= right
                                pointerB -= 1

                            else:
                                """
                                    Continue on with the left pointer to move to the next 
                                    item in the list.

                                    Reset the value of pointerB to keep in check with the 
                                    current list length after deleting the indices.
                                """
                                pointerA += 1
                                pointerB = len(self.itemList) - 1
                                continue

                        return False

                # Go back, and initialize more values for the user until "exit" is input.
                CreateShoppingList.__init__(self, subtotal, totalCost)

            except AttributeError:
                selectionMenu()
                return False

    def getItemPrice(self) -> float | bool:
        """ Getter method for the item pricing, by multiplying the count of the item and 
          multiplying it by price.

        Args:
            None

        Returns:
            individualCost (float): The individual cost of the item.
            bool: Returns False to return to the selection list screen for the shopping list.

        """
        try:
            individualCost = round((self.itemCount * self.itemPrice), 2)
            return individualCost

        except Exception as err:
            print(f"An error occured getting the item's price! {err}")
            return False

    def getSubtotal(self) -> float | bool:
        """ Getter method for the subtotal, by summating all the indexes 
            in the 'individualItemPrice' list.

        Args:
            None

        Returns:
            subtotal (float): The subtotal for all of the products.
            bool: Returns False to return to the selection list screen for the shopping list.

          """
        try:
            for i in range(0, len(self.individualItemPrice)):
                self.subtotal = (self.subtotal + self.individualItemPrice[i])
            return self.subtotal

        except Exception as err:
            print(f"An error occured getting the item's subtotal! {err}")
            return False

    def getTotalCost(self) -> float | bool:
        """ Getter method for the total, by getting the subtotal, 
            and multiplying it with the current sales tax (13%)

        Args:
            None

        Returns:
            totalCost (float): The totalCost for all of the products.
            bool: Returns False to return to the selection list screen for the shopping list.

          """
        try:
            self.totalCost = (self.subtotal * CreateShoppingList.ONTARIO_SALES_TAX)
            return self.totalCost

        except Exception as err:
            print(f"An error occured getting the item's total cost! {err}")
            return False

    def getItemListLength(self) -> int:
        """ Getter method for the list length for items.

        Args:
            None

        Returns:
            int: The length of the current item list.

        """
        return len(self.itemList)

class DownloadShoppingList(CreateShoppingList):
    """ A class for downloading (or viewing) the shopping list.

    Attributes:
        subtotal (float): The subtotal for the current products in the list.
        totalCost (float): The total cost for the current products in the list.
        fileName (str): The specified file name to create the list off of.

    Methods:
        __init__(self, subtotal, totalCost, fileName): 
        Constructs the attributes: subtotal, totalCost and fileName which is set to self.

        downloadChoice(self):
            Asks the user if they want to save the file or not. If so, then continue to 
            createFile(), if not, then return to the menu for the shopping list.

        createFile(self):
            Creates the file, by asking the user for their desired file name, then creates 
            and writes the table based off of the current list and dictionary data.

        getDict(self):
            A getter method that returns the current dictionary's key and value pairs.

        getFileName(self):
            A getter method that returns the specified file name. 

    """
    choiceBoolean = True
    counter = 0

    def __init__(self, subtotal, totalCost, fileName) -> None:
        """ Initializes the current attributes of the DownloadShoppingList class. 

        Args:
          None

        Returns:
          None

        """
        try:

            self.subtotal = subtotal
            self.totalCost = totalCost
            self.fileName = fileName

            # For each indice, get the key/value pairs based off of the the item and price lists
            self.savedItems = {CreateShoppingList.itemList[i]: 
                               CreateShoppingList.individualItemPrice[i] 
                               for i in range(0, CreateShoppingList.getItemListLength(self))}

            print("\nCURRENT LIST:")
            print(f"\n\tITEMS: {CreateShoppingList.itemList}")
            print(f"\tITEM COUNT: {CreateShoppingList.countOfItem}")
            print(f"\tINDIVIDUAL COST (NO TAX): {CreateShoppingList.individualItemPrice}")
            print(f"\tSUBTOTAL: ${str(round(self.getSubtotal(), 2))}")
            print(f"\tTOTAL COST: ${str(round(self.getTotalCost(), 2))}")

        except Exception as err:
            print(f"Something went wrong! ERROR: {err}")

    def downloadChoice(self) -> None:
        """ Asks the user whether or not they want to save their current list.
            If not, then return to menu, if so then continue to creating the file. 

        Args:
            None

        Returns:
            None

        """

        self.userChoice = input("\nAre you sure you want to download? (Y/N): ").lower()

        # User wants to download the list
        if self.userChoice == "y":
            DownloadShoppingList.choiceBoolean = True
            print("Continuing... \n")
            time.sleep(1)

        # User does not want to download the list
        elif self.userChoice == "n":
            DownloadShoppingList.choiceBoolean = False
            print("Returning to Menu...")
            time.sleep(1)

    def createFile(self) -> None:
        """ Creates the file for the user based on the current data they have given.
            It will create a new file if it does not exist, but will also overwrite any 
            data for existing files.

        Args:
            None

        Returns:
            None

        """
        try:
            self.fileName = input("Enter a File Name: ")

            # Clear any existing data over a file 
            with open(f"{self.fileName}.txt", "w", encoding="utf-8") as file:
                print("\nClearing file data before handling...")
                time.sleep(1)
                file.close()

            # Then, open the file to write any new data 
            with open(f"{self.fileName}.txt", "a+", encoding="utf-8") as file:  

                # The max row lengths for the table headers.
                # Mainly based off of the length of the longest item/price/count
                maxItemRowLength = (max(len(i) for i in
                                            CreateShoppingList.itemList))
                maxCountRowLength = (max(len(str(j)) for j in 
                                            CreateShoppingList.countOfItem))
                maxCostRowLength = (max(len(str(k)) for k in 
                                            CreateShoppingList.individualItemPrice))

                # TABLE HEADERS FOR ITEM, COUNT, COST
                file.write(
                    "ITEM" + (" "*(maxItemRowLength+1))
                    + "COUNT"+ (" "*(maxCountRowLength+2))
                    + "COST" + (" "*(maxCostRowLength+1))
                    + "\n"
                )

                # TABLE BODY
                file.write(
                    ("*" + ("-" * (maxItemRowLength + 2)) + "*" 
                    + ("-" * (maxCountRowLength + 6)) + "*"
                    + ("-" * (maxCostRowLength + 3)) + "*")
                    + "\n"
                )

                # TABLE CONTENT ROWS (ITEMS, COUNT, INDIVIDUAL COST)
                # The format statements (f"") just say to print out the desired content, 
                # with a left alignment of x amount of characters.
                for k, v in self.savedItems.items():
                    file.write(
                        ("|" + f"{k.upper():<{maxItemRowLength}}" + "  |"
                        + " " + f"{CreateShoppingList.countOfItem[DownloadShoppingList.counter]:<{maxCountRowLength}}" + "     |"
                        + " " + f"${v:<{maxCostRowLength}}" + " |")
                        + "\n"
                    )

                    DownloadShoppingList.counter += 1

                # TABLE END
                file.write(
                    ("*" + ("-" * (maxItemRowLength + 2)) + "*" 
                    + ("-" * (maxCountRowLength + 6)) + "*"
                    + ("-" * (maxCostRowLength + 3)) + "*")
                    + "\n"
                )

                # SUBTOTAL, TOTAL COST (DIVDED BY TWO TO GET ACTUAL)
                file.write(
                    f"SUBTOTAL: ${round(CreateShoppingList.getSubtotal(self) / 2, 2)}" 
                    + (" "*(maxItemRowLength+1))

                    + f"\nTOTAL COST: ${round(CreateShoppingList.getTotalCost(self) / 2, 2)}" 
                    + (" "*(maxCountRowLength+2))
                )

                file.close()

                # Must reset before entering this menu again
                # Otherwise, the list index is out of range
                DownloadShoppingList.counter = 0

                time.sleep(1)
                print("Writing data...")

                time.sleep(2)
                print("Write to file successful.")
                print("Check around this program's folder for the text data!")

                time.sleep(1)
                return

        except Exception as err:
            DownloadShoppingList.counter = 0

            print("\nSomething went wrong writing to the file!")
            print("Maybe add something to your shopping list first?")
            print(f"\nERROR LOG: {err}")
            time.sleep(2)

    def getDict(self) -> Dict:
        """ Returns the current dictionary of the items and cost.

        Args:
            None

        Returns:
            savedItems (Dict): The dictionary of the current items in the list. Contains the item, and cost.

        """
        return self.savedItems

    def getFileName(self) -> str:
        """ Returns the current file name that the user specified

        Args:
            None

        Returns:
            fileName (str): The file name specified.

        """
        return self.fileName

# ------------------------------------------------------------------ #

class RemoveEntries(DownloadShoppingList):
    """ A class for removing entries from the item/price/count lists, in order to provide 
        flexibility with being able to edit the list.

    Attributes:
      subtotal (float): The subtotal for the current products in the list.
      totalCost (float): The total cost for the current products in the list.

    Methods:

      __init__(self, subtotal, totalCost): 
          Constructs the attributes: subtotal, totalCost, which inherits from the 
          DownloadShoppingList class. 

      removeIndex(self): 
          Asks the user for what item they would like to remove, correspondent to their 
          position on the list. Checks for this positon, and deletes the corresponding 
          values for that item, i.e. Pricing, count.

    """
    iterCount = 0 # Keep track of the position of the indices
    choiceBoolean = True

    def __init__(self, subtotal, totalCost) -> None:
        """ Constructor for the subtotal and totalCost, which are inherited from the 
            DownloadShoppingList class. 

        Args:
          None

        Returns:
          None

        """
        try:
            super().__init__(subtotal, totalCost, fileName)

            self.userChoice = input("\nAre you sure you want to remove items? (Y/N): ")

            if self.userChoice.lower() == "y":
              RemoveEntries.choiceBoolean = True
              print("Continuing...") 

            if self.userChoice.lower() == "n":
              RemoveEntries.choiceBoolean = False
              print("Returning to Menu...")
              time.sleep(1)

        except Exception as err:
            print("Something went wrong!")
            print(f'ERROR LOG: {err}')

    def removeIndex(self) -> bool:
        """ Instance method for removing certain entries from the list. 
            Looks for an index in range (as specified by the user) and deletes it,
            along with its corresponding values.

        Args:
          None

        Returns:
          bool: Returns False if the process is over, and returns the user to the list menu.

        """
        while True:
            try:

                # Check if the list is empty
                # If so, deny the user from removing anything
                if not CreateShoppingList.itemList:
                    print("\nThere's nothing in your shopping list!")
                    print("Maybe add something first?")
                    time.sleep(1)
                    return False

                print("\nWhich item do you want to remove?")

                # Getting the names and indexes of the items
                for itemKeys in DownloadShoppingList.getDict(self):
                    items = (f"[{RemoveEntries.iterCount}]: {str(itemKeys).upper()}")
                    RemoveEntries.iterCount += 1
                    print(items)
    
                print(f"[{RemoveEntries.iterCount}]: All Items")
                indexToRemove = int(input("\nEnter the item: "))
              
                # Check if index exists within the list, then delete the item and its corresponding count/price
                if (indexToRemove >= 0) and (indexToRemove < len(CreateShoppingList.itemList)):
                    del CreateShoppingList.itemList[indexToRemove]
                    del CreateShoppingList.countOfItem[indexToRemove]
                    del CreateShoppingList.individualItemPrice[indexToRemove]
                    RemoveEntries.iterCount = 0 # Reset the iteration count, so that we can have ordered numbers each time

                    print("Item removed successfully.")
                    return False
                
                elif (indexToRemove == RemoveEntries.iterCount):
                    (CreateShoppingList.itemList).clear()
                    (CreateShoppingList.countOfItem).clear()
                    (CreateShoppingList.individualItemPrice).clear()
                    RemoveEntries.iterCount = 0
                    
                    print("Item(s) removed successfully.")
                    return False

                # Case when index does not exist, and user selects an invalid number.
                else:
                    RemoveEntries.iterCount = 0
                    print("\nThe item does not exist!")
                    print("Are you sure you put the right number in?")
                    continue

            except Exception as err: 
                RemoveEntries.iterCount = 0
                print("Something went wrong removing your item!")
                print(f"{err}")

# ------------------------------------------------------------------ #
def startingMenu() -> bool:
    """ The menu when the user first enters the program, only contains the 
        options to exit or enter.

    Args:
      None

    Returns:
      bool: Returns False if the process is over and exits the program
            Returns True if an exception has occurred, and continues with asking the user.

    """
    try:
        selections = {
            "1": ("Enter", selectionMenu),
            "2": ("Exit Program", main)
        }

        prompt = "Select an Option: "
        userSelect = input(f"{prompt.rjust(95//2)}").strip()

        # Check if the user's selection is in the dictionary, and correlates
        # to the key needed to exit the program.
        if (userSelect in selections) and (userSelect == "2"):
            print("\nThanks For Using the Shopping List Creator!")
            return False

        selections[userSelect][1]()

    except Exception:
        print("An exception occurred! Try again, and enter one of the options above! \n")
        startingMenu()
        return True

def selectionMenu() -> bool:
    """ The subsequent menu, after selecting to enter. Gives the user a variety of choices
        i.e. Adding/Removing Entries, Downloading Lists, and Exiting

    Args:
        selectionInput (str): Correspondent to the option the user wishes to select. 

    Returns:
        bool: Returns False if the user wants to stop running this function. 

    """
    while running:
        try:

            print("\nShopping List Menu")
            selections = ({
                "1": ("Create/Add Entries", None),
                "2": ("Remove Entries", None),
                "3": ("View/Download your Shopping List", None),
                "4": ("Instructions", None),
                "5": ("Exit", main)
            })

            # For all key/value pairs in the selections dict, print the options
            for k, v in selections.items():
                options = (f"{str(k)} > {str(v[0])}")
                print(f"{options}")

            selectionInput = input("\nEnter Selection: ").strip()

            # Creating a shopping list
            if (selectionInput == "1"):
                shoppingList = CreateShoppingList(subtotal, totalCost) # Initialize CreateShoppingList
                shoppingList.createLists()

            # Removing entries from the shopping list
            elif (selectionInput == "2"):
                removeEntry = RemoveEntries(subtotal, totalCost) # Initialize RemoveEntries

                if removeEntry.choiceBoolean:
                  removeEntry.removeIndex()

            # Downloading/viewing the shopping list
            elif (selectionInput == "3"):
                downloadList = DownloadShoppingList(subtotal, totalCost, fileName) # Initialize DownloadShoppingList
                downloadList.downloadChoice()

                # Check if the user wants to download
                if downloadList.choiceBoolean:
                    downloadList.createFile() 

            # Fetches the instructions for the program
            elif (selectionInput == "4"):
                print(instructions.__doc__) # Get documentation from instructions.py
                time.sleep(2)

            # Returns to the main menu
            elif (selectionInput == "5"):
                main()
                return False

            # Invalid selection
            else:
                print("Enter a Valid Option.")
                continue   

        except ValueError:
            print("Please enter valid values!\n")
            continue

def main() -> None:
    """ The main function of the program, simply just prints the banner for the program 
        and heads to the starting menu. It will also check if it should 
        continue running, depending on the options or values that are returned towards 'running'.

    Args:
        None

    Returns:
        None

    """

    menuBanner = """
           _____ __                      _                __    _      __     
          / ___// /_  ____  ____  ____  (_)___  ____ _   / /   (_)____/ /_    
          \__ \/ __ \/ __ \/ __ \/ __ \/ / __ \/ __ `/  / /   / / ___/ __/    
         ___/ / / / / /_/ / /_/ / /_/ / / / / / /_/ /  / /___/ (__  ) /_      
        /____/_/ /_/\____/ .___/ .___/_/_/ /_/\__, /  /_____/_/____/\__/      
                        /_/   /_/            /____/                           
                     ______                __                                 
                    / ____/_______  ____ _/ /_____  _____                     
                   / /   / ___/ _ \/ __ `/ __/ __ \/ ___/                     
                  / /___/ /  /  __/ /_/ / /_/ /_/ / /                         
                  \____/_/   \___/\__,_/\__/\____/_/  


                  ======================================
                  [V1.0] Latest




                             >> Main Menu <<


                           [1] > Enter Program          
                           [2] > Exit Program




                  Joshua Tuibuen
                  ICS4U1 ISP Project
                  ======================================
    """

    print(menuBanner)
    startingMenu()

if __name__ == "__main__":
    main()

"""
TEST CASES

* NOTE THAT FOR INPUTS LIKE (1,2,3 ...) THEY ARE SEPARATE INPUTS,
  AND ARE NOT MADE ON A SINGLE LINE.

CASE A (ENTRY ADDITIONS, LIST CHECKING):

    [-- Starting from selectionMenu() --]

    Enter Selection: 1
    Enter Your Item:         (Eggs, Milk, Carrots, Bread, Cereal)
    Enter Your Price (CAD$): (3.87, 1.86, 0.57,    3.59,  4.97)
    How Many:                (1,    2,    3,       4,     5

    Enter Your Item: "exit"
    Enter Selection: 3

    CURRENT LIST:

        ITEMS:  ['eggs', 'milk', 'carrots', 'bread', 'cereal']
        ITEM COUNT:  [1, 2, 3, 4, 5]
        INDIVIDUAL COST (NO TAX):  [3.87, 3.72, 1.71, 14.36, 24.85]
        SUBTOTAL: $48.51
        TOTAL COST: $54.82

    [-- CASE A END --]

CASE B (INVALID VALUE CHECKS):

    [-- Starting from CreateShoppingList.__init__ --]

    Enter Your Item: Pickles
    Enter Your Price (CAD$): -2
    Try Again ($0.00 or More!): (-2, 1)
    How Many: -2
    Try Again (1 Item or More!): (-2, 1)

    "Item Successfully Added."

    [-- CASE B End --]

CASE C (EMPTY LIST CHECKS):

    [-- Starting from selectionMenu() --]

    Enter Selection: 2

    CURRENT LIST:

        ITEMS:  []
        ITEM COUNT:  []
        INDIVIDUAL COST (NO TAX):  []
        SUBTOTAL: $0.0
        TOTAL COST: $0.0

    "There's nothing in your shopping list!"
    "Maybe add something first?"

    [-- CASE C End --]

CASE D (DUPLICATES):

    [-- Starting from CreateShoppingList.__init__ --]

    Enter Your Item: (Bread, Bread, Eggs, Eggs, Bread, Juice, Juice)
    Enter Your Price (CAD$): (2, 2, 4, 2, 5, 4, 2)
    How Many: (3, 3, 5, 3, 6, 3, 1)

    Enter Your Item: "exit"
    Enter Selection: 3

    CURRENT LIST:

        ITEMS:  ['bread', 'eggs', 'juice']
        ITEM COUNT:  [12, 8, 4]
        INDIVIDUAL COST (NO TAX):  [42.0, 26.0, 14.0]
        SUBTOTAL: $82.0
        TOTAL COST: $92.66

    [-- CASE D End --]

CASE E (DOWNLOADING FILE):

    [-- Starting from DownloadShoppingList.createFile() --]

    CURRENT LIST:

        ITEMS:  ['apple']
        ITEM COUNT:  [1]
        INDIVIDUAL COST (NO TAX):  [1.0]
        SUBTOTAL: $1.0
        TOTAL COST: $1.13

    Are you sure you want to download? (Y/N): y
    "Continuing..." 

    Enter a File Name: apple_tst

    "Clearing file data before handling..."
    "Writing data..."
    "Write to file successful."
    "Check around this program's folder for the text data!"

    [-- CASE E End --]

CASE F (DOWNLOADING FILE W/ EMPTY LISTS)

    [-- Starting from DownloadShoppingList.createFile() --]

    CURRENT LIST:

        ITEMS:  []
        ITEM COUNT:  []
        INDIVIDUAL COST (NO TAX):  []
        SUBTOTAL: $0.0
        TOTAL COST: $0.0

    Are you sure you want to download? (Y/N): y
    "Continuing..." 

    Enter a File Name: empty_tst

    "Clearing file data before handling..."

    "Something went wrong writing to the file!"
    "Maybe add something to your shopping list first?"

    "ERROR LOG: max() arg is an empty sequence" 

    [-- CASE E End --]

"""
