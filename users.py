class User: # 3
    def __init__(self, username, password, role, campus_id):
        self.username = username
        self.password = password
        self.role = role
        self.campus_id = campus_id

class Lecturer(User): #3.1
    pass

class CampusAdministrator(User): #3.2
    pass

class SystemOperator(User): # 3.3
    pass