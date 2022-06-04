# Import libraries
import os # <== read files and directories
import datetime # <== Get date and times

# Initiate global variable CURRENT_USER
CURRENT_USER = '';

# -----------------------------------
# checkDecimal(<decimal>) --> Checks if a string has only numerical or decimal points
def checkDecimal(decimal):
  return str(decimal).replace('.', '0').isdecimal(); # Replace each decimal with a 0 so isdecimal can return true or false
  
# -----------------------------------
# checkInput(<input>, <validInputs>) --> Checks to see if an input matches an item in validInputs
# <input> - what is being checked
# <validInput> - a list of what input must be for this function to return true
# --> Returns true or false, depending on whether input is a value in validInputs
def checkInput(input, validInputs):
  for validInput in validInputs: # Loop through all valid inputs
    if input == validInput: # If one value in validInputs is the user input
      return True; # Return true
  return False; # Return false

# -----------------------------------
# getFileName(<username>) --> Takes in the username and returns the path and file type
def getFileName(username):
  return 'accounts/' + username + '.txt' # Add the folder and the .txt at the end of the username

# -----------------------------------
# formatMoney(<money) --> Takes in a money amount, as a number, and returns it as a string, with the $ at the front and cents having exactly two decimal places
def formatMoney(money):
  dollars, cents = str(round(money, 2)).split('.'); # Split dollars and cents
  while len(cents) < 2: # If cents have less than 2 characters, add a 0 at the end until there is two characters
    cents += '0'
  while len(cents) > 2: # If cents have over two charaters (due to the program having precision errors when adding), remove decimal places until there are two
    cents.rstrip(cents[:-1])
  return '$%s.%s' % (dollars, cents) # Return dollars and cents with a $ at the front

# -----------------------------------
# getAccounts() --> Looks through each account and returns each account's username and password
def getAccounts():
  accountsList = os.listdir("accounts"); # Get the account files path
  accountsDict = {}; # Create a dictionary
  for account in accountsList: # For each file:
    file = open('accounts/' + account, 'r'); # Open the file
    username, password = file.readlines(1)[0].strip().split('§§') # Look through the first line and split the string into the username and password
    accountsDict[username] = password; # Add to the dictionary (username is the key, password is the value)
  return accountsDict; # Return the dictionary

# -----------------------------------
# doesUserExist(<username>) --> Checks if a user exists
def doesUserExist(username):
  usernames = getAccounts().keys(); # Get all the usernames (the returned dictionary's keys are all usernames)
  for user in usernames: # For each user
    if username == user: # If that user's username matches the username passed into this method
      return True; # Return True
  return False; # If all the usernames have been looped through and none of them matches the passed in username, return False

# -----------------------------------
# doTransaction(<username>, <action>, <moneyChange>) --> Add or remove money from an account
# <username> --> THe username of the account that the transaction is modifying
# <action> --> A string that will be added to the account's text file, showing what the user did
# <moneyChange> --> The transaction that will determine how much money is added or removed
def doTransaction(username, action, moneyChange):
  currDatetime = datetime.datetime.now().strftime("%B %d, %Y (%H:%M:%S)"); # Use the datetime library to get the current date and time
  file = open(getFileName(username), 'r') # Open the file, use getFileName(username) to get the file name, set it to read mode
  lines = len(file.readlines()) # Get the number of lines the file has
  file.close(); # Close the file
  file = open(getFileName(username), 'a') # open the same file, this time, put it on append mode
  file.write('\n%s§§%s§§%s§§%s' % (lines, currDatetime, action, moneyChange)); # Add a new line, put lines, current date and time, action and change in money in that order, each separated by two section symbols
  file.close(); # Close the file

# -----------------------------------
# getBalanceFrom(<username>) --> Gets the total balance a user has in their account
def getBalanceFrom(username):
  file = open(getFileName(username), 'r') # Open the file, use getFileName and pass in the username, set it to read mode
  lines = file.readlines(); # Put each line in a list
  totalBalance = 0; # Create a new variable, totalBalance, set to it 0
  for i in range(1, len(lines)): # Loop through each line EXCEPT the first
    line = lines[i]; # set a new variable, line, to the string in the specified index of the lines list
    transactionNumber, transDatetime, action, moneyChange = line.split('§§'); # Split each element
    totalBalance += float(moneyChange) # Cast moneyChange to a float and add it to totalBalance
  return totalBalance; # Return totalBalance

# -----------------------------------
# createAccount() --> Creates a new account
def createAccount():
  print("================================")
  username = input("Please enter a USERNAME for your account: "); # Prompt user for a username
  while doesUserExist(username) or len(username) == 0: # If an account with the same username already exists or if the user inputted nothing:
    if (doesUserExist(username)): # Display a different error depending on what the user did, prompt them to enter a new username each time
      username = input("Sorry, this username is already taken. Please enter a USERNAME for your account: ")
    elif len(username) == 0:
      username = input("Please enter a USERNAME: ")
  password = input("Please enter a PASSWORD for your account (be careful with the spelling, you cannot change it later): "); # Prompt user for a password
  newFile = open(getFileName(username), "w"); # Create a new file, with the username as the file name
  newFile.write(username + '§§' + password); # On the first line, put the username and password, separated with two section symbols
  newFile.close(); # Close the file
  doTransaction(username, 'account creation', 100) # Put $100 into the account

