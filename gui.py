import tkinter as tk
from database import (
    login_user, view_users,
    view_bookings, add_resource,
    update_resource, delete_resource,
    view_resources, generate_report,
    add_booking, cancel_booking,
    most_used_resources, campus_resource_availability,
    view_campus_bookings, get_campus_policy,
    view_active_bookings, resource_availability,
    campus_report, cross_campus_report)
from tkinter import messagebox

root = tk.Tk()
root.title("Campus Resource Booking System")
root.geometry("300x300")

signup_frame = tk.Frame(root)
signup_frame.pack(pady=20)

active_campus = tk.StringVar()
active_campus.set("No Campus Selected")

tk.Label(
    signup_frame,
    text="Campus Resource Booking System",
    font=("Arial", 14, "bold")
).pack(pady=10)

tk.Label(signup_frame, text="Username:").pack()
username_entry = tk.Entry(signup_frame)
username_entry.pack()

tk.Label(signup_frame, text="Password:").pack()
password_entry = tk.Entry(signup_frame, show="*")
password_entry.pack()

def login():
    username = username_entry.get()
    password = password_entry.get()

    user = login_user(username, password)

    if user:
        role = user[3]

        policy = get_campus_policy(user[4])
        signup_frame.pack_forget()

        if role == "Lecturer":
            lecture_frame.pack(pady=20)
        elif role == "CampusAdministrator":
            admin_frame.pack(pady=20)
        elif role == "Operator":
            operator_frame.pack(pady=20)

        policy_label = tk.Label(
            root,
            text=""
        )

        policy_label.config(
            text=
            f"Campus: {policy['name']} | "
            f"Max Duration: {policy['max_duration']}h | "
            f"Hours: {policy['start_hour']}:00-"
            f"{policy['end_hour']}:00"
        )

        policy_label.pack()

        messagebox.showinfo("Success", "Logged in successfully")
    else:
        messagebox.showerror("Error", "Login failed")


campus_frame = tk.Frame(root)
signup_frame.pack_forget()
campus_frame.pack(pady=20)

tk.Label(
    campus_frame,
    text="Select Campus",
    font=("Arial", 14, "bold")
).pack(pady=10)

selected_campus = tk.StringVar()

campus_dropdown = tk.OptionMenu(
    campus_frame,
    selected_campus,
    "Pretoria Campus",
    "Johannesburg Campus",
    "Durban Campus"
)

campus_dropdown.pack(pady=10)

active_campus_label = tk.Label(
    campus_frame,
    textvariable=active_campus,
    font=("Arial", 12)
)

active_campus_label.pack(pady=10)

def select_campus():

    campus = selected_campus.get()

    active_campus.set(
        f"Active Campus: {campus}"
    )

    messagebox.showinfo(
        "Campus Selected",
        f"You selected {campus}"
    )

tk.Button(
    campus_frame,
    text="Select Campus",
    command=select_campus
).pack(pady=10)

campuses = {
    1: {
        "name": "Pretoria Campus",
        "max_hours": 2
    },
    2: {
        "name": "Johannesburg Campus",
        "max_hours": 3
    },
    3: {
        "name": "Durban Campus",
        "max_hours": 4
    }
}

def select_campus():
    campus_frame.pack_forget()

login_button = tk.Button(
    signup_frame,
    text="Login",
    command=login
)
login_button.pack(pady=10)

lecture_frame = tk.Frame(root)
lecture_frame.pack(pady=20)

def show_resources():
    view_resources()

def show_bookings():
    view_bookings()

def logout():
    lecture_frame.pack_forget()
    admin_frame.pack_forget()
    operator_frame.pack_forget()

    signup_frame.pack(pady=20)

    messagebox.showinfo("Logging Out", "Logged out successfully")

