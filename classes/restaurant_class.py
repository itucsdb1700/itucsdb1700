class Restaurant:
  def __init__(self, restaurantName, locationID, menuType, restaurantPoint, openingTime, closingTime, ownerEmail, ownerPhone, serviceType):
    self.restaurantName = restaurantName
    self.locationID = locationID
    self.menuType = menuType
    self.restaurantPoint = restaurantPoint
    self.openingTime = openingTime
    self.closingTime = closingTime
    self.ownerEmail = ownerEmail
    self.ownerPhone = ownerPhone
    self.serviceType = serviceType

    def get_restaurant_name(self):
        return self.restaurantName
    def get_location_id(self):
        return self.locationID
    def get_menu_type(self):
        return self.menuType
    def get_restaurant_point(self):
        return self.restaurantPoint
    def get_opening_time(self):
        return self.openingTime
    def get_closing_time(self):
        return self.closingTime
    def get_owner_email(self):
        return self.ownerEmail
    def get_owner_phone(self):
        return self.ownerPhone
    def get_service_type(self):
        return self.service_type

