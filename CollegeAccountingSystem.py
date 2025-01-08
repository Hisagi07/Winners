import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import qrcode
from io import BytesIO
from tkinter import ttk

# Path for credentials file
CREDENTIALS_FILE = "user_credentials.json"

# Load user credentials from file
if os.path.exists(CREDENTIALS_FILE):
    with open(CREDENTIALS_FILE, "r") as file:
        USER_CREDENTIALS = json.load(file)
else:
    USER_CREDENTIALS = {}

# Example student fees data
STUDENT_FEES = {
    "John Doe": 70000 - 45000,
    "Jane Smith": 70000 - 30000,
    "Alice Johnson": 70000 - 70000,
}

# Function to save credentials to file
def save_credentials():
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump(USER_CREDENTIALS, file)

# Function to handle login
def login():
    username = username_entry.get()
    password = password_entry.get()

    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        open_homepage()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Function to handle sign-up
def signup():
    username = username_entry.get()
    password = password_entry.get()

    if username in USER_CREDENTIALS:
        messagebox.showerror("Sign-Up Failed", "Username already exists")
    elif username and password:
        USER_CREDENTIALS[username] = password
        save_credentials()
        messagebox.showinfo("Sign-Up Successful", "Account created successfully! Redirecting to homepage.")
        open_homepage()
    else:
        messagebox.showerror("Sign-Up Failed", "Please enter a valid username and password")

# Function to handle forgot password
def forgot_password():
    def reset_password():
        username = username_entry.get()
        new_password = password_entry.get()

        if username in USER_CREDENTIALS:
            USER_CREDENTIALS[username] = new_password
            save_credentials()
            messagebox.showinfo("Password Reset", "Password changed successfully")
            forgot_window.destroy()
        else:
            messagebox.showerror("Error", "Username does not exist")

    forgot_window = tk.Toplevel(app)
    forgot_window.title("Reset Password")
    forgot_window.geometry("400x250")
    forgot_window.configure(bg="#2E4053")

    tk.Label(forgot_window, text="Reset Password", font=("Helvetica", 16), bg="#2E4053", fg="white").pack(pady=10)
    tk.Label(forgot_window, text="Username:", font=("Arial", 12), bg="#2E4053", fg="white").pack(pady=5)
    username_entry = tk.Entry(forgot_window, font=("Arial", 12), width=30)
    username_entry.pack()
    tk.Label(forgot_window, text="New Password:", font=("Arial", 12), bg="#2E4053", fg="white").pack(pady=5)
    password_entry = tk.Entry(forgot_window, font=("Arial", 12), width=30, show="*")
    password_entry.pack()

    reset_button = tk.Button(forgot_window, text="Reset Password", font=("Arial", 12), bg="green", fg="white", command=reset_password)
    reset_button.pack(pady=10)

# Function to toggle password visibility
def toggle_password():
    if password_entry.cget('show') == '*':
        password_entry.config(show='')
        show_password_button.config(text="Hide Password")
    else:
        password_entry.config(show='*')
        show_password_button.config(text="Show Password")