def open_booking_window():
    booking_window = tk.Toplevel(root)
    booking_window.title("Book Resource")
    booking_window.geometry("300x300")

    tk.Label(booking_window, text="User ID").pack()
    user_id_entry = tk.Entry(booking_window)
    user_id_entry.pack()

    tk.Label(booking_window, text="Resource ID").pack()
    resource_id_entry = tk.Entry(booking_window)
    resource_id_entry.pack()

    tk.Label(booking_window, text="Booking Date (YYYY-MM-DD)").pack()
    booking_date_entry = tk.Entry(booking_window)
    booking_date_entry.pack()

    tk.Label(booking_window, text="Start Time (HH:MM)").pack()
    start_time_entry = tk.Entry(booking_window)
    start_time_entry.pack()

    tk.Label(booking_window, text="Duration (Hours)").pack()
    duration_entry = tk.Entry(booking_window)
    duration_entry.pack()

    def submit_booking():
        try:
            add_booking(
                int(user_id_entry.get()),
                int(resource_id_entry.get()),
                booking_date_entry.get(),
                start_time_entry.get(),
                int(duration_entry.get()),
                "Active"
            )

            messagebox.showinfo(
                "Success",
                "Booking created successfully"
            )

            booking_window.destroy()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    tk.Button(
        booking_window,
        text="Book Resource",
        command=submit_booking
    ).pack(pady=10)

def open_cancel_booking_window():

    cancel_window = tk.Toplevel(root)
    cancel_window.title("Cancel Booking")

    tk.Label(
        cancel_window,
        text="Booking ID"
    ).pack()

    booking_id_entry = tk.Entry(cancel_window)
    booking_id_entry.pack()

    def submit_cancel():

        cancel_booking(
            int(booking_id_entry.get())
        )

        messagebox.showinfo(
            "Success",
            "Booking cancelled successfully"
        )

        cancel_window.destroy()

    tk.Button(
        cancel_window,
        text="Cancel Booking",
        command=submit_cancel
    ).pack(pady=10)

tk.Button(
    lecture_frame,
    text="Book Resources",
    font=("Arial", 14, "bold"),
    command= open_booking_window
).pack(pady=5)


tk.Button(
    lecture_frame,
    text="Cancel Booking",
    font=("Arial", 14, "bold"),
    command= open_cancel_booking_window
).pack(pady=5)

tk.Button(
    lecture_frame,
    text="View Resources",
    font=("Arial", 14, "bold"),
    command= show_resources
).pack(pady=5)

tk.Button(
    lecture_frame,
    text="View Bookings",
    font=("Arial", 14, "bold"),
    command= show_bookings
).pack(pady=5)

tk.Button(
    lecture_frame,
    text="Logout",
    font=("Arial", 14, "bold"),
    command= logout
).pack(pady=5)

lecture_frame.pack_forget()

admin_frame = tk.Frame(root)
admin_frame.pack(pady=20)

def admin_add_resource():

    window = tk.Toplevel(root)
    window.title("Add Resource")

    tk.Label(window, text="Resource Name").pack()
    name_entry = tk.Entry(window)
    name_entry.pack()

    tk.Label(window, text="Resource Type").pack()
    type_entry = tk.Entry(window)
    type_entry.pack()

    tk.Label(window, text="Campus ID").pack()
    campus_entry = tk.Entry(window)
    campus_entry.pack()

    def save_resource():

        add_resource(
            name_entry.get(),
            type_entry.get(),
            int(campus_entry.get())
        )

        messagebox.showinfo(
            "Success",
            "Resource Added"
        )

        window.destroy()

    tk.Button(
        window,
        text="Save",
        command=save_resource
    ).pack(pady=10)

def admin_update_resource():
    messagebox.showinfo(
        "Update Resource",
        "Feature coming next"
    )

def admin_delete_resource():

    window = tk.Toplevel(root)
    window.title("Delete Resource")

    tk.Label(window, text="Resource ID").pack()

    resource_id_entry = tk.Entry(window)
    resource_id_entry.pack()

    def delete_it():

        delete_resource(
            int(resource_id_entry.get())
        )

        window.destroy()

    tk.Button(
        window,
        text="Delete",
        command=delete_it
    ).pack(pady=10)

def show_report():
    generate_report()

def show_users():
    view_users()

def show_campus_resources():
    view_resources()

def show_usage_trends():
    most_used_resources()

tk.Button(
    admin_frame,
    text="Add Resource",
    font=("Arial", 14, "bold"),
    command=admin_add_resource
).pack(pady=5)

tk.Button(
    admin_frame,
    text="Update Resource",
    font=("Arial", 14, "bold"),
    command= admin_update_resource
).pack(pady=5)

