class Listing:
    def __init__(self, Title, URL, Condition, Price, Shipping=0.00, Best_Offer=False, Auction=False,):
        self.Title = Title
        self.URL = URL
        self.Condition = Condition
        self.Price = Price
        self.Best_Offer = Best_Offer
        self.Auction = Auction
        self.Shipping = Shipping