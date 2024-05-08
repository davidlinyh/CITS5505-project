# CITS5505-project


## Description
This project is a basic Flask application.

## Prerequisites
Before you begin, ensure you have met the following requirements:
- You have a `Windows/Linux/Mac` machine.
- You have installed Python 3.6 or higher.

## Installing Our Flask App
To install Our Flask App, follow these steps:

## Clone the Repository
`git clone https://github.com/davidlinyh/CITS5505-project`

## Navigate to Project Directory
`cd CITS5505-project/agileapp`



# Create and activate a virtual environment:
This step is optional but recommended. To create a virtual environment, run the following command:
```
python3 -m venv venv
```

To activate the virtual environment, run one of the following commands depending on your operating system:
```
source venv/bin/activate    # Linux or macOS
venv/Scripts/activate       # Windows
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

# Run the application:
To run the application, use the command
```
flask run
```

The application will be running on http://localhost:5000/ by default.
