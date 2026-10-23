# STAGE 4
# Opens the database.py
import sqlite3

# STAGE 8
#import resources

# Creates the Database Connection STAGE 4
conn = sqlite3.connect('project.db')
c = conn.cursor()

# Creating my Users table STAGE 4.1
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    campus_id INTEGER NOT NULL 
    )
""")

# Creating a Resources Table STAGE 4.2
c.execute("""
CREATE TABLE IF NOT EXISTS resources (
    resource_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    resource_name TEXT NOT NULL,
    resource_type TEXT NOT NULL,
    campus_id INTEGER NOT NULL 
    )
""")

# Creating a Bookings Table STAGE 4.3
c.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    resource_id INTEGER NOT NULL,
    booking_date TEXT NOT NULL,
    start_time TEXT NOT NULL,
    duration INTEGER NOT NULL,
    status TEXT NOT NULL
    )
""")

# This is where we Save the Changes STAGE 4
conn.commit()
# Closing the Database STAGE 4
conn.close()

# Notify a Message of Success STAGE 4
#print("Database and all it's tables were created successfully")

#STAGE 5
def add_user(username, password, role, campus_id):
    conn = sqlite3.connect('project.db') # What's creating out connection to the database
    c = conn.cursor()

    c.execute("""
        INSERT INTO users 
        (username, password, role, campus_id)
        VALUES (?, ?, ?, ?)
    """, (username, password, role, campus_id))

    conn.commit()
    conn.close()

    print("User was successfully added")

def add_resource(resource_name, resource_type, campus_id):
    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        INSERT INTO resources
        (resource_name, resource_type, campus_id)
        VALUES (?, ?, ?)
    """, (resource_name, resource_type, campus_id))

    conn.commit()
    conn.close()

    print("Resource was successfully added")

def booking_exists(resource_id, booking_date, start_time):
    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        SELECT * FROM bookings
        WHERE resource_id = ?
        AND booking_date = ?
        AND start_time = ?
        AND status = 'Active'
    """, (resource_id, booking_date, start_time))

    booking = c.fetchone()
    conn.close()

    if booking:
        return True
    else:
        return False

def add_booking(user_id, resource_id, booking_date, start_time, duration, status):
    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
                SELECT campus_id
                FROM users
                WHERE user_id = ?
            """, (user_id,))

    result = c.fetchone()

    conn.close()

    if not result:
        print("User not found")
        return

    campus_id = result[0]

    if booking_exists(resource_id, booking_date, start_time):
        if not validate_campus_booking(
                campus_id,
                duration,
                start_time):
            print("Campus booking policy violated")
            return


    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        INSERT INTO bookings
        (user_id, resource_id, booking_date, start_time, duration, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, resource_id, booking_date, start_time, duration, status))

    conn.commit()
    conn.close()

    print("Booking was successfully added")

# STAGE 6
def view_users():
    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        SELECT * FROM users
        order by user_id desc
    """)

    # Will grab all the rows returned by query
    users = c.fetchall()

    for user in users:
        print(user)

    conn.close()

#add_user(username="David", password="1234", role="Lecturer", campus_id=1)
#view_users()

# STAGE 7
def login_user(username, password):
    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        SELECT * FROM users
        WHERE username = ?
        AND password = ?
    """, (username, password))

    user = c.fetchone()

    conn.close()

    if user:
        print("Logged in successfully")
        return user
    else:
        print("Login failed")
        return None

# STAGE 8
# Resource Management
def view_resources():
    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        SELECT * FROM resources
        ORDER BY resource_id desc
    """)

    resources = c.fetchall()

    for resource in resources:
        print(resource)

    conn.close()

def resource_exists(resource_name, campus_id):
    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        SELECT *
        FROM resources
        WHERE resource_name = ?
        AND campus_id = ?
    """, (resource_name, campus_id))

    resource = c.fetchone()

    conn.close()

    if resource:
        return True
    else:
        return False

def get_resource_by_id(resource_id):
    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        SELECT * FROM resources
        WHERE resource_id = ?
    """, (resource_id,))

    resource = c.fetchone()

    if resource:
        print(resource)
    else:
        print("Resource not found")

    conn.close()

def delete_resource(resource_id):
    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        DELETE FROM resources
        WHERE resource_id = ?
    """, (resource_id,))

    rows_delete = c.rowcount

    conn.commit()
    conn.close()

    if rows_delete > 0:
        print("Deletion of resource was successful")
    else:
        print("Resource not found")

# STAGE 9
# Update Resource
def update_resource(resource_id, resource_name, resource_type, campus_id):
    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        UPDATE resources
        SET resource_name = ?,
            resource_type = ?,
            campus_id = ?
        WHERE resource_id = ?
    """, (resource_name, resource_type, campus_id, resource_id))

    rows_update = c.rowcount

    conn.commit()
    conn.close()

    if rows_update > 0:
        print("Updating resource was successful")
    else:
        print("Resource not found")

