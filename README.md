# CITS5505-project


## Team Member
| Student ID | Name         | GitHub Username |
|------------|--------------|-----------------|
| 23796349  | Adharsh Sundaram Soudakar     | adarsh136         |
| 23853569  | Ammad Rahman   | AmmadR       |
| 22570361  | David Yonghui Lin | davidlinyh     |
| 23894575  | Ida Bagus Prawira Janottama KN | gusprauwa     |

## Description
This project is a basic Flask application. An application to facilitate UWA Guild for Lost and Found items in University. 
A user have to register an account before viewing the gallery of Lost items, claim their item, and upload their prove of ownership of their item.
A member of UWA Guild Student can act as an Administrator, to post a lost item to the gallery, and also approve or deny the claim.

## Prerequisites
Before you begin, ensure you have met the following requirements:
- You have a `Windows/Linux/Mac` machine.
- You have installed Python 3.6 or higher.
- Run the terminal as Administrator

## Installing Our Flask App
To install Our Flask App, follow these steps:

## Clone the Repository
`git clone https://github.com/davidlinyh/CITS5505-project`
or
Download the zip source.

## Navigate to Project Directory
`cd CITS5505-project/agileapp`



# Create and activate a virtual environment:
This step is optional but recommended. To create a virtual environment, run the following command:
```
python3 -m venv venv
```
or 
```
python -m venv venv
```
or
```
py -m venv venv
```

To activate the virtual environment, run one of the following commands depending on your operating system:
LINUX or MACOS:
```
source venv/bin/activate     
```
WINDOWS:
```
venv/Scripts/activate       
```
or try this if it doesn't work:
```
venv\Scripts\Activate.ps1      
```

If you are on Windows and unable to activate virtual environment, according to Microsoft Tech Support, it is related to setting Execution Policy. Try the following:
```
Set-ExecutionPolicy Unrestricted -Force
```
To deactivate the virtual environment, run the following command:
```
deactivate
```
Install the required packages:
If you're using a virtual environment, make sure to activate it first. Then, run the following command:
```
pip install -r requirements.txt
```
This command installs all the necessary libraries and tools specified in the requirements.txt file.

# Database:
The database file is in agileapp/app.db
To reset the database file into test case data, do the following:
First, make sure you are on agileapp directory CITS5505-project/agileapp/ 
And then, empty the database:
```
flask db downgrade base
flask db upgrade
```
Then, import the test data with the python code agileapp/app/test_data.py :
```
flask shell
```
After entering the shell, then type:
```
from app import test_data
```

# Run the application:
To run the application, use the command
```
flask run
```
The application will be running on http://localhost:5000/ by default.

Login information:
for user:
email: user2@gmail.com
password: 123

for admin:
email: admin1@gmail.com
password: 123

# Testing:

Please open agileapp\app\tests\test_app.py and make the changes in the NOTE section.

Each function can be considered as a unit.

NOTE:
***************************************************************************************************************************************************************************************
* Please dont change the password of user2@gmail.com, its being used for testing

* Ignore the warning at line number 238 during testing. It is because I have escaped d for checking numbers, but since it is under comments, it displays the Deprecation warning.

* Uncomment a test you want to run and copy-paste it below def teardown_method(): or at line 21. (If you run the whole test, it would take some time to run:( ).

* Please have the app running.

* Please install Chrome as I have used Chrome drivers to test.

* While testing, For the Manage-Account page, Paste your Absolute path to agileapp/app/static/profile_photos at line number (526) or you could have a folder of photos yourself, mine is:
  C:\Users\adhar\Desktop\sem3\cits5505\Group project\1\CITS5505-project\agileapp\app\static\profile_photos

* While testing, for the New item page, Paste your Absolute path to agileapp/app/static/profile_photos/{any photo} at line number (129) or you could use any photo as you wish, mine is:
  C:\Users\adhar\Desktop\sem3\cits5505\Group project\1\CITS5505-project\agileapp\app\static\item_photos\sample_photo.JPG
***************************************************************************************************************************************************************************************

To run the tests, 
* Open the command prompt/prompt/terminal and install pytest, if not already installed (pip install pytest).
* You may have to set your path variables right if it still shows pytest is not a callable command.
* Once pytest is installed successfully if a terminal is open, switch to the directory \agileapp\app\tests\.
* Just type pytest and press ENTER.
* You should see the number of test cases passed (hopefully all).
