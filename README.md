Overview
This project implements a mass transit billing system that calculates journey costs based on user travel data and zone-based pricing. The solution reads input from CSV files, processes the journey information, calculates charges, and applies daily fare caps. Erroneous fees are charged for incomplete or missing journeys.

The system is designed to handle multiple users and journeys, storing the billing information for each user and outputting the total charges in a CSV file.

Key features:

Zone-based pricing model
Daily fare caps to prevent overcharging
Handling of incomplete journeys with erroneous fees
Support for bulk processing of transit data using command-line tools
This Python-based project can be run in a virtual environment for isolation and dependency management.

Technologies & Libraries Used

Python 3.x: The primary programming language used to implement the billing system logic.
csv: Built-in Python library for reading and writing CSV files, used for handling zone and journey data.
datetime: Python's library for working with date and time, used to parse and process journey timestamps.
collections.defaultdict: For creating dictionaries with default values, simplifying data storage for users and daily charges.
Virtual Environment (venv): Used to create an isolated environment for the project, ensuring consistent dependency management.
Logging: For tracking the application's internal processes and debugging.
 


Features

Zone-based Billing System: Calculates journey costs based on station zones, with additional pricing for specific zones.
Daily Charge Capping: Ensures that users are not overcharged by applying daily caps to their total journey costs.
Erroneous Fee Handling: Applies a penalty charge for incomplete or invalid journeys, such as missing entry or exit points.
CSV Data Parsing: Reads station zone information and user journey records from CSV files to process billing.
Customizable Zone Map: Allows for easy updates to the zone map via CSV files to reflect changes in the transit system.
Command Line Interface (CLI): Users can run the billing system via the command line by specifying input and output files.
Debugging Support: Includes optional logging and print statements to track journey processing and billing calculations during development.




Steps to Run the Project

To run the mass transit billing system, follow these steps:

1. Install Python
Download and install Python 3.x. from website (https://www.python.org/downloads/)

For Terminal

macOS: 

brew install python

Linux:

Ubuntu/Debian
sudo apt install python3

Fedora
sudo dnf install python3

CentOS/RHEL
sudo yum install python3


2. Install Virtual Environment
After Python is installed, open your terminal and create a virtual environment.
virtualenv is another tool for creating virtual environments.

bash

python3 -m venv myenv

If you are using a non-macOS system and prefer to use virtualenv, you can install 

bash

pip install virtualenv



3. Navigate to the project directory
Use this command to make sure you are in the correct project directory.

bash

cd mass_transit_billing\ \(2\)

4. Activate the Python virtual environment
Create and activate a Python virtual environment.

bash

 
source myenv/bin/activate


5. Install Dependencies
Install the dependencies for this project.

bash

pip install -r requirements.txt


If you do not have a requirements.txt file, 
you can create one by running 'pip freeze > requirements.txt'
in your virtual environment after installing any packages you need for your project.


6. Run the Python Solution

After following these steps. The project can be runned. 

bash

python app/my_solution.py data/zone_map.csv data/journey_data.csv output/output.csv

File layout:
--data/zone_map.csv: Contains station-to-zone mappings
--data/journey_data.csv: Contains user journey data
--output/output.csv: The file where the billing information will be saved

6. View the Output

After running the command, the billing information will be written to the specified output CSV file. You will see a message confirming this.

Billing amounts have been written to output/output.csv


Explanation of File Structure
The project has a clean structure that separates the application logic and data files. The main components are organized as follows:

-app/: Contains the main Python script for processing transit data.

-data/: Contains input data files for zone mappings and journey records.

-output/: Contains the output CSV file with calculated billing amounts.

This structure promotes better organization and ease of maintenance, allowing for efficient development and testing.