import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

limiting_reactant_label = None
tab_results = None

def get_input(label_text, var, callback):
    input_window = tk.Toplevel(root)
    label = tk.Label(input_window, text=label_text)
    label.pack()

    entry = tk.Entry(input_window, textvariable=var)
    entry.pack()
    

    ok_button = tk.Button(input_window, text="OK", command=lambda: callback(entry.get(), input_window))
    ok_button.pack()

def set_a(value, window):
    a_var.set(value)
    window.destroy()
    create_input_tab("Entrez l'espèce chimique b:", b_var, set_b)

def set_b(value, window):
    b_var.set(value)
    window.destroy()
    create_input_tab("Entrez l'espèce chimique c:", c_var, set_c)

def set_c(value, window):
    c_var.set(value)
    window.destroy()
    create_input_tab("Entrez l'espèce chimique d:", d_var, set_d)

def set_d(value, window):
    d_var.set(value)
    window.destroy()
    create_input_tab("Entrez le coefficient A:", A_var, set_A)

def set_A(value, window):
    A_var.set(value)
    window.destroy()
    create_input_tab("Entrez le coefficient B:", B_var, set_B)

def set_B(value, window):
    B_var.set(value)
    window.destroy()
    create_input_tab("Entrez le coefficient C:", C_var, set_C)

def set_C(value, window):
    C_var.set(value)
    window.destroy()
    create_input_tab("Entrez le coefficient D:", D_var, set_D)

def set_D(value, window):
    D_var.set(value)
    window.destroy()
    create_input_tab("Entrez la quantité initiale de l'espèce A:", na_var, set_na)

def set_na(value, window):
    na_var.set(value)
    window.destroy()
    create_input_tab("Entrez la quantité initiale de l'espèce B:", nb_var, set_nb)

def set_nb(value, window):
    nb_var.set(value)
    window.destroy()
    create_tab_selection_tab()

def create_input_tab(label_text, var, callback):

    input_tab = ttk.Frame(tab_control)
    tab_control.add(input_tab, text="Entrez les valeurs")

    label = tk.Label(input_tab, text=label_text)
    label.grid(row=0, column=0, pady=10)

    entry = tk.Entry(input_tab, textvariable=var)
    entry.grid(row=0, column=1, pady=10)
    entry.focus_set()

    def validate_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def on_ok_button_click():
        
        value = entry.get()
        
        if var is a_var or var is b_var or var is c_var or var is d_var:
            callback(value, input_tab)
        elif validate_float(value):
            callback(value, input_tab)
        else:
            error_label.config(text="Veuillez entrer un nombre décimal (float).")

    ok_button = tk.Button(input_tab, text="OK", command=on_ok_button_click)
    ok_button.grid(row=1, column=0, columnspan=2, pady=10)

    entry.bind('<Return>', lambda event=None: on_ok_button_click())

    error_label = tk.Label(input_tab, text="", fg="red")
    error_label.grid(row=2, column=0, columnspan=2)

    input_tab.grid_rowconfigure(0, weight=1)
    input_tab.grid_columnconfigure(0, weight=1)
    input_tab.grid(row=0, column=0, sticky="nsew", padx=50, pady=50)

def create_tab_selection_tab():
    tab_selection_tab = ttk.Frame(tab_control)
    tab_control.add(tab_selection_tab, text="Sélectionnez l'onglet")

    label = tk.Label(tab_selection_tab, text="Choisissez l'onglet que vous souhaitez afficher:")
    label.pack(pady=20)
    results_button = tk.Button(tab_selection_tab, text="Afficher le résultat et la representation", command=create_volumetric_flask_tab)
    root.bind('<Return>', lambda event=None: create_volumetric_flask_tab())

    results_button.pack(pady=10)

spam_la = 0

def create_volumetric_flask_tab():
    
    global spam_la
    if spam_la == 1:
        return False
    create_result_tab()
    create_avance_tab()
    image_frame = ImageDisplayFrame(tab_control)
    image_frame.pack()
    tab_control.add(image_frame, text="Representation de l'équation")
    tab_control.bind("<<NotebookTabChanged>>", on_tab_change)
    spam_la += 1
    

