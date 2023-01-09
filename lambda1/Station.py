import config as cfg
import requests
from lxml import html

class Station:

    def __init__(self, station_name):
        # self.station_code = station_code
        self.station_name = station_name
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
          
        tree = html.fromstring(self.departurevision_html)
        
        # parse arrival boxes using XPath
        raw_rows = tree.xpath("//div[@class='media no-gutters p-3']")
        parsed_rows=[str(row.xpath("string()")) for row in raw_rows]
        split_rows = [row.split('\n') for row in parsed_rows]
        stripped_rows = []
        for row in split_rows:
            stripped_row = []
            for word in row:
                stripped_row.append(word.strip())
            stripped_rows.append([i for i in stripped_row if i])
        dict_rows = {}
        for row in stripped_rows:
            dict_rows[row[1].split(' ')[1]]={
                'destination': row[0].split('-')[0],
                'eta': row[3].lower(),
                'track': row[4].split(' ')[1]
            }

        return dict_rows

# testing
if __name__ == "__main__":
    s = Station("Hoboken Terminal")
    print(s.departurevision_arrivals)
