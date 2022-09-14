class FlightData:
    def __init__(self, price, city_from, city_code_from, city_to, city_code_to, local_departure, nights_in_dest):
        self.price = price
        self.city_from = city_from
        self.city_code_from = city_code_from
        self.city_to = city_to
        self.city_code_to = city_code_to
        self.local_departure = local_departure
        self.nights_in_dest = nights_in_dest
