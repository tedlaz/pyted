"""
Σύμβαση εργασίας
"""


class Symbasi:
    """Symbasi"""
    def __init__(self):
        self.days_week = 5
        self.days_month = 25
        self.hours_week = 40
        self.hours_day = round(self.hours_week / self.days_week, 3)

    def __repr__(self):
        ast = "Symbasi ergasias\n"
        ast += "Working days per week  : %s\n" % self.days_week
        ast += "Working hours per Week : %s\n" % self.hours_week
        ast += "Working hours per day  : %s\n" % self.hours_day
        return ast

if __name__ == "__main__":
    sym = Symbasi()
    print(sym)
