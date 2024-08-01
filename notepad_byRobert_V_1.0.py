import tkinter as tk
import ctypes
import os

from tkinter import messagebox
from tkinter import filedialog

# TODO
#   1.- optimizacion de codigo
#   2.- problemas con la ruta del icono. Como el ejecutable lo puede ejecutar cualquiera?

# Fix bugs
# Global variables
file_path = None
file_name = "Untitled"
saved = True
flag_global = True
flag_set_size = True

# FUNCIONES
# SAVES and OPEN
def save_as():
    global saved
    global file_path
    # Nombre predeterminado del archivo
    default_file_name = "robs.txt"

    file_path_def = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Archivos de texto", "*.txt")], initialfile=default_file_name)
    if file_path_def:
        with open(file_path_def, "w") as file:
            file.write(text.get("1.0", tk.END))
        # file_path global
        file_path = file_path_def
        saved = True
        update_title()
def save_file():
    global saved
    global file_path

    if file_path:
        with open(file_path, "w") as file:
            file.write(text.get("1.0", tk.END))
        saved = True
        update_title()
    else:
        save_as()
def open_file():
    global file_path
    global saved

    file_path = filedialog.askopenfilename(
        filetypes=[("Archivos de texto", "*.txt")])
    if file_path:
        text.delete("1.0", tk.END)
        with open(file_path, "r") as file:
            text.insert(tk.END, file.read())
        file_path = file_path
        saved = True
        update_title()

#
def check_empty():
    content = text.get("1.0", "end-1c")  # Obtiene el contenido del Text desde el inicio hasta el último carácter (sin incluir la nueva línea final)
    if content.strip() == "":
        return True
    else:
        return False

# Funciones para salir y guardar, actualizar titulo, etc.
def exit():
    global saved
    if check_empty():
        saved = True
        exit_notepad()

    if not saved:
        result = messagebox.askyesnocancel(
            title="Notepad", message="Do you want to save changes to " + file_name + "?")
        if result is None:  # Si se presiona "Cancelar", se cancela la salida
            return
        elif result:
            save_file()

    root.quit()

def on_text_change(event):
    global saved
    saved = False
    update_title()
def update_title():
    title = "robs - "
    global file_name
    if file_path:
        file_name = os.path.basename(file_path)
        title += f"{file_name}"
    if not saved:
        title += " *"
    root.title(title)


    pass

# THEME
def dark_theme():
    # Update the background color and text color of the text widget
    text.configure(bg="#282828", fg="#F8F8F8")
    text.config(insertbackground="#F8F8F8")  # Cambiando color del cursor
    # Update the background color of the root window
    root.config(bg="#282828")
    # Update the background color of the menu bar
    menu_bar.config(bg="#282828")

    # options_menu.config(bg="red")
def light_theme():
    # Update the background color and text color of the text widget
    text.configure(bg="#ffffff", fg="#000000")
    text.config(insertbackground="#000000")
    # Update the background color of the root window
    root.config(bg="#000000")

    # Update the background color of the menu bar
    menu_bar.config(bg="#000000")

# Window
def always_top():
    global flag_global

    if flag_global:
        root.attributes("-topmost", True)
        flag_global = False
    else:
        root.attributes("-topmost", False)
        flag_global = True
def set_windows_size():
    global flag_set_size

    if flag_set_size:
        root.geometry("350x300")
        flag_set_size = False
    else:
        root.geometry("750x530")  # Siempre se inicia con ese tamaño
        flag_set_size = True
    
# EXIT
def exit_notepad():
    root.destroy()
    
# Funciones de los ATAJOS
def copy_line(event):
    # Obtener la posición actual del cursor de texto
    cursor_pos = text.index(tk.INSERT)

    # Obtener la línea actual del cursor de texto
    line_start = cursor_pos.split('.')[0] + '.0'
    line_end = cursor_pos.split('.')[0] + '.end'
    current_line = text.get(line_start, line_end)

    # Copiar la línea al portapapeles
    root.clipboard_clear()
    root.clipboard_append(current_line)
