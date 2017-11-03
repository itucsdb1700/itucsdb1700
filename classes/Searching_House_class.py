class searchingHouseAnnouncement:
    def __init__(self,location,mixRent,maxRent,description,currentuser_id):
        self.LocationOfSearchingHouse = location
        self.MinRentPriceOfSearchingHouse = mixRent
        self.MaxRentPriceOfSearchingHouse = maxRent
        self.DescriptionOfSearchingHouse = description
        self.id_ownerOfSearchingHouseAnnouncement = currentuser_id