class ImageDisplayFrame(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.image_folder = "images"
        self.image_paths = [os.path.join(self.image_folder, f"phy_{i + 1}.png") for i in range(8)]
        self.current_image_index = 0

        self.label = tk.Label(self, highlightthickness=0)
        self.label.pack()

        self.load_image()

        self.after(1000, self.change_image)

    def load_image(self):
        image_path = self.image_paths[self.current_image_index]
        self.image = Image.open(image_path)
        self.tk_image = ImageTk.PhotoImage(self.image)

        self.label.config(image=self.tk_image)

    def change_image(self):

        self.current_image_index = (self.current_image_index + 1) % len(self.image_paths)


        self.load_image()


        if self.current_image_index >= 1:
            self.add_annotation(f"{A_var.get()} {a_var.get()}", 45, 350)
        if self.current_image_index >= 3:
            self.add_annotation(f"{B_var.get()} {b_var.get()}", 230, 350)
        if self.current_image_index >= 5:
            self.add_annotation(f"{C_var.get()} {c_var.get()}", 485, 350)
        if self.current_image_index == 7:
            self.add_annotation(f"{D_var.get()} {d_var.get()}", 675, 350)


        if self.current_image_index == 7:

            self.after(15000, self.change_image)
        else:

            self.after(1000, self.change_image)

    def add_annotation(self, text, x, y):

        annotation = tk.Label(
            self.label,
            text=text,
            font=("Arial", 22),
            fg="black",
            padx=5,
            pady=5,
            bg = "white"
        )
        annotation.place(x=x, y=y)

def on_tab_change(event):
    selected_tab = event.widget.select()
    tab_text = event.widget.tab(selected_tab, "text")

    if tab_text == "Representation de l'équation":
        create_volumetric_flask_tab()


def calculate(result_label, a_var, b_var, c_var, d_var, A_var, B_var, C_var, D_var, na_var, nb_var):
    global xmax
    a = a_var.get()
    b = b_var.get()
    c = c_var.get()
    d = d_var.get()

    A = float(A_var.get())
    B = float(B_var.get())
    C = float(C_var.get())
    D = float(D_var.get())

    na = float(na_var.get())
    nb = float(nb_var.get())




    if (na / A) < (nb / B):
        xmax = na/A
        additional_text = f"L'espèce {a} est le réactif limitant"
    elif (na / A) > (nb / B):
        xmax = nb/B
        additional_text = f"L'espèce {b} est le réactif limitant"
    else:
        xmax = na/A
        additional_text = "Les réactifs ont été introduits dans les proportions stœchiométriques"
        

    naf = na - (A * xmax)
    nbf = nb - (B * xmax)
    ncf = (C * xmax)
    ndf = (D * xmax)

    result_label.config(text=f"{additional_text}\n"
                             f"l'équation équilibrée est : {A_var.get()}{a_var.get()} + {B_var.get()}{b_var.get()} --> {C_var.get()}{c_var.get()} + {D_var.get()}{d_var.get()}\n"
                             f"A l'état final, la quantité de matière de l'espèce {a_var.get()} vaut : {abs(naf)} mol\n"
                             f"A l'état final, la quantité de matière de l'espèce {b_var.get()} vaut : {abs(nbf)} mol\n"
                             f"A l'état final, la quantité de matière de l'espèce {c_var.get()} vaut : {abs(ncf)} mol\n"
                             f"A l'état final, la quantité de matière de l'espèce {d_var.get()} vaut : {abs(ndf)} mol\n"
                             f"xmax = {xmax}")

    return result_label, additional_text

def create_result_tab():
    global tab_results, limiting_reactant_label
    tab_results = ttk.Frame(tab_control)
    tab_control.add(tab_results, text="Résultats")
    
    equation_label = tk.Label(tab_results, text="")
    equation_label.grid(row=0, column=0, columnspan=2)

    limiting_reactant_label = tk.Label(tab_results, text="")
    limiting_reactant_label.grid(row=1, column=0, columnspan=2)

    result_label = tk.Label(tab_results, text="")
    result_label.grid(row=2, column=0, columnspan=2)

    result_tab_label = tk.Label(tab_results, text="")
    result_tab_label.grid(row=3, column=0, columnspan=2)

    result_label, additional_text = calculate(result_label, a_var, b_var, c_var, d_var, A_var, B_var, C_var, D_var, na_var, nb_var)

import tkinter as tk
from tkinter import ttk

def create_avance_tab():
    table_frame = ttk.Frame(tab_control)
    tab_control.add(table_frame, text="Tableau d'avancement")

    table_data = [
        ["Equation","", f"{A_var.get()} {a_var.get()} + {B_var.get()} {b_var.get()} → {C_var.get()}{c_var.get()} + {D_var.get()} {d_var.get()}"],
        ["Etat", "Avancement", "Quantités de matiere (mol)"],
        ["Initial", "0", f"{na_var.get()}", f"{nb_var.get()}", "0", "0"],
        ["En Cours", "x", f"{na_var.get()} - {A_var.get()}x", f"{nb_var.get()} - {B_var.get()}x", f"{C_var.get()}x", f"{D_var.get()}x"],
        ["Final", "Xmax", f"{na_var.get()} - {A_var.get()} xmax", f"{nb_var.get()} - {B_var.get()} xmax", f"{C_var.get()} xmax", f"{D_var.get()} xmax"]
    ]

    for i, row in enumerate(table_data):
        for j, cell_data in enumerate(row):
            cell_style = "height: 23px" if i in [0, 1, 4] else "height: 20px"
            if cell_data != "":
                label = tk.Label(table_frame, text=cell_data, borderwidth=1, relief="solid", padx=5, pady=5, height=1, width=20, anchor="center")
                label.grid(row=i, column=j, sticky="nsew")
                if i == 0 and cell_data == "Equation":
                    label.grid(columnspan=2)
                elif i == 0 and j == 2:
                    label.grid(columnspan=4)
                elif i == 1 and cell_data == "Quantités de matiere (mol)":
                    label.grid(columnspan=4)

    for i in range(len(table_data)):
        table_frame.grid_rowconfigure(i, weight=1)

    for j in range(len(table_data[0])):
        table_frame.grid_columnconfigure(j, weight=1)




root = tk.Tk()
root.title("Réaction Chimique")

tab_control = ttk.Notebook(root)


a_var = tk.StringVar()
b_var = tk.StringVar()
c_var = tk.StringVar()
d_var = tk.StringVar()
A_var = tk.StringVar()
B_var = tk.StringVar()
C_var = tk.StringVar()
D_var = tk.StringVar()
na_var = tk.StringVar()
nb_var = tk.StringVar()
root.geometry("800x500+330+190")
create_input_tab("Entrez l'espèce chimique a:", a_var, set_a)

tab_control.pack(expand=1, fill="both")

root.mainloop()
