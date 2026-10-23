class Resource:
    def __init__(self, resource_id, resource_name, resource_type, campus_id):
        self.resource_id = resource_id
        self.resource_name = resource_name
        self.resource_type = resource_type
        self.campus_id = campus_id

    def display_resource(self):
        print(
            f"ID:{self.resource_id},"
            f"Name:{self.resource_name},"
            f"Type:{self.resource_type},"
            f"Campus ID:{self.campus_id}"
        )