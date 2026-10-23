class Booking:
    def __init__(self, booking_id, user_id, resource_id, booking_date, start_time, duration,status):
        self.booking_id = booking_id
        self.user_id = user_id
        self.resource_id = resource_id
        self.booking_date = booking_date
        self.start_time = start_time
        self.duration = duration
        self.status = status

    def display_booking(self):
        print(
            f"Booking ID: {self.booking_id}\n"
            f"User ID: {self.user_id}\n"
            f"Resource ID: {self.resource_id}\n"
            f"Booking Date: {self.booking_date}\n"
            f"Start Time: {self.start_time}\n"
            f"Duration: {self.duration} hours(s)\n"
            f"Status: {self.status}"
        )