# -----------------------------------
# login() --> Logs into an account
def login():
  print("================================")
  username = input("Please enter your username: ") # Prompt for a username
  while not doesUserExist(username): # If the user does not exist
    username = input("Sorry, this user does not exist, please enter another username: ") # Prompt user for an existing username
  password = input("Please enter your password: ") # Prompt user for password
  if password == getAccounts()[username]: # If the set password and the inputted password matches
    global CURRENT_USER; # Get the global variable CURRENT_USER
    CURRENT_USER = username; # Set CURRENT_USER to the inputted username
  else: # If the password is incorrect
    print("Incorrect password. You have been sent back to the main menu.") # Send user back to main menu, tell them that too

# -----------------------------------
# logout() --> Logs out of account
def logout():
  global CURRENT_USER; # Get the global variable CURRENT_USER
  CURRENT_USER = '' # Set it to blank, meaning no account is logged in

# -----------------------------------
# depositMoney() --> Function that allows user to put money into their account
def depositMoney():
  money = input("Please enter the money you want to deposit (greater than 0): "); # Ask user for money they want to put into account
  while not checkDecimal(money) or float(money) <= 0: # If the input is not a number or is less than or equal to 0
    money = input("invalid input. Please enter the money you want to deposit (greater than 0): "); # Prompt user for another input
  money = round(float(money), 2); # Round the number to 2 decimal places
  global CURRENT_USER; # Get the global variable CURRENT_USER
  doTransaction(CURRENT_USER, 'deposit', str(money)) # Do a transaction, passing in CURRENT_USER as the username, 'deposit' as the action, and the money casted as a string
  print("You just added " + formatMoney(money) + " dollars into your bank account.") # Print this to the console

# -----------------------------------
# withdrawalMoney() --> Function that allows user to take out money from their account
def withdrawalMoney():
  money = input("Please enter the money you want to withdrawal (greater than 0): "); # Ask user for money amount
  global CURRENT_USER; # Get the global variable CURRENT_USER
  while not checkDecimal(money) or (float(money) <= 0 or float(money) > getBalanceFrom(CURRENT_USER)): # If the money is not a number, less than or equal to 0 or is greater than the total balance the user already has
    money = input("invalid input. Please enter the money you want to deposit (greater than 0): "); # Prompt user for another input
  money = -(round(float(money), 2)); # Round to 2 decimal places and switch to negative number
  doTransaction(CURRENT_USER, 'withdrawal', str(money)) # Do a transaction, passing in CURRENT_USER as username, 'withdrawal' as action and money casted as a string
  print("You just removed " + formatMoney(-money) + " dollars into your bank account.")

# -----------------------------------
# printHistory() --> Prints the account information and everything that has happened with this account
def printHistory():
  global CURRENT_USER; # Get the global variable CURRENT_USER
  balance = getBalanceFrom(CURRENT_USER); # Get the user's current balance
  file = open(getFileName(CURRENT_USER), 'r'); # open the user's account file
  lines = file.readlines(); # Read each line
  acccountInfo = lines[0]; # Get the username and password
  
  username, password = acccountInfo.split('§§'); # Split into the username and password
  censoredPassword = ''; # Create a new string, which will be the password censored into star symbols
  for char in password.strip(): # Strip the \n from the password string and loop through each character
    censoredPassword += '*'; # Add a * to censoredPssword for each character in password
  print("================================")
  print('Account info:\nUsername: %s\nPassword: %s\nTotal Balance: %s\n' % (username, censoredPassword, formatMoney(float(balance)))); # Print account info
  lines.pop(0); # Remove the first line from the list

  for line in lines: # For the rest of the lines:
    transactionNumber, currDatetime, action, moneyChange = line.split('§§') # Split the line to get each piece of info
    floatMoneyChange = float(moneyChange); # Get the money change in the line
    direction = '+'; # Create a new variable, which will be used for displaying a nicer string to the user
    if floatMoneyChange < 0: # If this action removed money from the account
      direction = '-'; # Change the sign
    print('{#%s} %s: %s from %s' % (transactionNumber, currDatetime, direction + formatMoney(abs(floatMoneyChange)).strip(), action)); # Print the string

