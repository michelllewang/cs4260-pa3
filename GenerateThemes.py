import csv
import random


# Function to generate random 0 or 1
def generate_random():
    return random.randint(0, 1)


# Function to add random themes to each location
def add_location_themes(input_file, output_file):
    with open(input_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header
        data = list(csv_reader)

    # Add random numbers after 'Longitude'
    for row in data:
        longitude_index = 2
        row[longitude_index + 1:longitude_index + 1] = [generate_random() for _ in range(3)]

    # Write the modified data to output file
    with open(output_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(
            ['Location Label', 'Latitude', 'Longitude', 'Theme1', 'Theme2', 'Theme3', 'Contributer', 'Notes'])
        csv_writer.writerows(data)


# Function to add random themes to each edge
def add_edge_themes(input_file, output_file):
    with open(input_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header
        data = list(csv_reader)

    # Add random numbers after 'Longitude'
    for row in data:
        distance_index = 3
        row[distance_index + 1:distance_index + 1] = [generate_random() for _ in range(3)]

    # Write the modified data to output file
    with open(output_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(
            ['edgeLabel', 'locationA', 'locationB', 'actualDistance', 'Theme1', 'Theme2', 'Theme3', 'Contributer', 'Notes'])
        csv_writer.writerows(data)


if __name__ == '__main__':
    add_location_themes('Locations.csv', 'LocThemes.csv')
    add_edge_themes('Edges.csv', 'EdgeThemes.csv')
