import config as cfg
import requests
from lxml import html

class Arrival:

    def __init__(self, row):
        self.parsed_content = str(row.xpath("string()")).split('\n')
        self.train_no = self.parsed_content[1].strip().split(' ')[1]
        self.destination = self.parse_destination()
        self.eta = self.parse_eta()

    def parse_destination(self):
        destination = self.parsed_content[0].strip()
        if len(destination.split('-')) > 1:
            destination = destination.split('-')[0]

        suffixes = ["MAIN"," SEC", "-SEC", "MOBO"," M&E", "RARV"]

        if destination[-4:] in suffixes:
            d = ' '.join(destination.split(' ')[:-1])
            return d

        return destination

    def parse_eta(self):
        # handled "To Be Announced" message
        if "View Stops" in self.parsed_content[5]:
            return self.parsed_content[7].strip().lower()
        else:
            return self.parsed_content[5].strip().lower()
    

class Station:

    def __init__(self, station_name, num_arrivals):
        # self.station_code = station_code
        self.station_name = station_name
        self.num_arrivals = int(num_arrivals)
        self.departurevision_url = f"https://www.njtransit.com/dv-to/{self.station_name}"
        self.departurevision_html = self.get_departurevision_html()
        self.departurevision_arrivals = self.parse_departurevision_html()

    def __repr__(self):
        return f"Station (station_name={self.station_name}, updated={self.arrivals_fetch_time}, no_arrivals={len(self.arrivals)})"

    #scrape the DepartureVision app like https://www.njtransit.com/dv-to/Hoboken%20Terminal
    def get_departurevision_html(self):
        response = requests.get(self.departurevision_url)
        return response.content

    def parse_departurevision_html(self):

        # parse arrival boxes using XPath
        arrival_blocks = html.fromstring(self.departurevision_html).xpath("//div[@class='media no-gutters p-3']")
        rows = [Arrival(r) for r in arrival_blocks][:self.num_arrivals]

        return rows

# testing
if __name__ == "__main__":
    s = Station("Hoboken Terminal")
    print(s.departurevision_arrivals)