# -----------------------------------
# transferMoney() --> Gives money to another user
def transferMoney():
  global CURRENT_USER; # Get the global variable CURRENT_USER
  transferToUser = input("Please input the user you would like to transfer money to: "); # Ask user for a user to transfer money to
  while not doesUserExist(transferToUser) or transferToUser == CURRENT_USER: # If the user does not exist or they try transferring money to themselves
    if not doesUserExist(transferToUser): # Display a different error message depending on what they do
      transferToUser = input("Sorry, this user does not exist. Please input the user you would like to transfer money to: ")
    elif transferToUser == CURRENT_USER:
      transferToUser = input("Please choose a user other than yourself. ")
  moneyTransfer = input('How much money would you like to transfer? ') # Ask user for the amount of money they want to transfer
  while not checkDecimal(moneyTransfer) or (float(moneyTransfer) <= 0 or float(moneyTransfer) > getBalanceFrom(CURRENT_USER)): # if this isn't a number, the number is less than 0, or the number is greater than what the user has
    moneyTransfer = input('Invalid input. How much money would you like to transfer? ') # Prompt the user for a valid input
  moneyTransfer = round(float(moneyTransfer), 2) # Round the money number to two decimal places
  doTransaction(CURRENT_USER, 'donation', str(-moneyTransfer)); # Remove the money from this account
  doTransaction(transferToUser, 'gift', str(moneyTransfer)); # Add the money to the other account
  print("You just gave %s to %s" % (formatMoney(moneyTransfer), transferToUser)) # Print what the user just did to the console

# -----------------------------------
# getAction() --> Get the user action
def getAction():
  accounts = len(getAccounts()); # Get the number of existing accounts
  validInputs = set() # Create a set called valid inputs
  if CURRENT_USER == '': # If no one is signed in
    if accounts > 0: # If there is one or more existing account
      validInputs.add('2'); # Add 2 to the set
    validInputs.add('1'); # Add 1 to the set
  else: # If someone is signed in
    validInputs.add('0') # Add 0, 1 and 2 to the set
    validInputs.add('1')
    validInputs.add('2')
    if getBalanceFrom(CURRENT_USER) > 0: # If the user has money in their account
      validInputs.add('3') # Add 3 to the set
      if accounts > 1: # If more than one account exists
        validInputs.add('4'); # Add 4 to the set
  validInputs.add('5') # Add 5 to the set
  print("================================\nMENU:")
  if CURRENT_USER == '': # If no one is signed in
    print('[1] ==> Create account') # Give option to create an account
    if '2' in validInputs: # If 2 is in the set
      print('[2] ==> Log in') # Give option to log in
  else: # If someone is signed in
    print("Your current balance is: %s\n" % (formatMoney(float(getBalanceFrom(CURRENT_USER))))) # Display current balance
    print('[1] ==> Log out') # Give option to log out
    print('[2] ==> Make a deposit') # Give option to make a deposit
    if getBalanceFrom(CURRENT_USER) > 0: # If the user has money in their account
      print('[3] ==> Make a withdrawal') # Give option to make a withdrawal
      if '4' in validInputs: # If there is a 4 in the set
        print('[4] ==> Transfer money') # Give option to transfer money
    print('[0] ==> Print account history') # Give option to print user's account history
  print('[5] ==> Quit program')

  userInput = input("What would you like to do? ") # Ask user what they want to do
  while not checkInput(userInput, validInputs): # Check if the input matches an item in the set
    userInput = input("Invalid input. What would you like to do? ") # If not, ask user for another input
  return userInput; # Return the user input

# -----------------------------------
# run() --> Runs an action based on what the user inputs
def run():
  action = getAction(); # Get action from user 
  if CURRENT_USER == '': # If no one is signed in
    if action == '1': # If user input is 1
      createAccount(); # Create an account
    elif action == '2': # If user input is 2
      login(); # Login
  else: # Is an account is logged in
    if action == '1': # If user input is 1
      logout(); # Logout
    elif action == '2': # If user input is 2
      depositMoney(); # Deposit money into account
    elif action == '3': # If user input is 3
      withdrawalMoney(); # Withdrawal money from account
    elif action == '4': # If user input is 4
      transferMoney(); # Transfer money to another account
    elif action == '0': # If user input is 0
      printHistory(); # Print the account's history
  if action == '5': # If user input is 5
    print("================================\nThank you for using my banking program!") # Print a goodbye nmessage
  else: # If user input is not 5
    run(); # Run again

print('''Welcome to my online bank! This program will let you add or remove money from different accounts while also giving money to others. All data will be saved when you run the program multiple times.

To use this program, type a number when prompted based on the action you want to perform. When logged out, you can create an account or log in, if an account already exists. Remember your password, because you cannot change it once you create your account! When you create an account, you will be given $100 automatically. When you log in, you will be asked for your username and password, which you will have to enter both.

Once you are logged in, you can manage your bank by depositing or withdrawaling money and give money to others. You are able to see your account history whenever you want. YOu can also log out and sign into other accounts.

In any main menu, you can shut down the program. This will automatically log you out of your account, if one is logged in.
''') # Print introduction
input("Press ENTER to begin!") # Allow user to read instructions and begin program whenever they want
run(); # Run program for the first time