# Function to generate a QR code
def generate_qr_code(data):
    qr = qrcode.QRCode(box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    return ImageTk.PhotoImage(img)

# Function to generate a Google Pay UPI QR code
def generate_google_pay_qr():
    # Replace this with your actual Google Pay UPI link
    google_pay_upi_link = "upi://pay?pa=bondgun12@oksbi&pn=Kaustubh&mc=0000&tid=00000000&tr=00000000&tn=PaymentDescription&am=100.00&cu=INR&url=yoururl.com"
    qr_code_image = generate_qr_code(google_pay_upi_link)  # Use the function to generate the QR
    return qr_code_image

# Function to search for student fees
def search_student_fees():
    student_name = search_entry.get()
    if student_name in STUDENT_FEES:
        balance = STUDENT_FEES[student_name]
        search_result_label.config(text=f"Balance Fees: ₹{balance}")
    else:
        search_result_label.config(text="Student not found")

# Function to open the homepage
def open_homepage():
    homepage = tk.Toplevel(app)
    homepage.title("Homepage")
    homepage.geometry("900x600")
    homepage.configure(bg="#34495E")

    tk.Label(homepage, text="Welcome to the Homepage!", font=("Helvetica", 18), bg="#34495E", fg="white").pack(pady=10)

    # Widget 1: Google Pay QR Code
    tk.Label(homepage, text="Scan to Pay via Google Pay", font=("Arial", 14), bg="#34495E", fg="white").pack(pady=5)
    google_pay_qr_image = generate_google_pay_qr()  # Generate Google Pay QR Code
    google_pay_qr_label = tk.Label(homepage, image=google_pay_qr_image, bg="#34495E")
    google_pay_qr_label.image = google_pay_qr_image  # Keep a reference to the image
    google_pay_qr_label.pack(pady=10)

    # Widget 2: Expenses Graph
    tk.Label(homepage, text="College Expenses", font=("Arial", 14), bg="#34495E", fg="white").pack(pady=10)
    fig, ax = plt.subplots(figsize=(5, 3))
    categories = ["Library", "Hostel", "Mess", "Sports"]
    expenses = [20000, 30000, 25000, 15000]
    ax.bar(categories, expenses, color="#2980B9")
    ax.set_title("Expenses")
    ax.set_ylabel("Amount (₹)")
    canvas = FigureCanvasTkAgg(fig, homepage)
    canvas.get_tk_widget().pack(pady=10)

    # Widget 3: Search Student Fees
    tk.Label(homepage, text="Check Student Fees", font=("Arial", 14), bg="#34495E", fg="white").pack(pady=10)
    search_frame = tk.Frame(homepage, bg="#34495E")
    search_frame.pack(pady=5)

    tk.Label(search_frame, text="Student Name:", font=("Arial", 12), bg="#34495E", fg="white").grid(row=0, column=0, padx=5)
    search_entry = tk.Entry(search_frame, font=("Arial", 12))
    search_entry.grid(row=0, column=1, padx=5)
    search_button = tk.Button(search_frame, text="Search", font=("Arial", 12), bg="#2980B9", fg="white", command=search_student_fees)
    search_button.grid(row=0, column=2, padx=5)

    global search_result_label
    search_result_label = tk.Label(homepage, text="", font=("Arial", 12), bg="#34495E", fg="white")
    search_result_label.pack(pady=5)

# Save credentials before exiting the app
def on_closing():
    save_credentials()
    app.destroy()

# Initialize the main application window
app = tk.Tk()
app.title("College Accounting System - Login")
app.geometry("600x500")

# Load and set background image
bg_image = Image.open(r"C:\Users\bondg\Downloads\2024-red-dead-redemption-2-minimal-game-4k-3840x2160_1703815995.jpg")  # Replace with your background image path
bg_image = bg_image.resize((1920, 1080), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)
background_label = tk.Label(app, image=bg_photo)
background_label.place(relwidth=1, relheight=1)

# Login Frame with transparency
login_frame = tk.Frame(app, bg="#2E4053", bd=0, highlightthickness=0)
login_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=300)

# App header
header_label = tk.Label(login_frame, text="Login", font=("Helvetica", 20, "bold"), bg="#2E4053", fg="white")
header_label.pack(pady=10)

# Username label and entry
username_label = tk.Label(login_frame, text="Username:", font=("Arial", 12), bg="#2E4053", fg="white")
username_label.pack(pady=5)
username_entry = tk.Entry(login_frame, font=("Arial", 12), width=30)
username_entry.pack()

# Password label and entry
password_label = tk.Label(login_frame, text="Password:", font=("Arial", 12), bg="#2E4053", fg="white")
password_label.pack(pady=5)
password_entry = tk.Entry(login_frame, font=("Arial", 12), width=30, show="*")
password_entry.pack()

# Show password button
show_password_button = tk.Button(login_frame, text="Show Password", font=("Arial", 10), bg="#34495E", fg="white", relief="flat", command=toggle_password)
show_password_button.pack(pady=5)

# Styled Buttons
style = {"font": ("Arial", 12), "bg": "#2980B9", "fg": "white", "relief": "flat", "width": 15}

# Login button
login_button = tk.Button(login_frame, text="Login", **style, command=login)
login_button.pack(pady=10)

# Sign-Up button
signup_button = tk.Button(login_frame, text="Sign Up", **style, command=signup)
signup_button.pack(pady=5)

# Forgot Password button
forgot_password_button = tk.Button(login_frame, text="Forgot Password?", font=("Arial", 10), bg="#34495E", fg="white", relief="flat", command=forgot_password)
forgot_password_button.pack(pady=5)

# Handle app close
app.protocol("WM_DELETE_WINDOW", on_closing)

# Run the application
app.mainloop()
