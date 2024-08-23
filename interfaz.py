import os
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk

# Importar los módulos
import barras_cont
import abdominales_cont
import correr_cont

class RoundedButton(tk.Canvas):
    def __init__(self, parent, width, height, cornerradius, padding, color, text='', command=None):
        tk.Canvas.__init__(self, parent, borderwidth=0, 
            relief="flat", highlightthickness=0, bg=parent["bg"])
        self.command = command

        if cornerradius > 0.5*width:
            print("Error: cornerradius is greater than width.")
            return None

        if cornerradius > 0.5*height:
            print("Error: cornerradius is greater than height.")
            return None

        rad = 2*cornerradius
        def shape():
            self.create_polygon((padding,height-cornerradius-padding,padding,cornerradius+padding,padding+cornerradius,padding,width-padding-cornerradius,padding,width-padding,cornerradius+padding,width-padding,height-cornerradius-padding,width-padding-cornerradius,height-padding,padding+cornerradius,height-padding), fill=color, outline=color)
            self.create_arc((padding,padding+rad,padding+rad,padding), start=90, extent=90, fill=color, outline=color)
            self.create_arc((width-padding-rad,padding,width-padding,padding+rad), start=0, extent=90, fill=color, outline=color)
            self.create_arc((width-padding,height-rad-padding,width-padding-rad,height-padding), start=270, extent=90, fill=color, outline=color)
            self.create_arc((padding,height-padding-rad,padding+rad,height-padding), start=180, extent=90, fill=color, outline=color)

        shape()
        (x0,y0,x1,y1)  = self.bbox("all")
        width = (x1-x0)
        height = (y1-y0)
        self.configure(width=width, height=height)
        self.create_text(width/2, height/2, text=text, fill='white', font=("Arial", 12, "bold"))

        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _on_press(self, event):
        self.configure(relief="sunken")

    def _on_release(self, event):
        self.configure(relief="raised")
        if self.command is not None:
            self.command()

def show_modal(full_name):
    print(f"Nombre completo en show_modal: {full_name}")  
    modal_window = tk.Toplevel(root)
    modal_window.title("Selección de Ejercicio")

    def option1():
        print(f"Nombre completo en option1: {full_name}")  
        camera_index = simpledialog.askinteger("Selección de cámara", "Ingrese el índice de la cámara (0 para interna, 1 para externa):", minvalue=0, maxvalue=1)
        correr_cont.run_correr_cont(full_name, camera_index)

    def option2():
        camera_index = simpledialog.askinteger("Selección de cámara", "Ingrese el índice de la cámara (0 para interna, 1 para externa):", minvalue=0, maxvalue=1)
        barras_cont.run_barras_cont(full_name, camera_index)

    def option3():
        camera_index = simpledialog.askinteger("Selección de cámara", "Ingrese el índice de la cámara (0 para interna, 1 para externa):", minvalue=0, maxvalue=1)
        abdominales_cont.run_abdominales_cont(full_name, camera_index)

    # Obtén la ruta base del ejecutable
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))

    # Cargar las imágenes de los iconos con rutas relativas
    icon1_path = os.path.join(base_path, 'IDA_Y_VUELTA.png')
    icon2_path = os.path.join(base_path, 'Dom.png')
    icon3_path = os.path.join(base_path, 'Abd.png')

    # Abrir y redimensionar las imágenes
    image1 = Image.open(icon1_path).resize((100, 100))
    icon1 = ImageTk.PhotoImage(image1)

    image2 = Image.open(icon2_path).resize((100, 100))
    icon2 = ImageTk.PhotoImage(image2)

    image3 = Image.open(icon3_path).resize((100, 100))
    icon3 = ImageTk.PhotoImage(image3)

    # Crear botones con los iconos
    button1 = tk.Button(modal_window, image=icon1, command=option1)
    button1.grid(row=0, column=0, padx=10, pady=10)

    button2 = tk.Button(modal_window, image=icon2, command=option2)
    button2.grid(row=0, column=1, padx=10, pady=10)

    button3 = tk.Button(modal_window, image=icon3, command=option3)
    button3.grid(row=0, column=2, padx=10, pady=10)

    modal_window.grab_set()

    # Ejecutar el administrador de ventanas de Tkinter (mainloop())
    modal_window.mainloop()

def login():
    username = username_entry.get()
    password = password_entry.get()

    if os.path.exists(f"usuarios/{username}"):
        with open(f"usuarios/{username}/info.txt", "r") as file:
            saved_password = file.readline().strip()
            full_name = file.readline().strip() 

        if saved_password == password:
            messagebox.showinfo("Login", "¡Bienvenido!")
            show_modal(full_name)
        else:
            messagebox.showerror("Error", "Contraseña incorrecta")
    else:
        messagebox.showerror("Error", "Usuario no encontrado")

