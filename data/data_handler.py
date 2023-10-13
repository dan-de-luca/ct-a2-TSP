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


def handle_csv_file(file_path, num_cities):
    """
    Reads the data file (csv) and returns a list of the cities
    :param file_path: path to the data file
    :return: list of cities
    """
    cities = []
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(cities) < num_cities: cities.append(City(int(row[0]), float(row[1]), float(row[2])))
            else: break
    
    return cities
