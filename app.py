from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from datetime import time
from tkinter.ttk import Button, Label
from tkcalendar import DateEntry

class Usuario:
    def __init__(self, id, nombre, email):
        self.id = id
        self.nombre = nombre
        self.email = email


class Estudiante(Usuario):
    def __init__(self, id, nombre, email):
        super().__init__(id, nombre, email)
        self.solicitudes = []

    def realizar_solicitud(self, profesor, dia, hora):
        solicitud = Solicitud(self, profesor, dia, hora)
        profesor.solicitudes.append(solicitud)
        self.solicitudes.append(solicitud)


class Profesor(Usuario):
    def __init__(self, id, nombre, email):
        super().__init__(id, nombre, email)
        self.solicitudes = []
        self.horarios_disponibles = []


class Administrador(Usuario):
    def __init__(self, id, nombre, email):
        super().__init__(id, nombre, email)
        self.tipo = "Administrador"


class Solicitud:
    def __init__(self, estudiante, profesor, dia, hora):
        self.estudiante = estudiante
        self.profesor = profesor
        self.dia = dia
        self.hora = hora
        self.estado = "Pendiente"
        


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión")
        self.geometry("600x500")

        self.usuarios = {}
        self.usuario_actual = None

        # Contenedor para las vistas
        self.contenedor = tk.Frame(self)
        self.contenedor.pack(fill="both", expand=True)

        # Vista inicial
        self.mostrar_vista(VistaPrincipal, self)

    def mostrar_vista(self, vista, *args):
        """Cambia dinámicamente la vista."""
        for widget in self.contenedor.winfo_children():
            widget.destroy()
        vista(self.contenedor, *args)