# STAGE 10
def view_bookings():
    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        SELECT * FROM bookings
        ORDER BY booking_date desc, start_time desc
    """)

    bookings = c.fetchall()

    for booking in bookings:
        print(booking)

    conn.close()

def get_booking_by_resource(resource_id):
    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        SELECT * FROM bookings
        WHERE resource_id = ?
    """, (resource_id,))

    booking = c.fetchall()

    if booking:
        for b in booking:
            print(b)
    else:
        print("Resource not found")

    conn.close()

def cancel_booking(booking_id):
    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        UPDATE bookings
        SET status = ?
        WHERE booking_id = ?
    """, ("Cancelled",booking_id,))

    rows_cancel = c.rowcount

    conn.commit()
    conn.close()

    if rows_cancel > 0:
        print("Booking cancelled successfully")
    else:
        print("Booking not found")

def get_booking_by_id(booking_id):
    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        SELECT * FROM bookings
        WHERE booking_id = ?
    """, (booking_id,))

    booking = c.fetchone()

    if booking:
        print(booking)
    else:
        print("No Bookings found for this resource")

    conn.close()

def update_booking_status(booking_id, status):
    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        UPDATE bookings
        SET status = ?
        WHERE booking_id = ?
    """, (status,booking_id,))

    rows_updated = c.rowcount

    conn.commit()
    conn.close()

    if rows_updated > 0:
        print("Booking status updated was successful")
    else:
        print("Booking status not found")

def resource_availability(resource_id, booking_date):
    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        SELECT * FROM bookings
        WHERE resource_id = ?
        AND booking_date = ?
        AND status = ?
    """, (resource_id, booking_date, "Active"))

    booking = c.fetchone()
    conn.close()

    if booking:
        print("Resource availability was unsuccessful")
        return False
    else:
        print("Resource availability was successful")
        return True
def view_active_bookings():
    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        SELECT * FROM bookings
        WHERE status = ?
    """,("Active",))

    bookings = c.fetchall()

    for booking in bookings:
        print(booking)

    conn.close()

def view_cancelled_bookings():
    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        SELECT * FROM bookings
        WHERE status = ?
    """,("Cancelled",))

    bookings = c.fetchall()

    for booking in bookings:
        print(booking)

    conn.close()

def validate_campus_booking(
        campus_id,
        duration,
        start_time):

    if campus_id not in campus_policies:
        return False

    policy = campus_policies[campus_id]

    if duration > policy["max_duration"]:
        print(
            f"Maximum booking duration is "
            f"{policy['max_duration']} hour(s)"
        )
        return False

    booking_hour = int(start_time.split(":")[0])

    if booking_hour < policy["start_hour"]:
        print("Booking is before allowed hours")
        return False

    if booking_hour >= policy["end_hour"]:
        print("Booking is after allowed hours")
        return False

    return True

campus_policies = {
    1: {
        "name": "Pretoria",
        "max_duration": 2,
        "start_hour": 8,
        "end_hour": 17
    },

    2: {
        "name": "Johannesburg",
        "max_duration": 3,
        "start_hour": 7,
        "end_hour": 18
    },

    3: {
        "name": "Durban",
        "max_duration": 4,
        "start_hour": 9,
        "end_hour": 16
    }
}

def get_campus_policy(campus_id):

    if campus_id in campus_policies:
        return campus_policies[campus_id]

    return None

def generate_report():
    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        SELECT COUNT(*)
        FROM users
    """)

    total_users = c.fetchone()[0]

    c.execute("""
              SELECT COUNT(*)
              FROM resources
              """)

    total_resources = c.fetchone()[0]

    c.execute("""
              SELECT COUNT(*)
              FROM bookings
              """)

    total_bookings = c.fetchone()[0]

    c.execute("""
              SELECT COUNT(*)
              FROM bookings
              WHERE status = 'Active'
              """)

    active_bookings = c.fetchone()[0]

    c.execute("""
              SELECT COUNT(*)
              FROM bookings
              WHERE status = 'Cancelled'
              """)

    cancelled_bookings = c.fetchone()[0]

    print("===== SYSTEM REPORT =====")
    print(f"Total Users: {total_users}")
    print(f"Total Resources: {total_resources}")
    print(f"Total Bookings: {total_bookings}")
    print(f"Active Bookings: {active_bookings}")
    print(f"Cancelled Bookings: {cancelled_bookings}")

    conn.close()

def view_campus_bookings(campus_id):
    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        SELECT b.*
        FROM bookings b
        JOIN users u
            ON b.user_id = u.user_id
        WHERE u.campus_id = ?
        ORDER BY b.booking_date DESC,
                 b.start_time DESC
    """, (campus_id,))

    bookings = c.fetchall()

    if bookings:
        for booking in bookings:
            print(booking)
    else:
        print("No bookings found for this campus")

    conn.close()

