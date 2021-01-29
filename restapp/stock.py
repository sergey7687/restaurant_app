class Stock:
    def __init__(self):
        self.stock = []

    def add_pos(self, pos):
        self.stock.append(pos)


    def get_stock(self):
        return self.stock