tk.Button(
    admin_frame,
    text="Delete Resource",
    font=("Arial", 14, "bold"),
    command= admin_delete_resource
).pack(pady=5)

tk.Button(
    admin_frame,
    text="View Resource",
    font=("Arial", 14, "bold"),
    command= show_resources
).pack(pady=5)

tk.Button(
    admin_frame,
    text="Logout",
    font=("Arial", 14, "bold"),
    command = logout
).pack(pady=5)

admin_frame.pack_forget()

operator_frame = tk.Frame(root)
operator_frame.pack(pady=20)

tk.Button(
    operator_frame,
    text="View Users",
    font=("Arial", 14, "bold"),
    command= show_users
).pack(pady=5)

tk.Button(
    operator_frame,
    text="View Resources",
    font=("Arial", 14, "bold"),
    command = show_resources
).pack(pady=5)

tk.Button(
    operator_frame,
    text="View Bookings",
    font=("Arial", 14, "bold"),
    command= show_bookings
).pack(pady=5)

tk.Button(
    operator_frame,
    text="Generate Report",
    font=("Arial", 14, "bold"),
    command= show_report
).pack(pady=5)

tk.Button(
    operator_frame,
    text="Logout",
    font=("Arial", 14, "bold"),
    command= logout
).pack(pady=5)

operator_frame.pack_forget()

tk.Button(
    admin_frame,
    text="View Campus Bookings",
    command=lambda: view_campus_bookings(1)
).pack(pady=5)

tk.Button(
    admin_frame,
    text="Resource Availability",
    command=lambda: campus_resource_availability(1)
).pack(pady=5)

tk.Button(
    admin_frame,
    text="Usage Trends",
    command=most_used_resources
).pack(pady=5)

tk.Label(
    campus_frame,
    text="Select Campus",
    font=("Arial", 14, "bold")
).pack(pady=10)

def show_active_bookings():
    view_active_bookings()

tk.Button(
    lecture_frame,
    text="View Active Bookings",
    command=show_active_bookings
).pack(pady=5)

def open_cancel_booking_window():

    cancel_window = tk.Toplevel(root)
    cancel_window.title("Cancel Booking")
    cancel_window.geometry("300x200")

    tk.Label(
        cancel_window,
        text="Booking ID"
    ).pack(pady=10)

    booking_id_entry = tk.Entry(cancel_window)
    booking_id_entry.pack()

    def submit_cancel():
        try:
            booking_id = int(booking_id_entry.get())

            cancel_booking(booking_id)

            messagebox.showinfo(
                "Success",
                "Booking cancelled successfully"
            )

            cancel_window.destroy()

        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter a valid Booking ID"
            )

    tk.Button(
        cancel_window,
        text="Cancel Booking",
        command=submit_cancel
    ).pack(pady=10)

def check_resource_availability():

    availability_window = tk.Toplevel(root)
    availability_window.title("Resource Availability")
    availability_window.geometry("300x200")

    tk.Label(
        availability_window,
        text="Resource ID"
    ).pack()

    resource_id_entry = tk.Entry(
        availability_window
    )
    resource_id_entry.pack()

    tk.Label(
        availability_window,
        text="Booking Date (YYYY-MM-DD)"
    ).pack()

    booking_date_entry = tk.Entry(
        availability_window
    )
    booking_date_entry.pack()

    def check():

        available = resource_availability(
            int(resource_id_entry.get()),
            booking_date_entry.get()
        )

        if available:
            messagebox.showinfo(
                "Availability",
                "Resource is Available"
            )

        else:
            messagebox.showwarning(
                "Availability",
                "Resource is Unavailable"
            )

    tk.Button(
        availability_window,
        text="Check Availability",
        command=check
    ).pack(pady=10)

tk.Button(
    lecture_frame,
    text="Check Availability",
    font=("Arial", 14, "bold"),
    command=check_resource_availability
).pack(pady=5)

def show_campus_report():
    campus_report(1)

def show_cross_campus_report():
    cross_campus_report()

tk.Button(
    operator_frame,
    text="Cross-Campus Report",
    font=("Arial", 14, "bold"),
    command=show_cross_campus_report
).pack(pady=5)

root.mainloop()