def most_used_resources(campus_id):

    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        SELECT r.resource_name,
               COUNT(*) AS bookings_count
        FROM bookings b
        JOIN resources r
        ON b.resource_id = r.resource_id
        WHERE r.campus_id = ?
        GROUP BY r.resource_name
        ORDER BY bookings_count DESC
        LIMIT 1
    """, (campus_id,))

    resource = c.fetchone()

    conn.close()

    if resource:
        print(
            f"Most Used Resource: "
            f"{resource[0]}"
        )
    else:
        print("No usage data available")

def average_booking_duration(campus_id):

    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        SELECT AVG(duration)
        FROM bookings b
        JOIN resources r
        ON b.resource_id = r.resource_id
        WHERE r.campus_id = ?
    """, (campus_id,))

    average = c.fetchone()[0]

    conn.close()

    if average:
        print(
            f"Average Duration: "
            f"{average:.2f} hours"
        )
    else:
        print("No booking data available")

def campus_resource_availability(campus_id):

    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        SELECT *
        FROM resources
        WHERE campus_id = ?
    """, (campus_id,))

    resources = c.fetchall()

    print("===== CAMPUS RESOURCES =====")

    for resource in resources:
        print(resource)

    conn.close()

def campus_report(campus_id):

    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        SELECT COUNT(*)
        FROM bookings b
        JOIN resources r
        ON b.resource_id = r.resource_id
        WHERE r.campus_id = ?
    """, (campus_id,))
    total_bookings = c.fetchone()[0]

    c.execute("""
        SELECT r.resource_name,
               COUNT(*) AS usage_count
        FROM bookings b
        JOIN resources r
        ON b.resource_id = r.resource_id
        WHERE r.campus_id = ?
        GROUP BY r.resource_name
        ORDER BY usage_count DESC
        LIMIT 1
    """, (campus_id,))
    most_used = c.fetchone()

    c.execute("""
        SELECT AVG(duration)
        FROM bookings b
        JOIN resources r
        ON b.resource_id = r.resource_id
        WHERE r.campus_id = ?
    """, (campus_id,))
    avg_duration = c.fetchone()[0]

    conn.close()

    print("===== CAMPUS REPORT =====")

    print(
        f"Total Bookings: "
        f"{total_bookings}"
    )

    if most_used:
        print(
            f"Most Used Resource: "
            f"{most_used[0]}"
        )

    if avg_duration:
        print(
            f"Average Booking Duration: "
            f"{avg_duration:.2f} hours"
        )

def view_user_booking_history(user_id):

    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        SELECT *
        FROM bookings
        WHERE user_id = ?
        ORDER BY booking_date DESC
    """, (user_id,))

    bookings = c.fetchall()

    for booking in bookings:
        print(booking)

    conn.close()

def campus_total_bookings(campus_id):

    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        SELECT COUNT(*)
        FROM bookings b
        JOIN resources r
        ON b.resource_id = r.resource_id
        WHERE r.campus_id = ?
    """, (campus_id,))

    total_bookings = c.fetchone()[0]

    conn.close()

    print(f"Total Bookings: {total_bookings}")

def compare_resource_usage():

    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        SELECT
            r.campus_id,
            COUNT(*) AS usage_count
        FROM bookings b
        JOIN resources r
            ON b.resource_id = r.resource_id
        GROUP BY r.campus_id
        ORDER BY usage_count DESC
    """)

    results = c.fetchall()

    conn.close()

    print("===== RESOURCE USAGE BY CAMPUS =====")

    for campus in results:
        print(
            f"Campus {campus[0]}: "
            f"{campus[1]} bookings"
        )

def compare_booking_trends():

    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        SELECT
            r.campus_id,
            COUNT(*) AS total_bookings,
            AVG(b.duration) AS avg_duration
        FROM bookings b
        JOIN resources r
            ON b.resource_id = r.resource_id
        GROUP BY r.campus_id
        ORDER BY r.campus_id
    """)

    trends = c.fetchall()

    conn.close()

    print("===== CAMPUS BOOKING TRENDS =====")

    for trend in trends:
        print(
            f"Campus {trend[0]} | "
            f"Bookings: {trend[1]} | "
            f"Average Duration: {trend[2]:.2f} hours"
        )

def cross_campus_report():

    conn = sqlite3.connect('project.db')
    c = conn.cursor()

    c.execute("""
        SELECT
            r.campus_id,
            COUNT(*) AS total_bookings,
            AVG(b.duration) AS avg_duration
        FROM bookings b
        JOIN resources r
            ON b.resource_id = r.resource_id
        GROUP BY r.campus_id
    """)

    data = c.fetchall()

    conn.close()

    print("===== CROSS CAMPUS REPORT =====")

    for row in data:
        print(
            f"Campus {row[0]} | "
            f"Bookings: {row[1]} | "
            f"Avg Duration: {row[2]:.2f} hours"
        )

"""
add_booking(
    1,
    1,
    "2026-10-23",
    "08:00",
    2,
    "Active"
)
"""

"""
add_booking(
    2,
    1,
    "2026-10-23",
    "08:00",
    2,
    "Active"
)
"""

#print(validate_campus_booking(1, 2))
#print(validate_campus_booking(1, 5))
#print(validate_campus_booking(3, 4))
#print(validate_campus_booking(3, 5))

#add_user("David", "1234", "Lecturer", 1)

#add_user("Mark", "1234", "CampusAdministrator", 2)

#add_user("Sarah", "1234", "Operator", 3)

generate_report()