class VistaPrincipal(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        tk.Label(self, text="Bienvenido", font=("Arial", 16)).pack(pady=20)
        tk.Button(self, text="Iniciar Sesión", command=lambda: app.mostrar_vista(VistaIniciarSesion, app)).pack(pady=5)
        tk.Button(self, text="Registrar usuarios", command=lambda: app.mostrar_vista(VistaRegistro, app)).pack(pady=5)
        self.pack()


class VistaIniciarSesion(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="Correo Electrónico").pack(pady=5)
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        tk.Label(self, text="Contraseña").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Iniciar Sesión", command=self.iniciar_sesion).pack(pady=10)
        tk.Button(self, text="Regresar", command=lambda: app.mostrar_vista(VistaPrincipal, app)).pack(pady=5)
        self.pack()

    def iniciar_sesion(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if email in self.app.usuarios and self.app.usuarios[email]["contraseña"] == password:
            user = self.app.usuarios[email]["objeto"]
            self.app.usuario_actual = user
            messagebox.showinfo("Éxito", f"Bienvenido, {user.nombre}!")

            if isinstance(user, Estudiante):
                self.app.mostrar_vista(VistaAlumno, self.app, user)
            elif isinstance(user, Profesor):
                self.app.mostrar_vista(VistaProfesor, self.app, user)
            elif isinstance(user, Administrador):
                self.app.mostrar_vista(VistaAdministrador, self.app, user)
        else:
            messagebox.showerror("Error", "Correo o contraseña incorrectos")


class VistaRegistro(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # Lista de IDs válidos (esto podría venir de un archivo o base de datos en un sistema más avanzado)
        self.ids_validos = ["admin123", "estudiante456", "profesor789"]

        tk.Label(self, text="Tipo de Usuario").pack(pady=5)
        self.tipo_usuario = tk.StringVar(value="Estudiante")
        tk.Radiobutton(self, text="Estudiante", variable=self.tipo_usuario, value="Estudiante").pack()
        tk.Radiobutton(self, text="Profesor", variable=self.tipo_usuario, value="Profesor").pack()
        tk.Radiobutton(self, text="Administrador", variable=self.tipo_usuario, value="Administrador").pack()

        tk.Label(self, text="Nombre Completo").pack(pady=5)
        self.nombre_entry = tk.Entry(self)
        self.nombre_entry.pack()

        tk.Label(self, text="Correo Electrónico").pack(pady=5)
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        tk.Label(self, text="Contraseña").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Label(self, text="Confirmar Contraseña").pack(pady=5)
        self.confirm_password_entry = tk.Entry(self, show="*")
        self.confirm_password_entry.pack()

        # Campo ID obligatorio para todos
        tk.Label(self, text="ID de Registro (proporcionado por el Administrador)").pack(pady=5)
        self.id_entry = tk.Entry(self)
        self.id_entry.pack()

        tk.Button(self, text="Registrar", command=self.registrar_usuario).pack(pady=10)
        tk.Button(self, text="Regresar", command=lambda: app.mostrar_vista(VistaPrincipal, app)).pack(pady=5)
        self.pack()

    def registrar_usuario(self):
        tipo_usuario = self.tipo_usuario.get()
        nombre = self.nombre_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        user_id = self.id_entry.get()

        # Verificar campos obligatorios
        if not nombre or not email or not password or not confirm_password or not user_id:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        # Verificar contraseñas coinciden
        if password != confirm_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return

        # Verificar que el correo no esté registrado
        if email in self.app.usuarios:
            messagebox.showerror("Error", "Este correo ya está registrado")
            return

        # Verificar ID de registro
        if user_id not in self.ids_validos:
            messagebox.showerror("Error", "ID de Registro inválido")
            return

        # Eliminar el ID de la lista después del uso (opcional, para evitar reutilización)
        self.ids_validos.remove(user_id)

        # Crear el usuario según el tipo
        id_usuario = len(self.app.usuarios) + 1
        nuevo_usuario = None

        if tipo_usuario == "Estudiante":
            nuevo_usuario = Estudiante(id_usuario, nombre, email)
        elif tipo_usuario == "Profesor":
            nuevo_usuario = Profesor(id_usuario, nombre, email)
        elif tipo_usuario == "Administrador":
            nuevo_usuario = Administrador(id_usuario, nombre, email)

        # Guardar el usuario en el sistema
        self.app.usuarios[email] = {"contraseña": password, "objeto": nuevo_usuario}
        messagebox.showinfo("Éxito", f"{tipo_usuario} registrado exitosamente")
        self.app.mostrar_vista(VistaPrincipal, self.app)

class VistaVerHorarios(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="Horarios Disponibles de los Profesores", font=("Arial", 16)).pack(pady=10)

        for usuario in self.app.usuarios.values():
            if isinstance(usuario["objeto"], Profesor):
                profesor = usuario["objeto"]
                tk.Label(self, text=f"Profesor: {profesor.nombre}", font=("Arial", 12)).pack(pady=5)

                for horario in profesor.horarios_disponibles:
                    tk.Label(self, text=horario.strftime("%H:%M")).pack()

        tk.Button(self, text="Regresar", command=lambda: app.mostrar_vista(VistaAlumno, app, self.app.usuario_actual)).pack(pady=10)
        self.pack()

class VistaAlumno(tk.Frame):
    def __init__(self, parent, app, estudiante):
        super().__init__(parent)
        self.app = app
        self.estudiante = estudiante

        tk.Label(self, text=f"Bienvenido, {estudiante.nombre}", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="Realizar Solicitud", command=lambda: app.mostrar_vista(VistaRealizarSolicitud, app, estudiante)).pack(pady=5)
        tk.Button(self, text="Ver Solicitudes", command=lambda: app.mostrar_vista(VistaVerSolicitudes, app, estudiante)).pack(pady=5)
        tk.Button(self, text="Ver Horarios Disponibles", command=lambda: app.mostrar_vista(VistaVerHorarios, app)).pack(pady=5)
        tk.Button(self, text="Cerrar Sesión", command=lambda: app.mostrar_vista(VistaPrincipal, app)).pack(pady=10)
        self.pack()




class VistaRealizarSolicitud(tk.Frame):
    def __init__(self, parent, app, estudiante):
        super().__init__(parent)
        self.app = app
        self.estudiante = estudiante

        Label(self, text="Seleccione un Profesor", font=("Arial", 12)).pack(pady=5)

        self.profesores = [user for user in self.app.usuarios.values() if isinstance(user["objeto"], Profesor)]
        self.profesores_var = tk.StringVar(value="")

        # Crear el menú de selección de profesores
        self.profesores_menu = tk.OptionMenu(self, self.profesores_var, *[prof["objeto"].nombre for prof in self.profesores])
        self.profesores_menu.pack(pady=5)

        # Selección de fecha usando un calendario
        Label(self, text="Seleccione una Fecha", font=("Arial", 12)).pack(pady=5)
        self.calendario = DateEntry(self, date_pattern="yyyy-mm-dd", width=12, background='darkblue', foreground='white', borderwidth=2)
        self.calendario.pack(pady=5)

        # Botón de mostrar horarios disponibles
        Button(self, text="Mostrar Horarios", command=self.mostrar_horarios).pack(pady=5)
        Button(self, text="Enviar Solicitud", command=self.enviar_solicitud).pack(pady=10)
        Button(self, text="Regresar", command=lambda: app.mostrar_vista(VistaAlumno, app, estudiante)).pack(pady=5)
        self.pack()

    def mostrar_horarios(self):
        """
        Muestra los botones con las horas disponibles del profesor seleccionado.
        """
        profesor_nombre = self.profesores_var.get()
        if not profesor_nombre:
            messagebox.showerror("Error", "Debe seleccionar un profesor")
            return

        fecha_seleccionada = self.calendario.get_date()
        if not fecha_seleccionada:
            messagebox.showerror("Error", "Debe seleccionar una fecha")
            return

        # Encontrar el profesor seleccionado
        profesor = next(prof["objeto"] for prof in self.profesores if prof["objeto"].nombre == profesor_nombre)

        # Crear los botones para las horas disponibles del profesor
        self.frame_horarios = tk.Frame(self)
        self.frame_horarios.pack(pady=5)

        # Limpiar los horarios anteriores si existen
        for widget in self.frame_horarios.winfo_children():
            widget.destroy()

        self.botones_horas = []
        self.seleccion_hora = None  # Guardará la hora seleccionada

        # Filtrar las horas que ya están solicitadas o aceptadas en la fecha seleccionada
        horas_ocupadas = [
            solicitud.hora
            for solicitud in profesor.solicitudes
            if solicitud.estado in ("Pendiente", "Aceptada")
        ]

        # Crear los botones para cada horario disponible que no esté ocupado
        for horario in profesor.horarios_disponibles:
            if horario not in horas_ocupadas:
                boton_hora = tk.Button(
                    self.frame_horarios,
                    text=horario.strftime("%H:%M"),
                    command=lambda h=horario: self.seleccionar_hora(h)
                )
                boton_hora.pack(padx=5, pady=5)
                self.botones_horas.append((horario, boton_hora))

    def seleccionar_hora(self, hora):
        """
        Resalta la hora seleccionada y permite solo una selección a la vez.
        """
        # Restaurar el color original de todos los botones
        for _, boton in self.botones_horas:
            boton.config(bg="SystemButtonFace")  # Color predeterminado del botón

        # Resaltar el botón correspondiente a la hora seleccionada
        boton_seleccionado = next(boton for h, boton in self.botones_horas if h == hora)
        boton_seleccionado.config(bg="lightblue")  # Color de resalte

        # Guardar la hora seleccionada
        self.seleccion_hora = hora

    def enviar_solicitud(self):
        """
        Envía la solicitud al profesor seleccionado con la hora y la fecha elegidos.
        """
        if not self.seleccion_hora:
            messagebox.showerror("Error", "Debe seleccionar una hora disponible")
            return

        fecha = self.calendario.get_date()
        if not fecha:
            messagebox.showerror("Error", "Debe seleccionar una fecha")
            return

        hora = self.seleccion_hora
        profesor_nombre = self.profesores_var.get()

        # Encontrar el profesor seleccionado
        profesor = next(prof["objeto"] for prof in self.profesores if prof["objeto"].nombre == profesor_nombre)

        # Realizar la solicitud
        self.estudiante.realizar_solicitud(profesor, fecha, hora)
        messagebox.showinfo("Éxito", "Solicitud enviada exitosamente")
        self.app.mostrar_vista(VistaAlumno, self.app, self.estudiante)


class VistaVerSolicitudes(tk.Frame):
    def __init__(self, parent, app, estudiante):
        super().__init__(parent)
        self.app = app
        self.estudiante = estudiante

        tk.Label(self, text="Solicitudes Realizadas", font=("Arial", 16)).pack(pady=10)

        # Crear un contenedor para cada solicitud
        for solicitud in self.estudiante.solicitudes:
            estado = solicitud.estado
            dia = solicitud.dia
            profesor = solicitud.profesor.nombre
            hora = solicitud.hora.strftime("%H:%M")

            solicitud_frame = tk.Frame(self)
            solicitud_frame.pack(pady=5)

            # Información de la solicitud
            tk.Label(
                solicitud_frame, 
                text=f"Profesor: {profesor} | Hora: {hora} | Estado: {estado} | Día: {dia}"
            ).pack(side="left")

            # Botón para cancelar solicitud si no ha sido aceptada
            if estado in ("Pendiente", "Rechazada", "Aceptada"):
                tk.Button(
                    solicitud_frame, 
                    text="Cancelar", 
                    command=lambda s=solicitud: self.cancelar_solicitud(s)
                ).pack(side="left")

        tk.Button(self, text="Regresar", command=lambda: app.mostrar_vista(VistaAlumno, app, estudiante)).pack(pady=10)
        self.pack()

    def cancelar_solicitud(self, solicitud):

        solicitud.estado = "Cancelada"
        messagebox.showinfo("Éxito", "Solicitud cancelada exitosamente")
        self.app.mostrar_vista(VistaVerSolicitudes, self.app, self.estudiante)


class VistaProfesor(tk.Frame):
    def __init__(self, parent, app, profesor):
        super().__init__(parent)
        self.app = app
        self.profesor = profesor

        tk.Label(self, text=f"Bienvenido, {profesor.nombre}", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="Gestionar Horarios", command=lambda: app.mostrar_vista(VistaGestionarHorarios, app, profesor)).pack(pady=5)
        tk.Button(self, text="Revisar Solicitudes", command=lambda: app.mostrar_vista(VistaRevisarSolicitudes, app, profesor)).pack(pady=5)
        tk.Button(self, text="Cerrar Sesión", command=lambda: app.mostrar_vista(VistaPrincipal, app)).pack(pady=10)
        self.pack()


class VistaGestionarHorarios(tk.Frame):
    def __init__(self, parent, app, profesor):
        super().__init__(parent)
        self.app = app
        self.profesor = profesor

        tk.Label(self, text="Seleccionar Horarios Disponibles", font=("Arial", 14)).pack(pady=10)

        self.botones_horarios = []
        self.crear_botones_horarios()

        tk.Button(self, text="Regresar", command=lambda: app.mostrar_vista(VistaProfesor, app, profesor)).pack(pady=10)
        self.pack()

    def crear_botones_horarios(self):
        """
        Crea una cuadrícula de botones para seleccionar horarios.
        Los horarios seleccionados se muestran en un color diferente.
        """
        horarios = [
            time(hour, minute)
            for hour in range(8, 20)  # Horarios de 08:00 a 19:00
            for minute in (0, 30)    # Intervalos de 30 minutos
        ]

        frame_horarios = tk.Frame(self)
        frame_horarios.pack(pady=5)

        for idx, horario in enumerate(horarios):
            texto_horario = horario.strftime("%H:%M")
            color = "lightgreen" if horario in self.profesor.horarios_disponibles else "lightgray"

            boton = tk.Button(
                frame_horarios,
                text=texto_horario,
                bg=color,
                width=8,
                command=lambda h=horario: self.toggle_horario(h)
            )
            boton.grid(row=idx // 4, column=idx % 4, padx=5, pady=5)
            self.botones_horarios.append((horario, boton))

    def toggle_horario(self, horario):
        """
        Activa o desactiva un horario como disponible.
        """
        if horario in self.profesor.horarios_disponibles:
            self.profesor.horarios_disponibles.remove(horario)
            self.actualizar_color_boton(horario, "lightgray")
        else:
            self.profesor.horarios_disponibles.append(horario)
            self.actualizar_color_boton(horario, "lightgreen")

    def actualizar_color_boton(self, horario, color):
        """
        Cambia el color del botón correspondiente al horario.
        """
        for h, boton in self.botones_horarios:
            if h == horario:
                boton.config(bg=color)
                break

class VistaRevisarSolicitudes(tk.Frame):
    def __init__(self, parent, app, profesor):
        super().__init__(parent)
        self.app = app
        self.profesor = profesor

        tk.Label(self, text="Solicitudes Recibidas", font=("Arial", 16)).pack(pady=10)

        for solicitud in profesor.solicitudes:
            estudiante = solicitud.estudiante.nombre
            hora = solicitud.hora.strftime("%H:%M")
            estado = solicitud.estado
            dia = solicitud.dia

            # Crear el contenedor para cada solicitud
            solicitud_frame = tk.Frame(self)
            solicitud_frame.pack(pady=5)

            # Información de la solicitud
            tk.Label(
                solicitud_frame, 
                text=f"Estudiante: {estudiante} | Hora: {hora} | Estado: {estado} | Día: {dia}"
            ).pack(side="left")

            # Botones de acciones según el estado de la solicitud
            if estado == "Pendiente":
                tk.Button(
                    solicitud_frame, 
                    text="Aceptar", 
                    command=lambda s=solicitud: self.actualizar_estado(s, "Aceptada")
                ).pack(side="left")
                tk.Button(
                    solicitud_frame, 
                    text="Rechazar", 
                    command=lambda s=solicitud: self.actualizar_estado(s, "Rechazada")
                ).pack(side="left")
            
            # Botón para cancelar la solicitud (disponible para cualquier estado)
            tk.Button(
                solicitud_frame, 
                text="Cancelar", 
                command=lambda s=solicitud: self.cancelar_solicitud(s)
            ).pack(side="left")

        tk.Button(self, text="Regresar", command=lambda: app.mostrar_vista(VistaProfesor, app, profesor)).pack(pady=10)
        self.pack()

    def actualizar_estado(self, solicitud, nuevo_estado):
        """
        Actualiza el estado de la solicitud a "Aceptada" o "Rechazada".
        """
        solicitud.estado = nuevo_estado
        messagebox.showinfo("Éxito", f"Solicitud {nuevo_estado}")
        self.app.mostrar_vista(VistaRevisarSolicitudes, self.app, self.profesor)

    def cancelar_solicitud(self, solicitud):
        """
        Permite al profesor cancelar una solicitud independientemente de su estado actual.
        """
        solicitud.estado = "Cancelada"
        messagebox.showinfo("Éxito", "Solicitud cancelada exitosamente")
        self.app.mostrar_vista(VistaRevisarSolicitudes, self.app, self.profesor)

class VistaAdministrador(tk.Frame):
    def __init__(self, parent, app, administrador):
        super().__init__(parent)
        self.app = app
        self.administrador = administrador

        tk.Label(self, text=f"Bienvenido, {administrador.nombre}", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="Buscar Usuario", command=lambda: app.mostrar_vista(VistaBuscarUsuario, app, administrador)).pack(pady=5)
        tk.Button(self, text="Cerrar Sesión", command=lambda: app.mostrar_vista(VistaPrincipal, app)).pack(pady=10)
        self.pack()

class VistaBuscarUsuario(tk.Frame):
    def __init__(self, parent, app, administrador):
        super().__init__(parent)
        self.app = app
        self.administrador = administrador

        tk.Label(self, text="Buscar Usuario por ID", font=("Arial", 16)).pack(pady=10)

        # Campo de entrada para ID
        tk.Label(self, text="Ingrese el ID del Usuario").pack(pady=5)
        self.id_entry = tk.Entry(self)
        self.id_entry.pack(pady=5)

        # Botón de búsqueda
        tk.Button(self, text="Buscar", command=self.buscar_usuario).pack(pady=10)

        # Etiqueta para mostrar resultados
        self.resultado_label = tk.Label(self, text="", font=("Arial", 12), wraplength=400)
        self.resultado_label.pack(pady=10)

        # Botón para regresar
        tk.Button(self, text="Regresar", command=lambda: app.mostrar_vista(VistaAdministrador, app, administrador)).pack(pady=5)

        self.pack()

    def buscar_usuario(self):
        user_id = self.id_entry.get()

        # Verificar si el ID es válido
        if not user_id.isdigit():
            self.resultado_label.config(text="El ID debe ser un número válido", fg="red")
            return

        user_id = int(user_id)
        usuario_encontrado = None

        # Buscar en los usuarios registrados
        for usuario in self.app.usuarios.values():
            if usuario["objeto"].id == user_id:
                usuario_encontrado = usuario["objeto"]
                break

        # Mostrar el resultado
        if usuario_encontrado:
            tipo_usuario = type(usuario_encontrado).__name__
            self.resultado_label.config(
                text=f"Usuario encontrado:\n\n"
                     f"Nombre: {usuario_encontrado.nombre}\n"
                     f"Email: {usuario_encontrado.email}\n"
                     f"Tipo: {tipo_usuario}",
                fg="green"
            )
        else:
            self.resultado_label.config(text="Usuario no encontrado", fg="red")

if __name__ == "__main__":
    app = App()
    app.mainloop()
