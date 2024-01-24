import tkinter as tk

def mi_funcion(parametro):
    # Esta es tu función, puedes modificarla según tus necesidades
    return f"Hola, {parametro}!"

def actualizar_etiqueta():
    parametro = entrada_texto.get()
    resultado = mi_funcion(parametro)
    etiqueta.config(text=resultado)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Interfaz de Usuario Python")

# Crear caja de texto para ingresar el parámetro
entrada_texto = tk.Entry(ventana, width=20)
entrada_texto.pack(pady=10)

# Crear etiqueta para mostrar la salida de la función
etiqueta = tk.Label(ventana, text="", font=("Arial", 12))
etiqueta.pack(pady=20)

# Crear botón para activar la función y actualizar la etiqueta
boton_actualizar = tk.Button(ventana, text="Actualizar", command=actualizar_etiqueta)
boton_actualizar.pack()

# Ejecutar el bucle principal
ventana.mainloop()
