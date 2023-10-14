import csv
# import os.path


class City:
    """
    City class
    """
    def __init__(self, id, x, y):
        """
        Constructor
        :param id: id of the city
        :param x: x coordinate of the city (latitude)
        :param y: y coordinate of the city (longitude)
        """
        self.id = id
        self.x = x
        self.y = y

    def __str__(self):
        """
        String representation of the city
        :return: string representation of the city
        """
        return "City: " + str(self.id) + ", x: " + str(self.x) + ", y: " + str(self.y)
    
    # Getters
    def get_id(self):
        return self.id
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y


def get_delimiter(file_path):
    with open(file_path, "r") as file:
        # Read the first line
        first_line = file.readline()
        
        # Check for possible delimiters (comma, space, tab, semicolon)
        delimiters = [",", " ", "\t", ";"]
        for delimiter in delimiters:
            if delimiter in first_line: return delimiter
        
        # If no delimiter found, raise an error (invalid file format)
        raise Exception("Common delimiter not found. Invalid file format.")


def handle_csv_file(file_path, num_cities):
    """
    Reads the data file (csv) and returns a list of the cities
    :param file_path: path to the data file
    :return: list of cities
    
    Data sourced from: https://www.math.uwaterloo.ca/tsp/world/countries.html
    """
    cities = []
    
    # Get the delimiter
    delimiter = get_delimiter(file_path)
    
    # Read the CSV file using the correct delimiter
    with open(file_path, "r") as file:
        reader = csv.reader(file, delimiter=delimiter)
        for row in reader:
            # Only read the first num_cities cities
            if len(cities) < num_cities: cities.append(City(int(row[0]), float(row[1]), float(row[2])))
            else: break
    
    return cities
