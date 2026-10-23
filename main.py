from users import Lecturer, CampusAdministrator, SystemOperator # 3
from database import (
    add_resource, update_resource, delete_resource,
    view_resources, login_user,
    get_campus_policy)
from resources import Resource
from bookings import Booking

lecture = Lecturer("John", "1425","Lecturer", 1) # 3.1
Admin = CampusAdministrator("Mark", "67","CampusAdministrator", 2)  # 3.2
operator = SystemOperator("Danger Room", "0101","Operator", 3) # 3.3

print(lecture.username, lecture.role) # 3.1
print(Admin.username, Admin.role) # 3.2
print(operator.username, operator.role) # 3.3

login_user(username="David", password="1234")
#add_resource("Projector Q", "Projector", 1)
#get_resource_by_id(1)
#delete_resource(1)
view_resources()
#add_resource("Projector Q", "Projector", 1)
view_resources()
update_resource(2,"Projector B", "Pro Projector", 2)
view_resources()

resource1 = Resource(
    1, "Resource A",
    "Projector", 1)
resource1.display_resource()

booking1 = Booking(
    1,
    2,
    1,
    "2026-01-23",
    "08:00",
    2,
    "Active"
)
booking1.display_booking()