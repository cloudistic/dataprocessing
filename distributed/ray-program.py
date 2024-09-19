from collections import namedtuple
import csv
import tarfile
import time

import ray

@ray.remote
class GSODActor():

    def __init__(self, year, high_temp):
        self.high_temp = float(high_temp)
        self.high_temp_count = None
        self.rows = []
        self.stations = None
        self.year = year

    def get_row_count(self):
        return len(self.rows)

    def get_high_temp_count(self):
        if self.high_temp_count is None:
            filtered = [l for l in self.rows if float(l.TEMP) >= self.high_temp]
            self.high_temp_count = len(filtered)
        return self.high_temp_count

    def get_station_count(self):
        return len(self.stations)

    def get_stations(self):
        return self.stations

    def get_high_temp_count(self, stations):
        filtered_rows = [l for l in self.rows if float(l.TEMP) >= self.high_temp and l.STATION in stations]
        return len(filtered_rows)

    def load_data(self):
        file_name = self.year + '.tar.gz'
        row = namedtuple('Row', ('STATION', 'DATE', 'LATITUDE', 'LONGITUDE', 'ELEVATION', 'NAME', 'TEMP', 'TEMP_ATTRIBUTES', 'DEWP',
                                 'DEWP_ATTRIBUTES', 'SLP', 'SLP_ATTRIBUTES', 'STP', 'STP_ATTRIBUTES', 'VISIB', 'VISIB_ATTRIBUTES',
                                 'WDSP', 'WDSP_ATTRIBUTES', 'MXSPD', 
                                 'GUST', 'MAX', 'MAX_ATTRIBUTES', 'MIN', 'MIN_ATTRIBUTES', 'PRCP',
                                 'PRCP_ATTRIBUTES', 'SNDP', 'FRSHTT'))

        tar = tarfile.open(file_name, 'r:gz')
        for member in tar.getmembers():
            member_handle = tar.extractfile(member)
            byte_data = member_handle.read()
            decoded_string = byte_data.decode()
            lines = decoded_string.splitlines()
            reader = csv.reader(lines, delimiter=',')

            # Get all the rows in the member. Skip the header.
            _ = next(reader)
            file_rows = [row(*l) for l in reader]
            self.rows += file_rows

        self.stations = {l.STATION for l in self.rows}

# Code assumes you have the 1980.tar.gz and 2020.tar.gz files in your current working directory.
def compare_years(year1, year2, high_temp):

    # if you know that you need fewer than the default number of workers,
    # you can modify the num_cpus parameter
    ray.init(num_cpus=2)

    # Create actor processes
    gsod_y1 = GSODActor.remote(year1, high_temp)
    gsod_y2 = GSODActor.remote(year2, high_temp)

    ray.get([gsod_y1.load_data.remote(), gsod_y2.load_data.remote()])

    y1_stations, y2_stations = ray.get([gsod_y1.get_stations.remote(),
               	                    gsod_y2.get_stations.remote()])

    intersection = set.intersection(y1_stations, y2_stations)

    y1_count, y2_count = ray.get([gsod_y1.get_high_temp_count.remote(intersection),
                                  gsod_y2.get_high_temp_count.remote(intersection)])

    print('Number of stations in common: {}'.format(len(intersection)))
    print('{} - High temp count for common stations: {}'.format(year1, y1_count))
    print('{} - High temp count for common stations: {}'.format(year2, y2_count))

#Running the code below will output which year had more extreme temperatures
compare_years('1980', '2020', 100)