def registrar():
    username = new_username_entry.get()
    password = new_password_entry.get()
    full_name = full_name_entry.get()
    user_id = id_entry.get()

    if os.path.exists(f"usuarios/{username}"):
        messagebox.showerror("Error", "Usuario ya registrado. Intente con otro nombre de usuario.")
    else:
        os.makedirs(f"usuarios/{username}")
        with open(f"usuarios/{username}/info.txt", "w") as file:
            file.write(f"{password}\n{full_name}\n{user_id}")

        messagebox.showinfo("Registro", "¡Usuario registrado con éxito!")

def salir():
    root.destroy()

# Crear la ventana principal
root = tk.Tk()
root.title(" ")
root.geometry("400x500")
root.configure(bg='beige')

def show_login_screen():
    for widget in root.winfo_children():
        widget.destroy()

    # Frame principal
    main_frame = tk.Frame(root, bg='beige', padx=20, pady=20)
    main_frame.place(relx=0.5, rely=0.5, anchor='center')

    # Título
    title_label = tk.Label(main_frame, text="Inicio de sesion", font=("Arial", 18, "bold"), bg='beige', fg='black')
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

    # Login
    username_label = tk.Label(main_frame, text="Usuario:", bg='beige', fg='black')
    username_label.grid(row=1, column=0, sticky="e")
    global username_entry
    username_entry = tk.Entry(main_frame)
    username_entry.grid(row=1, column=1, pady=5)

    password_label = tk.Label(main_frame, text="Contraseña:", bg='beige', fg='black')
    password_label.grid(row=2, column=0, sticky="e")
    global password_entry
    password_entry = tk.Entry(main_frame, show="*")
    password_entry.grid(row=2, column=1, pady=5)

    login_button = RoundedButton(main_frame, 150, 30, 10, 2, "#FF1493", text="Iniciar sesión", command=login)
    login_button.grid(row=3, column=0, columnspan=2, pady=10)

    register_label = tk.Label(main_frame, text="¿No tienes cuenta?", bg='beige', fg='black')
    register_label.grid(row=4, column=0, columnspan=2)

    create_account_button = tk.Button(main_frame, text="Crear cuenta", command=show_register_screen, bg='beige', fg='#FF1493', bd=0)
    create_account_button.grid(row=5, column=0, columnspan=2)

    exit_button = tk.Button(main_frame, text="Salir", command=salir, bg='beige', fg='#FF1493', bd=0)
    exit_button.grid(row=6, column=0, columnspan=2)

def show_register_screen():
    for widget in root.winfo_children():
        widget.destroy()

    # Frame principal
    main_frame = tk.Frame(root, bg='beige', padx=20, pady=20)
    main_frame.place(relx=0.5, rely=0.5, anchor='center')

    # Título
    title_label = tk.Label(main_frame, text="Crear Cuenta", font=("Arial", 18, "bold"), bg='beige', fg='black')
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

    # Registro
    new_username_label = tk.Label(main_frame, text="Nuevo usuario:", bg='beige', fg='black')
    new_username_label.grid(row=1, column=0, sticky="e")
    global new_username_entry
    new_username_entry = tk.Entry(main_frame)
    new_username_entry.grid(row=1, column=1, pady=5)

    new_password_label = tk.Label(main_frame, text="Nueva contraseña:", bg='beige', fg='black')
    new_password_label.grid(row=2, column=0, sticky="e")
    global new_password_entry
    new_password_entry = tk.Entry(main_frame, show="*")
    new_password_entry.grid(row=2, column=1, pady=5)

    full_name_label = tk.Label(main_frame, text="Nombre completo:", bg='beige', fg='black')
    full_name_label.grid(row=3, column=0, sticky="e")
    global full_name_entry
    full_name_entry = tk.Entry(main_frame)
    full_name_entry.grid(row=3, column=1, pady=5)

    id_label = tk.Label(main_frame, text="C.C.:", bg='beige', fg='black')
    id_label.grid(row=4, column=0, sticky="e")
    global id_entry
    id_entry = tk.Entry(main_frame)
    id_entry.grid(row=4, column=1, pady=5)

    register_button = RoundedButton(main_frame, 150, 30, 10, 2, "#FF1493", text="Registrar", command=registrar)
    register_button.grid(row=5, column=0, columnspan=2, pady=10)

    login_label = tk.Label(main_frame, text="¿Ya tienes cuenta?", bg='beige', fg='black')
    login_label.grid(row=6, column=0, columnspan=2)

    login_button = tk.Button(main_frame, text="Iniciar sesión", command=show_login_screen, bg='beige', fg='#FF1493', bd=0)
    login_button.grid(row=7, column=0, columnspan=2)

    exit_button = tk.Button(main_frame, text="Salir", command=salir, bg='beige', fg='#FF1493', bd=0)
    exit_button.grid(row=8, column=0, columnspan=2)

# Mostrar la pantalla de inicio de sesión al iniciar la aplicación
show_login_screen()

root.mainloop()
