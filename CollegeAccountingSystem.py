import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Dummy database for login credentials (replace with actual database integration)
USER_CREDENTIALS = {}

# Function to handle login
def login():
    username = username_entry.get()
    password = password_entry.get()

    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        open_homepage()
    else:
        messagebox.showerror("Login Failed", "dispression mai hai kya")

# Function to handle sign-up
def signup():
    username = username_entry.get()
    password = password_entry.get()

    if username in USER_CREDENTIALS:
        messagebox.showerror("Sign-Up Failed", "Username already exists")
    elif username and password:
        USER_CREDENTIALS[username] = password
        messagebox.showinfo("Sign-Up Successful", "Account created successfully! Redirecting to homepage.")
        open_homepage()
    else:
        messagebox.showerror("Sign-Up Failed", "Pahele sign up kar bhadwe")

# Function to handle forgot password
def forgot_password():
    def reset_password():
        username = username_entry.get()
        new_password = password_entry.get()

        if username in USER_CREDENTIALS:
            USER_CREDENTIALS[username] = new_password
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

# Function to open the homepage
def open_homepage():
    homepage = tk.Toplevel(app)
    homepage.title("Homepage")
    homepage.geometry("600x400")
    homepage.configure(bg="#34495E")

    tk.Label(homepage, text="Welcome to the Homepage!", font=("Helvetica", 18), bg="#34495E", fg="white").pack(pady=20)

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
style = {"font": ("Arial", 12), "bg": "#2980B9", "fg": "white", "relief": "flat", "bd": 0}

login_button = tk.Button(login_frame, text="Login", **style, command=login)
login_button.pack(pady=5)

signup_button = tk.Button(login_frame, text="Sign Up", **style, command=signup)
signup_button.pack(pady=5)

forgot_button = tk.Button(login_frame, text="Forgot Password", **style, command=forgot_password)
forgot_button.pack(pady=5)

# Add rounded corners
for widget in [login_button, signup_button, forgot_button, show_password_button]:
    widget.config(highlightbackground="white", highlightcolor="white", highlightthickness=2, padx=10, pady=5)

# Run the application
app.mainloop()
