import csv
import sys
import logging
from collections import defaultdict
from datetime import datetime

# Constants
BASE_FEE = 2.00
DAILY_CAP = 15.00
MONTHLY_CAP = 100.00
ERRONEOUS_FEE = 5.00

# To test if the files are in the correct folders
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Additional cost for the different zones 
def get_additional_cost(zone):
     
     # Error message when zone is not greater or equal to 1
    if zone < 1:
        raise ValueError("\n Zone must be greater than or equal to 1.")

    if zone == 1:
        return 0.80
    elif 2 <= zone <= 3:
        return 0.50
    elif 4 <= zone <= 5:
        return 0.30
    else:
        return 0.10

def read_zone_map(filename):
    logger.info('Reading zone map from: %s', filename)
    # Read zone map file
    zone_map = {}
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            station = row['station']
            try:
                zone = int(row['zone'])
                zone_map[station] = zone
                #logger.info(f"Loaded station: {station}, Zone: {zone}")
            except ValueError:
                # Error message when zone is can not be a letter or invalid
                raise ValueError(f"\n Zone must be a positive integer; can't be a letter or invalid value: '{row['zone']}' for station '{station}'")
    return zone_map



def process_transit_data(journey_file, zone_file):
    # Processes the transit data and calculates the total charges 
    logger.info('Processing journeys from: %s', journey_file)
    logger.info('Using zone file: %s', zone_file)
    zone_map = read_zone_map(zone_file)
    user_journeys = defaultdict(list)
    user_charges = defaultdict(float)
    daily_charges = defaultdict(lambda: defaultdict(float))

    with open(journey_file, mode='r') as file:
        reader = csv.DictReader(file)
        for record in reader:
            user_id = record['user_id']
            direction = record['direction']
            station = record['station']
            journey_time = record['time'].strip()

            # Debugging timestamp
            # print(f"Raw timestamp: '{journey_time}'")

            try:
                journey_date = datetime.strptime(journey_time, '%Y-%m-%dT%H:%M:%S').date()
            except ValueError as e:
                # Print error message if timestamp parsing fails
                # print(f"Error parsing timestamp: {e}")
                continue
            # The IN and OUT of the user's journey
            if direction == 'IN':
                # Store the entry station for the user
                user_journeys[user_id].append((station, journey_date))
            elif direction == 'OUT':
                if user_journeys[user_id]:
                    start_station, entry_date = user_journeys[user_id].pop()
                    start_zone = zone_map.get(start_station, None)
                    end_zone = zone_map.get(station, None)
                    # These messages are used for debugging if the info iis being read
                    # print(f"Processing OUT for User: {user_id}, Station: {station}, Time: {journey_time}")
                    # print(f"Start Zone: {start_zone}, End Zone: {end_zone}")

                    if start_zone is not None and end_zone is not None:
                        # Calculate the journey cost based on the base fee and additional costs for both start and end zones
                        journey_cost = BASE_FEE + get_additional_cost(start_zone) + get_additional_cost(end_zone)
                      
                        #Use for debugging for user and journey cost
                        #print(f"User: {user_id}, Journey Cost: {journey_cost:.2f}")
                       
                        daily_charges[user_id][entry_date] += journey_cost
                    else:
                        # Charge erroneous fee if zone is missing
                        daily_charges[user_id][entry_date] += ERRONEOUS_FEE

     # Uncompleted journeys, missing OUT journey and apply fee
    for user_id in user_journeys:
        if user_journeys[user_id]:
            entry_station, entry_date = user_journeys[user_id][0]
           # To check if the missing out journey for the user is being charged the fee
           # print(f"Missing OUT journey for User: {user_id}, charging erroneous fee.")
            daily_charges[user_id][entry_date] += ERRONEOUS_FEE

    # Apply daily caps and calculate final user charges
    for user_id, days in daily_charges.items():
        for day, total in days.items():
            capped_total = min(total, DAILY_CAP)
            user_charges[user_id] += capped_total

    return user_charges


def write_output(output_file, charges):
    
    # Writes the final charges to an output CSV file
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['user_id', 'billing_amount']) 
        for user_id in sorted(charges.keys()):
            writer.writerow([user_id, f"{charges[user_id]:.2f}"])

# Check if the correct number of command-line arguments are given
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python my_solution.py <zones_file_path> <journey_data_path> <output_file_path>")
        sys.exit(1)
    
    # Assign command-line arguments to variables for clarity
    zone_file = sys.argv[1]
    journey_file = sys.argv[2]
    output_file = sys.argv[3]

    charges = process_transit_data(journey_file, zone_file)
    write_output(output_file, charges)
    # Inform the user that the billing amounts have been successfully written to the output file
    print(f"Billing amounts have been written to {output_file}")
