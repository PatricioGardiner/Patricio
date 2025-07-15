import sqlite3
import os

# ===================== CREACIÓN DE LA BASE DE DATOS =====================

def crear_base_datos():
    try:
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT
        )
        """)
        conn.commit()
        conn.close()
        print("Base de datos y tabla creadas correctamente.")
    except Exception as e:
        print(" Error al crear la base de datos:", e)

# ===================== FUNCIONES CRUD =====================

def registrar_producto(nombre, descripcion, cantidad, precio, categoria):
    try:
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria) VALUES (?, ?, ?, ?, ?)",
                    (nombre, descripcion, cantidad, precio, categoria))
        conn.commit()
        conn.close()
        print(f"Producto '{nombre}' registrado con éxito.")
    except Exception as e:
        print("Error al registrar producto:", e)

def mostrar_productos():
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    
    if productos:
        print("\n Productos registrados:")
        for producto in productos:
            print(producto)
    else:
        print("\n No hay productos registrados.")

def actualizar_producto(id_producto, nombre, descripcion, cantidad, precio, categoria):
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE productos 
    SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
    WHERE id = ?
    """, (nombre, descripcion, cantidad, precio, categoria, id_producto))
    conn.commit()
    conn.close()
    print("Producto actualizado.")

def eliminar_producto(id_producto):
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
    conn.commit()
    conn.close()
    print("Producto eliminado.")

def buscar_producto(id_producto):
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
    producto = cursor.fetchone()
    conn.close()
    
    if producto:
        print("\n Producto encontrado:")
        print(producto)
    else:
        print(" No se encontró un producto con ese ID.")

def reporte_bajo_stock(limite):
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE cantidad <= ?", (limite,))
    productos = cursor.fetchall()
    conn.close()

    print(f"\n Productos con cantidad menor o igual a {limite}:")
    if productos:
        for producto in productos:
            print(producto)
    else:
        print("Todos los productos tienen suficiente stock.")

# ===================== MENÚ PRINCIPAL =====================

def menu():
    while True:
        print("\n=====  Menú de Inventario - Carnicería =====")
        print("1. Registrar producto")
        print("2. Mostrar productos")
        print("3. Actualizar producto")
        print("4. Eliminar producto")
        print("5. Buscar producto por ID")
        print("6. Reporte de bajo stock")
        print("0. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            nombre = input("Nombre: ")
            descripcion = input("Descripción: ")
            cantidad = int(input("Cantidad disponible: "))
            precio = float(input("Precio ($): "))
            categoria = input("Categoría: ")
            registrar_producto(nombre, descripcion, cantidad, precio, categoria)
        elif opcion == "2":
            mostrar_productos()
        elif opcion == "3":
            id_producto = int(input("ID del producto a actualizar: "))
            nombre = input("Nuevo nombre: ")
            descripcion = input("Nueva descripción: ")
            cantidad = int(input("Nueva cantidad: "))
            precio = float(input("Nuevo precio: "))
            categoria = input("Nueva categoría: ")
            actualizar_producto(id_producto, nombre, descripcion, cantidad, precio, categoria)
        elif opcion == "4":
            id_producto = int(input("ID del producto a eliminar: "))
            eliminar_producto(id_producto)
        elif opcion == "5":
            id_producto = int(input("ID del producto a buscar: "))
            buscar_producto(id_producto)
        elif opcion == "6":
            limite = int(input("Mostrar productos con cantidad igual o inferior a: "))
            reporte_bajo_stock(limite)
        elif opcion == "0":
            print("Saliendo del programa...")
            break
        else:
            print(" Opción no válida. Intente nuevamente.")

# ===================== EJECUCIÓN =====================

if __name__ == "__main__":
    crear_base_datos()

    # Verificar si ya hay productos registrados
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM productos")
    cantidad_productos = cursor.fetchone()[0]
    conn.close()

    if cantidad_productos == 0:
        registrar_producto("Milanesas de carne", "Carne vacuna empanada", 10, 8000.0, "Vacuno")
        registrar_producto("Milanesa de pollo", "Pechuga empanada", 15, 7000.0, "Aves")
        registrar_producto("Milanesa de cerdo", "Cerdo empanado", 20, 6000.0, "Cerdo")
        print(" Productos iniciales cargados.")

    menu()