def cut_line(event):
    # Copy
    cursor_pos = text.index(tk.INSERT)
    line_start = cursor_pos.split('.')[0] + '.0'
    line_end = cursor_pos.split('.')[0] + '.end'
    current_line = text.get(line_start, line_end)
    root.clipboard_clear()
    root.clipboard_append(current_line)
    # Delete
    current_line = text.index(tk.INSERT).split('.')[0]
    start_pos = current_line + '.0'
    end_pos = current_line + '.end'
    text.delete(start_pos, end_pos)
def delete_line(event):
    # get the current line number
    current_line = text.index(tk.INSERT).split('.')[0]
    # get the start and end positions of the line
    start_pos = current_line + '.0'
    end_pos = current_line + '.end'
    # Borra el texto de la linea
    text.delete(start_pos, end_pos)
def save_shortcut(event):
    save_file()
def redo_action(event):
    try:
        text.edit_redo()
    except tk.TclError:
        pass

# Función para actualizar el tamaño del cuadro de texto
def resize_text(event):
    text.config(width=event.width-10, height=event.height-10)
def on_text_change(event):
    global saved
    saved = False
    update_title()
    # global global_count
    # global_count += 1
    # print("Count:", global_count)

#main():

# Configurar la sensibilidad a la escala de DPI
ctypes.windll.shcore.SetProcessDpiAwareness(1)
# Crear ventana principal
root = tk.Tk()
root.title("robs - Untitled")
#Tamaño inicial del notepad
root.geometry("750x530")  # Siempre se inicia con ese tamaño

ancho_original = root.winfo_width()
alto_original = root.winfo_height()

# Icono
root.iconbitmap('C:\\Users\\juani\\Python\\AppNotepadV1\\resourses\\icono_file_3.ico')

# Crear barra de menú
menu_bar = tk.Menu(root)

# Crear eventos de file y file
file_menu = tk.Menu(menu_bar, tearoff=0)
theme_menu = tk.Menu(menu_bar, tearoff=0)
format_menu = tk.Menu(menu_bar, tearoff=0)

# File
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As...", command=save_as)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_separator()
file_menu.add_command(label="Bye", command=exit_notepad)

# Theme
theme_menu.add_command(label="Dark", command=dark_theme)
theme_menu.add_command(label="Light", command=light_theme)

# Window
format_menu.add_command(label="Always On Top", command=always_top)
format_menu.add_command(label="Resize", command=set_windows_size)

# Formatos de el menu contextual
menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="Theme", menu=theme_menu)
menu_bar.add_cascade(label="Window", menu=format_menu)

# Asignar menú a la ventana principal
root.config(menu=menu_bar)

# Crear cuadro de texto
text = tk.Text(root, padx=8, undo=True, autoseparators=True, maxundo=-1)
#
root.protocol("WM_DELETE_WINDOW", exit)  # Manejar el cierre de ventana
text.bind("<Key>", on_text_change)  # Rastrear los cambios en el texto

# Tipo de fuente del cuadro de texto
text.configure(font=("Consolas", 11))

# Agregar barras de desplazamiento
y_scrollbar = tk.Scrollbar(root, orient="vertical", command=text.yview)
y_scrollbar.pack(side="right", fill="y")
text.configure(yscrollcommand=y_scrollbar.set)
#
text.pack(side="left", fill="both", expand=True)

# Asignar función al evento de cambio de tamaño de la ventana
root.bind("<Configure>", resize_text)
# Eventos de teclas
text.bind('<Control-C>', copy_line)
text.bind('<Control-c>', copy_line)
text.bind('<Control-X>', cut_line)
text.bind('<Control-x>', cut_line)
text.bind("<Control-Shift-K>", delete_line)
text.bind("<Control-Shift-k>", delete_line)
text.bind("<Control-Y>", redo_action)
text.bind("<Control-y>", redo_action)
text.bind("<Shift-Delete>", delete_line)
text.bind("<Control-S>", save_shortcut)
text.bind("<Control-s>", save_shortcut)

root.mainloop()