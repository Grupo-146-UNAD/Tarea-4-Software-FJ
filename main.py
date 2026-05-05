# =========================================================================================================
# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ
# =========================================================================================================
# Versión con Interfaz Gráfica Tkinter - Menú Principal y Gestión Completa
# =========================================================================================================
# Integrantes:  
# Yuris Cerguey Reyes Mandón
# Danna Valeria Uribe Santiago
# Jose Daniel Machado Castellanos
# Diego Alejandro Rocha Manzano
# =========================================================================================================
# Curso: Programación
# =========================================================================================================
# Grupo: 146
# =========================================================================================================
# Tutor: Jhon Harold Patiño Pantoja
# =========================================================================================================
# Fecha: Mayo 2026
# =========================================================================================================
# Universidad Nacional Abierta y a Distancia (UNAD)
# =========================================================================================================

# =========================================================================================================
# MÓDULO MAIN
# =========================================================================================================

# ==================== IMPORTACIONES ======================================================================
# Cada importación trae funcionalidades específicas de Python
import tkinter as tk # Tkinter para interfaz gráfica (alias 'tk' para simplificar)
from tkinter import ttk, messagebox, scrolledtext, simpledialog # Componentes específicos de tkinter
import datetime # Para manejar fechas, horas y realizar operaciones con tiempo

from sistema import SistemaGestionFJ #  Para gestión de clientes, servicios, reservas, verificar disponibilidad y gestionar el backup de datos
from servicio import ReservaSalas, AlquilerEquipos, AsesoriaEspecializada # Para gestión de servicios
from logger import LoggerSistema # Para registro de eventos y errores

import os # Proporciona funciones para interactuar con el sistema operativo (archivos, directorios, rutas, etc.)
import traceback # Proporciona información detallada de errores (stack trace), mostrando la secuencia de llamadas que llevaron a una excepción
import io # Proporciona herramientas para trabajar con flujos de datos en memoria (como capturar texto)
import sys # Proporciona acceso a variables y funciones del intérprete de Python (como la salida estándar)

# =========================================================================================================
# Función que permite Centrar Ventanas en la pantalla, con tamaño automático o fijo 
# =========================================================================================================
def centrar_ventana(ventana, ancho=None, alto=None):
    
    # Si no se especifican ancho y alto, la ventana se ajusta automáticamente a su contenido.
    
    # PARÁMETROS:
        # - ventana: el widget Tk o Toplevel a centrar
        # - ancho: ancho deseado (opcional, si es None usa el ancho del contenido)
        # - alto: alto deseado (opcional, si es None usa el alto del contenido)
    # RETORNA: No retorna valor, modifica la geometría de la ventana
    
    # update_idletasks(): Procesa todas las tareas pendientes y actualiza la ventana
    # Esto es CRÍTICO para obtener las dimensiones correctas después de crear los widgets
    ventana.update_idletasks()
    
    # Si no se especificó un ancho, usar el ancho que la ventana necesita para mostrar todo su contenido
    # winfo_reqwidth(): Retorna el ancho requerido por todos los widgets de la ventana
    if ancho is None:
        ancho = ventana.winfo_reqwidth() + 20 # +20 píxeles de margen para seguridad
        
    # Si no se especificó un alto, usar el alto que la ventana necesita para mostrar todo su contenido
    # winfo_reqheight(): Retorna el alto requerido por todos los widgets de la ventana
    if alto is None:
        alto = ventana.winfo_reqheight() + 20
    
    
    # winfo_screenwidth(): Obtiene el ancho total de la pantalla del monitor
    # winfo_screenheight(): Obtiene el alto total de la pantalla del monitor
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    
    # Calcula la coordenada X para centrar: (ancho_pantalla - ancho_ventana) // 2
    # // es división entera (floor division) para obtener un número entero
    x = (screen_width - ancho) // 2
    
    # Calcula la coordenada Y para centrar: (alto_pantalla - alto_ventana) // 2
    y = (screen_height - alto) // 2
    
    # geometry(): Configura la posición y tamaño de la ventana
    # Formato: f"{ancho}x{alto}+{x}+{y}"  (ej: "500x400+260+140")
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
    
    # update(): Forzar actualización inmediata para que la geometría se aplique
    ventana.update()

# ==================== INTERFAZ GRÁFICA CON TKINTER =======================================================
# Clse AplicacionFJ
# Interfaz gráfica completa usando Tkinter.
# Contiene todas las ventanas, botones, tablas y diálogos.
# =========================================================================================================
class AplicacionFJ:
    
    # CONSTRUCTOR: Inicializa la ventana principal y todos los componentes
    def __init__(self):
        
        # Crear instancia del sistema de gestión
        self.sistema = SistemaGestionFJ()
        
        # Crear ventana principal (root)
        self.root = tk.Tk()
        self.root.title("Software FJ - Sistema Integral de Gestión")
        
        # Configurar colores y estilos (diccionario de colores)
        self.colores = {
            "primary": "#1a237e",      # Azul oscuro principal
            "secondary": "#283593",    # Azul secundario
            "success": "#2e7d32",      # Verde para éxito
            "danger": "#c62828",       # Rojo para peligro/error
            "warning": "#f57c00",      # Naranja para advertencia
            "info": "#1565c0",         # Azul para información
            "light": "#f5f5f5",        # Gris claro
            "dark": "#212121",         # Gris oscuro
            "white": "#ffffff",        # Blanco
            "accent": "#00acc1"        # Turquesa acento
        }
        
        # Llamar a métodos de configuración y creación
        self._configurar_estilos()
        self._crear_menu_principal()
        self._crear_widgets()
        
        # ========== CENTRAR VENTANA PRIMERO ==========
        centrar_ventana(self.root, 1600, 850)
        
        # ========== CARGAR DATOS ==========
        self._actualizar_tablas()
        
        # ========== FORZAR ACTUALIZACIÓN FINAL (sin efecto visual) ==========
        self.root.after_idle(self._forzar_actualizacion_tablas)
        
        # Configurar manejador de cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    # ==================== CONFIGURACIÓN TKINTER ==========================================================
    
    # =====================================================================================================
    # MÉTODO: _configurar_estilo, configura la apariencia visual de todos los widgets
    # =====================================================================================================
    def _configurar_estilos(self):
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # === CONFIGURACIÓN DE BOTONES ===
        self.style.configure('TButton', font=('Segoe UI', 10), padding=5)
        
        # Botón Primario (Azul) - Nuevo, Editar, Refrescar
        self.style.configure('Primary.TButton',
                    background=self.colores["primary"],
                    foreground='white',
                    font=('Segoe UI', 10, 'bold'),
                    padding=8)
        
        self.style.map('Primary.TButton',
                    background=[('active', self.colores["secondary"])],
                    foreground=[('active', 'white')])
        
        # Botón Éxito (Verde) - Guardar, Confirmar, Activar
        self.style.configure('Success.TButton',
                    background=self.colores["success"],
                    foreground='white',
                    font=('Segoe UI', 10, 'bold'),
                    padding=8)
        
        self.style.map('Success.TButton',
                    background=[('active', '#1b5e20')],
                    foreground=[('active', 'white')])
        
        # Botón Peligro (Rojo) - Eliminar, Cancelar
        self.style.configure('Danger.TButton',
                    background=self.colores["danger"],
                    foreground='white',
                    font=('Segoe UI', 10, 'bold'),
                    padding=8)
        
        self.style.map('Danger.TButton',
                    background=[('active', '#b71c1c')],
                    foreground=[('active', 'white')])
        
        # Botón Métodos de Sobrecarga (Naranja)
        self.style.configure('Orange.TButton',
                    background="#f57c00",
                    foreground='white',
                    font=('Segoe UI', 10, 'bold'),
                    padding=8)
    
        self.style.map('Orange.TButton',
                    background=[('active', '#e65100')],
                    foreground=[('active', 'white')])
        
        # === ENCABEZADOS DE TABLA (HOVER VISIBLE) ===
        self.style.configure('Custom.Treeview.Heading', 
                    font=('Segoe UI', 10, 'bold'), 
                    background=self.colores["primary"], 
                    foreground=self.colores["white"], 
                    padding=5)
        
        self.style.map('Custom.Treeview.Heading', 
                    background=[('active', self.colores["secondary"])], 
                    foreground=[('active', self.colores["white"])])
        
        # === TABLA ===
        self.style.configure('Custom.Treeview', font=('Segoe UI', 9), 
                    rowheight=28, 
                    background=self.colores["white"], 
                    fieldbackground=self.colores["white"])
        
        self.style.map('Custom.Treeview', 
                    background=[('selected', '#bbdefb')],  
                    foreground=[('selected', '#1a237e')])
        
        # === COMBOBOX DEL MISMO TAMAÑO QUE ENTRY ===
        self.style.configure('TEntry', padding=5, font=('Segoe UI', 10))
        self.style.configure('TCombobox', padding=5, font=('Segoe UI', 10))
        
        # === ESTILOS GENERALES ===
        self.style.configure('TFrame', 
                    background=self.colores["light"])
        
        self.style.configure('TLabel', 
                    background=self.colores["light"], 
                    font=('Segoe UI', 10))
        
        self.style.configure('TLabelframe', 
                    background=self.colores["light"], 
                    font=('Segoe UI', 10, 'bold'))
        
        self.style.configure('TLabelframe.Label', 
                    background=self.colores["light"], 
                    font=('Segoe UI', 10, 'bold'))
        
        # === PESTAÑAS ===
        self.style.configure('TNotebook', 
                    background=self.colores["light"], 
                    tabmargins=[2, 5, 2, 0])
        
        self.style.configure('TNotebook.Tab', 
                    background=self.colores["secondary"], 
                    foreground='white', 
                    padding=[15, 5], 
                    font=('Segoe UI', 10, 'bold'))
        
        self.style.map('TNotebook.Tab', 
                    background=[('selected', self.colores["primary"])], 
                    foreground=[('selected', 'white')])
    
    # =====================================================================================================
    # MÉTODO: _crear_menu_principal, crea la barra de menú superior
    # =====================================================================================================
    def _crear_menu_principal(self):
        
        menubar = tk.Menu(self.root)  # Crea barra de menú
        self.root.config(menu=menubar)  # Asigna a la ventana
        
        # === MENÚ ARCHIVO ===
        file_menu = tk.Menu(menubar, tearoff=0)  # tearoff=0: no se puede desprender
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Ver Logs", command=self._ver_logs)
        file_menu.add_separator() # Línea separadora visual
        file_menu.add_command(label="Exportar Clientes a CSV", command=self._exportar_clientes)
        file_menu.add_command(label="Exportar Servicios a CSV", command=self._exportar_servicios)
        file_menu.add_command(label="Exportar Reservas a CSV", command=self._exportar_reservas)
        file_menu.add_separator() # Línea separadora visual
        file_menu.add_command(label="Guardar Backup Manual", command=self._guardar_backup_manual)
        file_menu.add_separator() # Línea separadora visual
        file_menu.add_command(label="Ejecutar Validaciones (try/except)", command=self._ejecutar_validaciones_demo)
        file_menu.add_separator() # Línea separadora visual
        file_menu.add_command(label="Salir", command=self._on_closing)
        
        # === MENÚ CLIENTES ===
        clientes_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Clientes", menu=clientes_menu)
        clientes_menu.add_command(label="Registrar Cliente", command=self._abrir_dialogo_cliente)
        clientes_menu.add_separator()
        clientes_menu.add_command(label="Listar Todos", command=lambda: self.notebook.select(0))
        
        # === MENÚ SERVICIOS ===
        servicios_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Servicios", menu=servicios_menu)
        servicios_menu.add_command(label="Agregar Servicio", command=self._abrir_dialogo_servicio)
        servicios_menu.add_separator()
        servicios_menu.add_command(label="Listar Todos", command=lambda: self.notebook.select(1))
        
        # === MENÚ RESERVAS ===
        reservas_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reservas", menu=reservas_menu)
        reservas_menu.add_command(label="Crear Reserva", command=self._abrir_dialogo_reserva)
        reservas_menu.add_separator()
        reservas_menu.add_command(label="Listar Todas", command=lambda: self.notebook.select(2))
        reservas_menu.add_separator()
        reservas_menu.add_command(label="Probar Sobrecarga", command=self._probar_sobrecarga_reserva)
        
        # === MENÚ AYUDA ===
        ayuda_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=ayuda_menu)
        ayuda_menu.add_command(label="Acerca de", command=self._acerca_de)
        ayuda_menu.add_command(label="Estadísticas", command=self._mostrar_estadisticas)
    
    # =====================================================================================================
    # MÉTODO: _crear_widgets, crea todos los elementos visuales de la interfaz
    # =====================================================================================================
    def _crear_widgets(self):
        
        # Frame principal (contenedor)
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # --- HEADER (cabecera con título) ---
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(header_frame, 
                    text="🏢 SOFTWARE FJ", 
                    font=('Segoe UI', 24, 'bold'), 
                    foreground=self.colores["primary"])
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame, 
                    text="Sistema Integral de Gestión de Clientes, Servicios y Reservas", 
                    font=('Segoe UI', 12), 
                    foreground=self.colores["dark"])
        subtitle_label.pack()
        
        # --- PANEL DE ESTADÍSTICAS RÁPIDAS ---
        stats_frame = ttk.Frame(main_frame)
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.stats_clientes = ttk.Label(stats_frame, 
                    text="Clientes: 0", 
                    font=('Segoe UI', 11, 'bold'), 
                    foreground=self.colores["info"])
        self.stats_clientes.pack(side=tk.LEFT, padx=20)
        
        self.stats_servicios = ttk.Label(stats_frame, 
                    text="Servicios: 0", 
                    font=('Segoe UI', 11, 'bold'), 
                    foreground=self.colores["success"])
        self.stats_servicios.pack(side=tk.LEFT, padx=20)
        
        self.stats_reservas = ttk.Label(stats_frame, 
                    text="Reservas: 0", 
                    font=('Segoe UI', 11, 'bold'), 
                    foreground=self.colores["warning"])
        self.stats_reservas.pack(side=tk.LEFT, padx=20)
        
        # --- NOTEBOOK (pestañas principales) ---
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Crear las 3 pestañas
        self._crear_pestana_clientes()
        self._crear_pestana_servicios()
        self._crear_pestana_reservas()
        
        # --- BARRA DE ESTADO ---
        self.status_bar = ttk.Label(main_frame, 
                    text="✅ Sistema listo",
                    relief=tk.SUNKEN, 
                    anchor=tk.W)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
    
    # =====================================================================================================
    # MÉTODO: _crear_pestana_clientes, crea la pestaña de gestión de clientes
    # =====================================================================================================
    def _crear_pestana_clientes(self):
        
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="👥 Clientes")
        
        # --- PANEL DE BOTONES ---
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # Botón Nuevo Cliente
        btn_nuevo = ttk.Button(btn_frame, 
                    text="➕ Nuevo Cliente", 
                    command=self._abrir_dialogo_cliente, 
                    style='Primary.TButton')
        btn_nuevo.pack(side=tk.LEFT, padx=5)
        
        # Botón Editar Cliente
        btn_editar = ttk.Button(btn_frame, 
                    text="✏️ Editar Cliente", 
                    command=self._editar_cliente, 
                    style='Primary.TButton')
        btn_editar.pack(side=tk.LEFT, padx=5)
        
        # Botón Eliminar Cliente
        btn_eliminar = ttk.Button(btn_frame, 
                    text="🗑️ Eliminar Cliente", 
                    command=self._eliminar_cliente,
                    style='Danger.TButton')
        btn_eliminar.pack(side=tk.LEFT, padx=5)
        
        # Botón Activar/Desactivar
        btn_activar = ttk.Button(btn_frame, 
                    text="✅ Activar/Desactivar", 
                    command=self._cambiar_estado_cliente, 
                    style='Success.TButton')
        btn_activar.pack(side=tk.LEFT, padx=5)
        
        # Botón Refrescar (a la derecha)
        btn_refresh = ttk.Button(btn_frame, 
                    text="🔄 Refrescar", 
                    command=self._actualizar_tablas, 
                    style='Primary.TButton')
        btn_refresh.pack(side=tk.RIGHT, padx=5)
        
        # --- CAMPO DE BÚSQUEDA ---
        busqueda_frame = ttk.Frame(tab)
        busqueda_frame.pack(fill=tk.X, pady=5, padx=10)
        
        ttk.Label(busqueda_frame, text="🔍 Buscar:").pack(side=tk.LEFT, padx=5)
        self.busqueda_cliente = ttk.Entry(busqueda_frame, width=40, font=('Segoe UI', 10))
        self.busqueda_cliente.pack(side=tk.LEFT, padx=5)
        self.busqueda_cliente.bind('<KeyRelease>', self._filtrar_clientes)  # Evento: tecla soltada
        
        # --- TABLA DE CLIENTES (Treeview) ---
        table_frame = ttk.LabelFrame(tab, text="Lista de Clientes", padding="10")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        # Definir columnas
        columns = ("ID", "Nombre", "Email", "Teléfono", "Cédula", "Activo")
        self.clientes_tree = ttk.Treeview(table_frame,
                columns=columns, show='headings', height=15, style='Custom.Treeview')
        
        # Configurar encabezados y ancho de columnas
        for col in columns:
            self.clientes_tree.heading(col, text=col)
            width = 120 if col != "Nombre" else 200  # La columna Nombre más ancha
            self.clientes_tree.column(col, width=width)
        
        # Scrollbars para la tabla
        scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL,
                command=self.clientes_tree.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL,
                command=self.clientes_tree.xview)
        self.clientes_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Posicionar elementos
        self.clientes_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        scrollbar_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Configurar expansión
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
    
    # =====================================================================================================
    # MÉTODO: _crear_pestana_servicios, crea la pestaña de gestión de servicios
    # =====================================================================================================
    def _crear_pestana_servicios(self):
        
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🛠️ Servicios")
        
        # Panel de botones
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, pady=10, padx=10)
        
        btn_nuevo = ttk.Button(btn_frame, 
                    text="➕ Nuevo Servicio", 
                    command=self._abrir_dialogo_servicio, 
                    style='Primary.TButton')
        btn_nuevo.pack(side=tk.LEFT, padx=5)
        
        btn_editar = ttk.Button(btn_frame, 
                    text="✏️ Editar Servicio", 
                    command=self._editar_servicio, 
                    style='Primary.TButton')
        btn_editar.pack(side=tk.LEFT, padx=5)
        
        btn_eliminar = ttk.Button(btn_frame, 
                    text="🗑️ Eliminar Servicio", 
                    command=self._eliminar_servicio, 
                    style='Danger.TButton')
        btn_eliminar.pack(side=tk.LEFT, padx=5)
        
        btn_toggle = ttk.Button(btn_frame, 
                    text="🔄 Cambiar Disponibilidad", 
                    command=self._cambiar_disponibilidad_servicio, 
                    style='Success.TButton')
        btn_toggle.pack(side=tk.LEFT, padx=5)
        
        btn_refresh = ttk.Button(btn_frame, 
                    text="🔄 Refrescar", 
                    command=self._actualizar_tablas, 
                    style='Primary.TButton')
        btn_refresh.pack(side=tk.RIGHT, padx=5)
        
        # Campo de búsqueda
        busqueda_frame = ttk.Frame(tab)
        busqueda_frame.pack(fill=tk.X, pady=5, padx=10)
        
        ttk.Label(busqueda_frame, text="🔍 Buscar:").pack(side=tk.LEFT, padx=5)
        self.busqueda_servicio = ttk.Entry(busqueda_frame, width=40, font=('Segoe UI', 10))
        self.busqueda_servicio.pack(side=tk.LEFT, padx=5)
        self.busqueda_servicio.bind('<KeyRelease>', self._filtrar_servicios)
        
        # Tabla de servicios
        table_frame = ttk.LabelFrame(tab, text="Lista de Servicios", padding="10")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        columns = ("ID", "Nombre", "Tipo", "Precio Base", "Disponible", "Detalle Extra")
        self.servicios_tree = ttk.Treeview(table_frame,
                columns=columns, show='headings', height=15, style='Custom.Treeview')
        
        for col in columns:
            self.servicios_tree.heading(col, text=col)
            width = 150 if col == "Detalle Extra" else 120
            self.servicios_tree.column(col, width=width)
        
        scrollbar_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL,
                command=self.servicios_tree.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL,
                command=self.servicios_tree.xview)
        self.servicios_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        self.servicios_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        scrollbar_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
    
    # =====================================================================================================
    # MÉTODO: _crear_pestana_reservas, crea la pestaña de gestión de reservas
    # =====================================================================================================
    def _crear_pestana_reservas(self):
        
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📅 Reservas")
        
        # ========== PANEL DE BOTONES ==========
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # Botón Nueva Reserva
        btn_nueva = ttk.Button(btn_frame, text="📅 Nueva Reserva", 
                command=self._abrir_dialogo_reserva,
                style='Primary.TButton')
        btn_nueva.pack(side=tk.LEFT, padx=5)
        
        # Botón Confirmar
        btn_confirmar = ttk.Button(btn_frame, text="✅ Confirmar", 
                command=self._confirmar_reserva_seleccionada,
                style='Success.TButton')
        btn_confirmar.pack(side=tk.LEFT, padx=5)
        
        # Botón Cancelar
        btn_cancelar = ttk.Button(btn_frame, text="❌ Cancelar", 
                command=self._cancelar_reserva_seleccionada,
                style='Danger.TButton')
        btn_cancelar.pack(side=tk.LEFT, padx=5)
        
        # Botón Completar
        btn_completar = ttk.Button(btn_frame, text="🏁 Completar", 
                command=self._completar_reserva_seleccionada,
                style='Primary.TButton')
        btn_completar.pack(side=tk.LEFT, padx=5)
        
        # Botón Aplicar Descuento
        btn_descuento = ttk.Button(btn_frame, text="💰 Aplicar Descuento", 
                command=self._aplicar_descuento_reserva,
                style='Success.TButton')
        btn_descuento.pack(side=tk.LEFT, padx=5)
        
        # Botón para probar métodos sobrecargados
        btn_sobrecargados = ttk.Button(btn_frame, text="📊 Ver Métodos Sobrecargados", 
                command=self._probar_sobrecarga_reserva_seleccionada,
                style='Orange.TButton')  # ← Cambiado a Orange.TButton
        btn_sobrecargados.pack(side=tk.LEFT, padx=5)
        
        # Botón Refrescar (IMPORTANTE: para forzar actualización)
        btn_refresh = ttk.Button(btn_frame, text="🔄 Refrescar Tabla", 
                command=self._actualizar_tablas,
                style='Primary.TButton')
        btn_refresh.pack(side=tk.RIGHT, padx=5)
        
        # ========== CAMPO DE BÚSQUEDA ==========
        busqueda_frame = ttk.Frame(tab)
        busqueda_frame.pack(fill=tk.X, pady=5, padx=10)
        
        ttk.Label(busqueda_frame, text="🔍 Buscar:").pack(side=tk.LEFT, padx=5)
        self.busqueda_reserva = ttk.Entry(busqueda_frame, width=40, font=('Segoe UI', 10))
        self.busqueda_reserva.pack(side=tk.LEFT, padx=5)
        self.busqueda_reserva.bind('<KeyRelease>', self._filtrar_reservas)
        
        # ========== TABLA DE RESERVAS (CONFIGURACIÓN CORREGIDA) ==========
        table_frame = ttk.LabelFrame(tab, text="Lista de Reservas", padding="10")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        # Títulos de las Columnas de la Tabla
        columnas = [
            "ID", "Cliente", "Servicio", "Duración (h)", "Parámetros Extra",
            "Precio Base", "% Descuento", "Valor Descuento", "Total", "Estado", "Fecha"
        ]
        
        # Crea el Treeview
        self.reservas_tree = ttk.Treeview(
            table_frame, 
            columns=columnas,
            show='headings',  # Muestra solo los encabezados (no la primera columna vacía)
            height=15,
            style='Custom.Treeview'
        )
        
        # CONFIGURAR ENCABEZADOS Y ANCHOS (UNO POR UNO)
        anchos = [60, 180, 180, 90, 280, 120, 100, 120, 120, 110, 150]
        
        for i, col in enumerate(columnas):
            self.reservas_tree.heading(col, text=col)
            self.reservas_tree.column(col, width=anchos[i], minwidth=anchos[i])
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.reservas_tree.yview)
        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.reservas_tree.xview)
        self.reservas_tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        # Posicionar elementos
        self.reservas_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scroll_y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        scroll_x.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Configurar expansión
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # ========== DOBLE CLIC PARA VER DETALLES ==========
        self.reservas_tree.bind('<Double-1>', self._ver_detalles_reserva_doble_clic)
    
    # ==================== MÉTODOS DE FILTRADO ============================================================
    # MÉTODO: _filtrar_clientes, filtra la tabla de clientes
    # mientras el usuario escribe en el campo de búsqueda.
    # Se ejecuta en cada tecla presionada (evento <KeyRelease>)
    # =====================================================================================================
    def _filtrar_clientes(self, event=None):
        
        texto = self.busqueda_cliente.get().lower()  # Obtiene texto en minúsculas para comparación insensible a mayúsculas
        
        # Limpiar tabla (eliminar todos los elementos actuales)
        # get_children(): retorna todos los IDs de los elementos en el Treeview
        for item in self.clientes_tree.get_children():
            self.clientes_tree.delete(item)  # delete(): elimina el elemento con el ID especificado
        
        # Recorrer TODOS los clientes y mostrar solo los que coinciden con el filtro
        for cliente in self.sistema.obtener_clientes():
            # Condición: nombre CONTIENE el texto O email CONTIENE el texto
            # in: operador que verifica si una subcadena existe dentro de una cadena
            if texto in cliente.nombre.lower() or texto in cliente.email.lower():
                # Operador ternario: valor_si_verdadero if condición else valor_si_falso
                estado = "✓ Activo" if cliente.activo else "✗ Inactivo"
                # insert(): agrega un nuevo elemento a la tabla
                # tk.END: inserta al final de la lista
                self.clientes_tree.insert("", tk.END, values=(
                    cliente.id, cliente.nombre, cliente.email, 
                    cliente.telefono, cliente.cedula, estado
                ))
    
    # =====================================================================================================
    # MÉTODO: _filtrar_servicios, filtra la tabla de servicios según el texto de búsqueda
    # =====================================================================================================
    def _filtrar_servicios(self, event=None):
        
        texto = self.busqueda_servicio.get().lower()
        
        # Limpiar tabla
        for item in self.servicios_tree.get_children():
            self.servicios_tree.delete(item)
        
        # Filtrar servicios
        for servicio in self.sistema.obtener_servicios():
            # Verifica si el texto está en el nombre o en el tipo del servicio
            if texto in servicio.nombre.lower() or texto in servicio.tipo.lower():
                disponible = "✓ Sí" if servicio.disponible else "✗ No"
                detalle = ""
                # isinstance(): verifica si un objeto es de una clase específica
                if isinstance(servicio, ReservaSalas):
                    detalle = f"Capacidad: {servicio.capacidad}"
                elif isinstance(servicio, AlquilerEquipos):
                    detalle = f"Tipo: {servicio.tipo_equipo}"
                elif isinstance(servicio, AsesoriaEspecializada):
                    detalle = f"Nivel: {servicio.nivel}"
                
                self.servicios_tree.insert("", tk.END, values=(
                    servicio.id, servicio.nombre, servicio.tipo.upper(),
                    f"${servicio.precio_base:,.0f}", disponible, detalle
                ))
                
    # =====================================================================================================
    # MÉTODO: _filtrar_reservas, filtra la tabla de reservas según el texto de búsqueda
    # =====================================================================================================
    def _filtrar_reservas(self, event=None):
        
        texto = self.busqueda_reserva.get().lower()
        
        for item in self.reservas_tree.get_children():
            self.reservas_tree.delete(item)
        
        for reserva in self.sistema.obtener_reservas():
            info = reserva.obtener_info()  # Obtiene diccionario con la información de la reserva
            # Busca coincidencia en nombre del cliente o nombre del servicio
            if texto in info["cliente"].lower() or texto in info["servicio"].lower():
                self.reservas_tree.insert("", tk.END, values=(
                    info["id"], info["cliente"], info["servicio"],
                    info["duracion"], info["estado"], f"${info['costo_total']:,.0f}", info["fecha"]
                ))
    
    # ==================== MÉTODOS DE ACTUALIZACIÓN =======================================================
    
    # =====================================================================================================
    # MÉTODO: _actualizar_tablas, actualiza todas las tablas con los datos más recientes del sistema
    # =====================================================================================================
    def _actualizar_tablas(self):
        
        # Limpiar filtros
        self.busqueda_cliente.delete(0, tk.END)
        self.busqueda_servicio.delete(0, tk.END)
        self.busqueda_reserva.delete(0, tk.END)
        
        # ========== ACTUALIZAR CLIENTES ==========
        for item in self.clientes_tree.get_children():
            self.clientes_tree.delete(item)
        
        for cliente in self.sistema.obtener_clientes():
            estado = "✓ Activo" if cliente.activo else "✗ Inactivo"
            self.clientes_tree.insert("", tk.END, values=(
                cliente.id, cliente.nombre, cliente.email, 
                cliente.telefono, cliente.cedula, estado
            ))
        
        # ========== ACTUALIZAR SERVICIOS ==========
        for item in self.servicios_tree.get_children():
            self.servicios_tree.delete(item)
        
        for servicio in self.sistema.obtener_servicios():
            disponible = "✓ Sí" if servicio.disponible else "✗ No"
            detalle = ""
            if isinstance(servicio, ReservaSalas):
                detalle = f"Capacidad: {servicio.capacidad}"
            elif isinstance(servicio, AlquilerEquipos):
                detalle = f"Tipo: {servicio.tipo_equipo}"
            elif isinstance(servicio, AsesoriaEspecializada):
                detalle = f"Nivel: {servicio.nivel}"
            
            self.servicios_tree.insert("", tk.END, values=(
                servicio.id, servicio.nombre, servicio.tipo.upper(),
                f"${servicio.precio_base:,.0f}", disponible, detalle
            ))
        
        # ========== ACTUALIZAR RESERVAS ==========
        for item in self.reservas_tree.get_children():
            self.reservas_tree.delete(item)
        
        for reserva in self.sistema.obtener_reservas():
            info = reserva.obtener_info()
            
            # Formatear parámetros extra
            params_display = ""
            if info.get("parametros_extra") and len(info["parametros_extra"]) > 0:
                params_list = []
                for k, v in info["parametros_extra"].items():
                    if isinstance(v, bool):
                        v_str = "Sí" if v else "No"
                    else:
                        v_str = str(v)
                    params_list.append(f"{k}={v_str}")
                params_display = ", ".join(params_list)
            else:
                params_display = "─"
            
            # Formatear valores monetarios
            precio_base_str = f"${info['precio_base']:,.0f}" if info['precio_base'] > 0 else "$0"
            valor_descuento_str = f"${info['valor_descuento']:,.0f}" if info['valor_descuento'] > 0 else "$0"
            total_str = f"${info['costo_total']:,.0f}"
            porcentaje_str = f"{info['porcentaje_descuento']:.0f}%" if info['porcentaje_descuento'] > 0 else "─"
            
            # Estado con emoji
            estado_emoji = {
                "PENDIENTE": "⏳ Pendiente",
                "CONFIRMADA": "✅ Confirmada",
                "CANCELADA": "❌ Cancelada",
                "COMPLETADA": "🏁 Completada"
            }.get(info["estado"], info["estado"])
            
            # Insertar en la tabla
            self.reservas_tree.insert("", tk.END, values=(
                info["id"], info["cliente"], info["servicio"],
                f"{info['duracion']:.1f}", params_display,
                precio_base_str, porcentaje_str, valor_descuento_str,
                total_str, estado_emoji, info["fecha"]
            ))
        
        # ========== FORZAR ACTUALIZACIÓN VISUAL DE LA TABLA ==========
        # Esto evita que la tabla se quede "congelada" al cargar backup
        self.reservas_tree.update_idletasks()  # Procesa eventos pendientes
        self.reservas_tree.see("")             # Hace scroll al inicio
        self.reservas_tree.update()            # Fuerza el redibujado completo
        
        # ========== ACTUALIZAR ESTADÍSTICAS ==========
        self.stats_clientes.config(text=f"Clientes: {len(self.sistema.obtener_clientes())}")
        self.stats_servicios.config(text=f"Servicios: {len(self.sistema.obtener_servicios())}")
        self.stats_reservas.config(text=f"Reservas: {len(self.sistema.obtener_reservas())}")
        self.status_bar.config(text="✅ Datos actualizados correctamente")
        
    # ==================== MÉTODOS DE SELECCIÓN ====================
    
    # =====================================================================================================
    # MÉTODO: _obtener_cliente_seleccionado, Obtiene el ID del cliente seleccionado en la tabla
    # Retorna int - ID del cliente, o None si no hay selección
    # =====================================================================================================
    def _obtener_cliente_seleccionado(self):
        
        # selection(): retorna una tupla con los IDs de los elementos seleccionados
        selection = self.clientes_tree.selection()
        
        # if not selection: verifica si la tupla está vacía (nada seleccionado)
        if not selection:
            # messagebox.showwarning(): muestra un cuadro de diálogo de advertencia
            messagebox.showwarning("Advertencia", "Por favor seleccione un cliente")
            return None
        
        # item(): obtiene el diccionario de datos del elemento seleccionado
        # selection[0] toma el primer elemento de la tupla (el seleccionado)
        item = self.clientes_tree.item(selection[0])
        
        # item['values'] es una tupla con los valores de las columnas
        # [0] retorna el primer valor (que es el ID)
        return item['values'][0]
    
    # =====================================================================================================
    # MÉTODO: _obtener_servicio_seleccionado, obtiene el ID del servicio seleccionado en la tabla
    # Retorna int - ID del servicio, o None si no hay selección
    # =====================================================================================================
    def _obtener_servicio_seleccionado(self):
        
        selection = self.servicios_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione un servicio")
            return None
        item = self.servicios_tree.item(selection[0])
        return item['values'][0]  # El ID es la primera columna
    
    # =====================================================================================================
    # MÉTODO: _obtener_servicio_seleccionado, obtiene el ID de la reserva seleccionada en la tabla
    # Retorna int - ID de la reserva, o None si no hay selección
    # =====================================================================================================
    def _obtener_reserva_seleccionada(self):
        
        selection = self.reservas_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione una reserva")
            return None
        item = self.reservas_tree.item(selection[0])
        return item['values'][0]  # El ID es la primera columna
    
    # ==================== MÉTODOS DE CLIENTES (UI) =======================================================
    # MÉTODO: _abrir_dialogo_cliente, abre un diálogo modal para registrar un nuevo cliente
    # La ventana se ajusta automáticamente a su contenido
    # =====================================================================================================
    def _abrir_dialogo_cliente(self):
        
        # Toplevel(): crea una ventana hija de la ventana principal
        dialog = tk.Toplevel(self.root)
        dialog.title("Registrar Nuevo Cliente")
        dialog.transient(self.root)   # Hace que sea hija de la ventana principal
        dialog.grab_set()             # Modal: bloquea otras ventanas hasta cerrar
        
        # Frame con padding (espacio interno)
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)  # fill=tk.BOTH: expande en ambas direcciones
        
        # Campos del formulario
        # grid(): organiza widgets en una cuadrícula (filas y columnas)
        # sticky=tk.W: alinea al oeste (izquierda)
        # pady=5: padding vertical de 5 píxeles
        ttk.Label(frame, text="Nombre Completo:",
                font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
        entry_nombre = ttk.Entry(frame, width=40,
                font=('Segoe UI', 10))
        entry_nombre.grid(row=0, column=1, pady=5, padx=10)  # padx=10: padding horizontal
        
        ttk.Label(frame, text="Email:",
                font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=5)
        entry_email = ttk.Entry(frame, width=40,
                font=('Segoe UI', 10))
        entry_email.grid(row=1, column=1, pady=5, padx=10)
        
        ttk.Label(frame, text="Teléfono:",
                font=('Segoe UI', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=5)
        entry_telefono = ttk.Entry(frame, width=40,
                font=('Segoe UI', 10))
        entry_telefono.grid(row=2, column=1, pady=5, padx=10)
        
        ttk.Label(frame, text="Cédula:",
                font=('Segoe UI', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=5)
        entry_cedula = ttk.Entry(frame, width=40,
                font=('Segoe UI', 10))
        entry_cedula.grid(row=3, column=1, pady=5, padx=10)
        
        # Botones
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)  # columnspan=2: ocupa 2 columnas
        
        # =================================================================================================
        # FUNCIÓN: guardar, captura los datos del formulario y registra el cliente
        # =================================================================================================
        def guardar():
            
            try:
                # Llama al método del sistema para registrar el cliente
                self.sistema.registrar_cliente(
                    entry_nombre.get(),   # .get(): obtiene el texto del Entry
                    entry_email.get(),
                    entry_telefono.get(),
                    entry_cedula.get()
                )
                self._actualizar_tablas()  # Actualiza las tablas con el nuevo cliente
                messagebox.showinfo("Éxito", "Cliente registrado correctamente")
                dialog.destroy()  # Cierra el diálogo
            except Exception as e:
                # Si hay error, muestra mensaje sin cerrar la ventana
                messagebox.showerror("Error", str(e))
        
        # Botón Guardar (verde) y Cancelar (rojo)
        ttk.Button(btn_frame, text="Guardar",
                command=guardar, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar",
                command=dialog.destroy, style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        
        centrar_ventana(dialog)  # Se ajusta automáticamente al contenido
    
    # =====================================================================================================
    # Abre diálogo para editar cliente seleccionado
    # =====================================================================================================
    def _editar_cliente(self):
        
        id_cliente = self._obtener_cliente_seleccionado()
        if not id_cliente:
            return
        
        # Busca el cliente por su ID
        # next(): retorna el primer elemento que cumple la condición
        cliente = next((c for c in self.sistema.obtener_clientes() if c.id == id_cliente), None)
        if not cliente:
            messagebox.showerror("Error", "Cliente no encontrado")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Editar Cliente - {cliente.nombre}")
        dialog.transient(self.root)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Campos precargados con los datos actuales del cliente
        ttk.Label(frame, text="Nombre Completo:",
                font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
        entry_nombre = ttk.Entry(frame, width=40,
                font=('Segoe UI', 10))
        entry_nombre.insert(0, cliente.nombre)  # insert(): precarga el texto existente
        entry_nombre.grid(row=0, column=1, pady=5, padx=10)
        
        ttk.Label(frame, text="Email:",
                font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=5)
        entry_email = ttk.Entry(frame, width=40,
                font=('Segoe UI', 10))
        entry_email.insert(0, cliente.email)
        entry_email.grid(row=1, column=1, pady=5, padx=10)
        
        ttk.Label(frame, text="Teléfono:",
                font=('Segoe UI', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=5)
        entry_telefono = ttk.Entry(frame, width=40,
                font=('Segoe UI', 10))
        entry_telefono.insert(0, cliente.telefono)
        entry_telefono.grid(row=2, column=1, pady=5, padx=10)
        
        ttk.Label(frame, text="Cédula:",
                font=('Segoe UI', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=5)
        entry_cedula = ttk.Entry(frame, width=40,
                font=('Segoe UI', 10))
        entry_cedula.insert(0, cliente.cedula)
        entry_cedula.grid(row=3, column=1, pady=5, padx=10)
        
        # =================================================================================================
        # FUNCIÓN: guardar, captura los datos del formulario y actualiza el cliente
        # =================================================================================================
        def guardar():
            try:
                self.sistema.actualizar_cliente(
                    id_cliente,
                    entry_nombre.get(),
                    entry_email.get(),
                    entry_telefono.get(),
                    entry_cedula.get()
                )
                self._actualizar_tablas()
                messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="Guardar",
                command=guardar, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar",
                command=dialog.destroy, style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        
        centrar_ventana(dialog)  # Se ajusta automáticamente al contenido
    
    # =====================================================================================================
    # Elimina el cliente seleccionado (con confirmación)
    # =====================================================================================================
    def _eliminar_cliente(self):
        
        id_cliente = self._obtener_cliente_seleccionado()
        if not id_cliente:
            return
        
        # askyesno(): muestra un cuadro de diálogo con Sí/No y retorna True/False
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cliente?"):
            try:
                self.sistema.eliminar_cliente(id_cliente)
                self._actualizar_tablas()
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    # =====================================================================================================
    # Cambia estado activo/inactivo del cliente seleccionado
    # =====================================================================================================
    def _cambiar_estado_cliente(self):
        
        id_cliente = self._obtener_cliente_seleccionado()
        if not id_cliente:
            return
        
        cliente = next((c for c in self.sistema.obtener_clientes() if c.id == id_cliente), None)
        if not cliente:
            return
        
        # Invierte el estado actual (not: operador de negación lógica)
        nuevo_estado = not cliente.activo
        estado_texto = "activar" if nuevo_estado else "desactivar"
        
        if messagebox.askyesno("Confirmar", f"¿Desea {estado_texto} este cliente?"):
            try:
                self.sistema.cambiar_estado_cliente(id_cliente, nuevo_estado)
                self._actualizar_tablas()
                messagebox.showinfo("Éxito", f"Cliente {estado_texto}do correctamente")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    # ==================== MÉTODOS DE SERVICIOS (UI) ====================
    
    # =====================================================================================================
    # MÉTODO: _abrir_dialogo_servicio, abre diálogo para agregar nuevo servicio - VENTANA AJUSTABLE
    # =====================================================================================================
    def _abrir_dialogo_servicio(self):
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Agregar Nuevo Servicio")
        dialog.transient(self.root)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Tipo de servicio (Combobox con opciones desplegables)
        ttk.Label(frame, text="Tipo de Servicio:", 
                font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
        combo_tipo = ttk.Combobox(frame, values=["sala", "equipo", "asesoria"], width=44)
        combo_tipo.grid(row=0, column=1, pady=5, padx=10)
        
        ttk.Label(frame, text="Nombre:", font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=5)
        entry_nombre = ttk.Entry(frame, width=40, font=('Segoe UI', 10))
        entry_nombre.grid(row=1, column=1, pady=5, padx=10)
        
        ttk.Label(frame, text="Precio Base:", font=('Segoe UI', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=5)
        entry_precio = ttk.Entry(frame, width=40, font=('Segoe UI', 10))
        entry_precio.grid(row=2, column=1, pady=5, padx=10)
        
        ttk.Label(frame, text="Parámetro Extra:", font=('Segoe UI', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=5)
        entry_extra = ttk.Entry(frame, width=40, font=('Segoe UI', 10))
        entry_extra.grid(row=3, column=1, pady=5, padx=10)
        
        # Mensaje informativo (wraplength: ajusta el texto a 350 píxeles)
        info_label = ttk.Label(frame, 
                text="💡 Sala: capacidad máxima | Equipo: tipo de equipo | Asesoría: nivel (Junior/Senior/Master)",
                foreground="gray", wraplength=350)
        info_label.grid(row=4, column=0, columnspan=2, pady=10)
        
        # =================================================================================================
        # FUNCIÓN: guardar, captura los datos del formulario y registra el tipo de servicio
        # =================================================================================================
        def guardar():
            try:
                tipo = combo_tipo.get()
                nombre = entry_nombre.get()
                precio = float(entry_precio.get())
                extra = entry_extra.get()
                
                # Validar que se haya seleccionado un tipo
                if not tipo:
                    messagebox.showerror("Error", "Debe seleccionar un tipo de servicio")
                    return
                
                # Validar que el nombre no esté vacío
                if not nombre:
                    messagebox.showerror("Error", "Debe ingresar un nombre para el servicio")
                    return
                
                # Conversión del parámetro extra según el tipo de servicio
                if tipo == "sala":
                    # Validar que la capacidad sea un número
                    if not extra:
                        messagebox.showerror("Error", "Debe ingresar la capacidad máxima de la sala")
                        return
                    try:
                        extra = int(extra)
                    except ValueError:
                        messagebox.showerror("Error", "La capacidad debe ser un número entero")
                        return
                elif tipo == "equipo":
                    extra = extra  # Tipo de equipo como string
                    if not extra:
                        messagebox.showerror("Error", "Debe ingresar el tipo de equipo")
                        return
                elif tipo == "asesoria":
                    extra = extra  # Nivel como string
                    if not extra:
                        messagebox.showerror("Error", "Debe ingresar el nivel de experto")
                        return
                else:
                    messagebox.showerror("Error", "Seleccione un tipo de servicio válido")
                    return
                
                # ========== CORRECCIÓN: Verificar si el servicio se creó ==========
                servicio_creado = self.sistema.agregar_servicio(tipo, nombre, precio, extra)
                
                # Si el servicio se creó correctamente (no es None)
                if servicio_creado is not None:
                    self._actualizar_tablas()
                    messagebox.showinfo("Éxito", "Servicio agregado correctamente")
                    dialog.destroy()
                else:
                    # Si el servicio NO se creó, mostrar mensaje de error
                    messagebox.showerror("Error", "No se pudo crear el servicio. Verifique los datos ingresados.")
                
            except ValueError:
                messagebox.showerror("Error", "Precio debe ser un número válido")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="Guardar", command=guardar, 
                style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy,
                style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        
        centrar_ventana(dialog) # Se ajusta automáticamente al contenido
    
    # =====================================================================================================
    # MÉTODO: _editar_servicio, edita el servicio seleccionado - VENTANA AJUSTABLE"""
    # =====================================================================================================
    def _editar_servicio(self):
        
        id_servicio = self._obtener_servicio_seleccionado()
        if not id_servicio:
            return
        
        servicio = next((s for s in self.sistema.obtener_servicios() if s.id == id_servicio), None)
        if not servicio:
            messagebox.showerror("Error", "Servicio no encontrado")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Editar Servicio - {servicio.nombre}")
        dialog.transient(self.root)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Nombre:", font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
        entry_nombre = ttk.Entry(frame, width=40, font=('Segoe UI', 10))
        entry_nombre.insert(0, servicio.nombre)
        entry_nombre.grid(row=0, column=1, pady=5, padx=10)
        
        ttk.Label(frame, text="Precio Base:", font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=5)
        entry_precio = ttk.Entry(frame, width=40, font=('Segoe UI', 10))
        entry_precio.insert(0, str(servicio.precio_base))
        entry_precio.grid(row=1, column=1, pady=5, padx=10)
        
        # =================================================================================================
        # FUNCIÓN: guardar, captura los datos del formulario y actualiza el tipo de servicio
        # =================================================================================================
        def guardar():
            try:
                self.sistema.actualizar_servicio(
                    id_servicio,
                    entry_nombre.get(),
                    float(entry_precio.get())
                )
                self._actualizar_tablas()
                messagebox.showinfo("Éxito", "Servicio actualizado correctamente")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="Guardar", command=guardar, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy, style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        
        centrar_ventana(dialog) # Se ajusta automáticamente al contenido
    
    # =====================================================================================================
    # MÉTODO: _eliminar_servicio, elimina el servicio seleccionado (con confirmación)
    # (activo/inactivo)
    # =====================================================================================================
    def _eliminar_servicio(self):
        
        id_servicio = self._obtener_servicio_seleccionado()
        if not id_servicio:
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este servicio?"):
            try:
                self.sistema.eliminar_servicio(id_servicio)
                self._actualizar_tablas()
                messagebox.showinfo("Éxito", "Servicio eliminado correctamente")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    # =====================================================================================================
    # MÉTODO: _cambiar_disponibilidad_servicio, cambia disponibilidad del servicio seleccionado
    # (activo/inactivo)
    # =====================================================================================================
    def _cambiar_disponibilidad_servicio(self):
        
        id_servicio = self._obtener_servicio_seleccionado()
        if not id_servicio:
            return
        
        try:
            self.sistema.cambiar_disponibilidad_servicio(id_servicio)
            self._actualizar_tablas()
            messagebox.showinfo("Éxito", "Disponibilidad cambiada correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # ==================== MÉTODOS DE RESERVAS (UI) =======================================================
    
    # =====================================================================================================
    # MÉTODO: _abrir_dialogo_reserva, abre un diálogo modal para que el usuario cree una nueva reserva
    #   - Campos dinámicos según el tipo de servicio (sala, equipo, asesoría)
    #   - Captura parámetros reales ingresados por el usuario
    #   - Muestra ejemplos específicos para cada tipo de servicio
    # =====================================================================================================
    def _abrir_dialogo_reserva(self):
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Crear Nueva Reserva")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # ========== FRAME PRINCIPAL ==========
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # ========== SELECCIÓN DE CLIENTE ==========
        ttk.Label(frame, text="Cliente:", font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
        combo_cliente = ttk.Combobox(frame, width=40)
        clientes = [f"{c.id} - {c.nombre}" for c in self.sistema.obtener_clientes() if c.activo]
        combo_cliente['values'] = clientes
        combo_cliente.grid(row=0, column=1, pady=5, padx=10, sticky=tk.W)
        
        # ========== SELECCIÓN DE SERVICIO ==========
        ttk.Label(frame, text="Servicio:", font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=5)
        combo_servicio = ttk.Combobox(frame, width=40)
        servicios = [f"{s.id} - {s.nombre} ({s.tipo.upper()})" for s in self.sistema.obtener_servicios() if s.disponible]
        combo_servicio['values'] = servicios
        combo_servicio.grid(row=1, column=1, pady=5, padx=10, sticky=tk.W)
        
        # ========== PRECIO BASE DEL SERVICIO ==========
        ttk.Label(frame, text="Precio Base del Servicio:", font=('Segoe UI', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=5)
        precio_base_label = ttk.Label(frame, text="$0 / hora", font=('Segoe UI', 10), foreground="green")
        precio_base_label.grid(row=2, column=1, pady=5, padx=10, sticky=tk.W)
        
        # ========== DURACIÓN ==========
        ttk.Label(frame, text="Duración (horas):", font=('Segoe UI', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=5)
        entry_duracion = ttk.Entry(frame, width=40, font=('Segoe UI', 10))
        entry_duracion.grid(row=3, column=1, pady=5, padx=10, sticky=tk.W)
        entry_duracion.insert(0, "3")
        
        # ========== SUBTOTAL EN TIEMPO REAL ==========
        ttk.Label(frame, text="Subtotal (sin descuento):", font=('Segoe UI', 10, 'bold')).grid(row=4, column=0, sticky=tk.W, pady=5)
        subtotal_label = ttk.Label(frame, text="$0", font=('Segoe UI', 10), foreground="blue")
        subtotal_label.grid(row=4, column=1, pady=5, padx=10, sticky=tk.W)
        
        # ========== CAPACIDAD MÁXIMA DE LA SALA ==========
        capacidad_label = ttk.Label(frame, text="", font=('Segoe UI', 9), foreground="#c62828")  # Rojo oscuro legible
        capacidad_label.grid(row=5, column=0, columnspan=2, pady=2, sticky=tk.W)
        
        # ========== FECHA (OPCIONAL) ==========
        ttk.Label(frame, text="Fecha y Hora (opcional):", font=('Segoe UI', 10, 'bold')).grid(row=6, column=0, sticky=tk.W, pady=5)
        entry_fecha = ttk.Entry(frame, width=40, font=('Segoe UI', 10))
        entry_fecha.grid(row=6, column=1, pady=5, padx=10, sticky=tk.W)
        entry_fecha.insert(0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        
        # ========== FRAME PARA PARÁMETROS DINÁMICOS ==========
        params_frame = ttk.LabelFrame(frame, text="Parámetros del Servicio", padding="10")
        params_frame.grid(row=7, column=0, columnspan=2, pady=10, padx=5, sticky=tk.W+tk.E)
        
        # Variables para los campos dinámicos
        self.campo_personas = None
        self.campo_equipo_adicional = None
        self.campo_cantidad = None
        self.campo_seguro = None
        self.campo_tema = None
        self.campo_miembro_premium = None
        
        # Label de ayuda
        ayuda_label = ttk.Label(params_frame, text="Seleccione un servicio para ver los parámetros", 
                                font=('Segoe UI', 9), foreground="blue")
        ayuda_label.pack(anchor=tk.W, pady=5)
        
        # Frame para campos dinámicos
        campos_dinamicos = ttk.Frame(params_frame)
        campos_dinamicos.pack(fill=tk.X, pady=5)
        
        # ========== FUNCIÓN PARA ACTUALIZAR PRECIO BASE Y SUBTOTAL ==========
        def actualizar_precio_y_subtotal(event=None):
            try:
                seleccion = combo_servicio.get()
                duracion_texto = entry_duracion.get()
                if not seleccion or not duracion_texto:
                    return
                id_servicio = int(seleccion.split(" - ")[0])
                servicio = next((s for s in self.sistema.obtener_servicios() if s.id == id_servicio), None)
                if servicio:
                    precio_base_label.config(text=f"${servicio.precio_base:,.0f} / hora")
                    duracion = float(duracion_texto)
                    subtotal = servicio.precio_base * duracion
                    subtotal_label.config(text=f"${subtotal:,.0f}")
            except:
                precio_base_label.config(text="$0 / hora")
                subtotal_label.config(text="$0")
        
        # ========== FUNCIÓN PARA ACTUALIZAR SUBTOTAL CON PARÁMETROS ==========
        def actualizar_subtotal_con_parametros():
            try:
                seleccion = combo_servicio.get()
                duracion_texto = entry_duracion.get()
                if not seleccion or not duracion_texto:
                    return
                id_servicio = int(seleccion.split(" - ")[0])
                servicio = next((s for s in self.sistema.obtener_servicios() if s.id == id_servicio), None)
                if not servicio:
                    return
                duracion = float(duracion_texto)
                texto_servicio = seleccion.lower()
                params = {}
                if "sala" in texto_servicio:
                    if self.campo_personas and self.campo_personas.get():
                        try:
                            params["personas"] = int(self.campo_personas.get())
                        except:
                            params["personas"] = 10
                    if self.campo_equipo_adicional is not None:
                        params["equipo_adicional"] = self.campo_equipo_adicional.get()
                elif "equipo" in texto_servicio:
                    if self.campo_cantidad and self.campo_cantidad.get():
                        try:
                            params["cantidad"] = int(self.campo_cantidad.get())
                        except:
                            params["cantidad"] = 1
                    if self.campo_seguro is not None:
                        params["seguro"] = self.campo_seguro.get()
                elif "asesoria" in texto_servicio:
                    if self.campo_tema and self.campo_tema.get():
                        params["tema"] = self.campo_tema.get()
                    if self.campo_miembro_premium is not None:
                        params["miembro_premium"] = self.campo_miembro_premium.get()
                if params:
                    subtotal = servicio.calcular_costo(duracion, **params)
                else:
                    subtotal = servicio.precio_base * duracion
                subtotal_label.config(text=f"${subtotal:,.0f}")
            except Exception as e:
                print(f"Error: {e}")
        
        # ========== FUNCIÓN PARA ACTUALIZAR CAMPOS SEGÚN SERVICIO ==========
        def actualizar_campos_por_servicio(event=None):
            for widget in campos_dinamicos.winfo_children():
                widget.destroy()
            seleccion = combo_servicio.get().lower()
            capacidad_label.config(text="")
            actualizar_precio_y_subtotal()
            
            if "sala" in seleccion:
                ayuda_label.config(text="📌 Para SALA: ingrese el número de personas")
                try:
                    id_servicio = int(combo_servicio.get().split(" - ")[0])
                    servicio = next((s for s in self.sistema.obtener_servicios() if s.id == id_servicio), None)
                    if servicio and hasattr(servicio, 'capacidad'):
                        capacidad_label.config(text=f"⚠️ Capacidad máxima de esta sala: {servicio.capacidad} personas")
                except:
                    pass
                ttk.Label(campos_dinamicos, text="Número de personas:", font=('Segoe UI', 9)).pack(anchor=tk.W)
                self.campo_personas = ttk.Entry(campos_dinamicos, width=20, font=('Segoe UI', 10))
                self.campo_personas.pack(anchor=tk.W, pady=2)
                self.campo_personas.insert(0, "10")
                self.campo_personas.bind('<KeyRelease>', lambda e: actualizar_subtotal_con_parametros())
                self.campo_equipo_adicional = tk.BooleanVar(value=False)
                ttk.Checkbutton(campos_dinamicos, text="¿Equipo adicional? (+20% costo)", 
                                variable=self.campo_equipo_adicional,
                                command=actualizar_subtotal_con_parametros).pack(anchor=tk.W, pady=5)
            elif "equipo" in seleccion:
                ayuda_label.config(text="📌 Para EQUIPO: ingrese la cantidad de equipos")
                ttk.Label(campos_dinamicos, text="Cantidad de equipos:", font=('Segoe UI', 9)).pack(anchor=tk.W)
                self.campo_cantidad = ttk.Entry(campos_dinamicos, width=20, font=('Segoe UI', 10))
                self.campo_cantidad.pack(anchor=tk.W, pady=2)
                self.campo_cantidad.insert(0, "1")
                self.campo_cantidad.bind('<KeyRelease>', lambda e: actualizar_subtotal_con_parametros())
                self.campo_seguro = tk.BooleanVar(value=False)
                ttk.Checkbutton(campos_dinamicos, text="¿Seguro? (+$5,000)", 
                                variable=self.campo_seguro,
                                command=actualizar_subtotal_con_parametros).pack(anchor=tk.W, pady=5)
            elif "asesoria" in seleccion:
                ayuda_label.config(text="📌 Para ASESORÍA: ingrese el tema y si es miembro premium")
                ttk.Label(campos_dinamicos, text="Tema de asesoría:", font=('Segoe UI', 9)).pack(anchor=tk.W)
                self.campo_tema = ttk.Entry(campos_dinamicos, width=40, font=('Segoe UI', 10))
                self.campo_tema.pack(anchor=tk.W, pady=2)
                self.campo_tema.insert(0, "Python Avanzado")
                self.campo_miembro_premium = tk.BooleanVar(value=False)
                ttk.Checkbutton(campos_dinamicos, text="¿Miembro Premium? (15% descuento)", 
                                variable=self.campo_miembro_premium,
                                command=actualizar_subtotal_con_parametros).pack(anchor=tk.W, pady=5)
            else:
                ayuda_label.config(text="🔧 Seleccione un servicio para ver los parámetros disponibles")
        
        # ========== VINCULAR EVENTOS ==========
        combo_servicio.bind('<<ComboboxSelected>>', actualizar_campos_por_servicio)
        entry_duracion.bind('<KeyRelease>', actualizar_subtotal_con_parametros)
        
        # ========== FUNCIÓN GUARDAR ==========
        def guardar():
            try:
                if not combo_cliente.get():
                    raise Exception("Seleccione un cliente")
                if not combo_servicio.get():
                    raise Exception("Seleccione un servicio")
                
                id_cliente = int(combo_cliente.get().split(" - ")[0])
                id_servicio = int(combo_servicio.get().split(" - ")[0])
                duracion = float(entry_duracion.get())
                
                fecha = None
                if entry_fecha.get():
                    try:
                        fecha = datetime.datetime.strptime(entry_fecha.get(), "%Y-%m-%d %H:%M")
                    except:
                        raise Exception("Formato de fecha inválido. Use YYYY-MM-DD HH:MM")
                
                params = {}
                texto_servicio = combo_servicio.get().lower()
                
                if "sala" in texto_servicio:
                    if self.campo_personas and self.campo_personas.get().strip():
                        try:
                            params["personas"] = int(self.campo_personas.get())
                        except ValueError:
                            params["personas"] = 10
                    else:
                        params["personas"] = 10
                    if self.campo_equipo_adicional is not None:
                        params["equipo_adicional"] = self.campo_equipo_adicional.get()
                elif "equipo" in texto_servicio:
                    if self.campo_cantidad and self.campo_cantidad.get().strip():
                        try:
                            params["cantidad"] = int(self.campo_cantidad.get())
                            if params["cantidad"] <= 0:
                                params["cantidad"] = 1
                        except ValueError:
                            params["cantidad"] = 1
                    else:
                        params["cantidad"] = 1
                    if self.campo_seguro is not None:
                        params["seguro"] = self.campo_seguro.get()
                elif "asesoria" in texto_servicio:
                    if self.campo_tema and self.campo_tema.get().strip():
                        tema = self.campo_tema.get().strip()
                        if ',' in tema:
                            tema = tema.split(',')[0].strip()
                        params["tema"] = tema
                    else:
                        params["tema"] = "Python Avanzado"
                    if self.campo_miembro_premium is not None:
                        params["miembro_premium"] = self.campo_miembro_premium.get()
                
                self.sistema.crear_reserva(id_cliente, id_servicio, duracion, fecha, **params)
                self._actualizar_tablas()
                messagebox.showinfo("Éxito", "Reserva creada correctamente")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        # ========== BOTONES ==========
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=8, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="Crear Reserva", command=guardar, style='Success.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=dialog.destroy, style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        
        # ========== CENTRAR VENTANA ==========
        centrar_ventana(dialog, 550, 580)
    
    # =====================================================================================================
    # MÉTODO: _confirmar_reserva_seleccionada
    # Confirma la reserva seleccionada en la tabla
    # No permite confirmar reservas vencidas
    # =====================================================================================================
    def _confirmar_reserva_seleccionada(self):
    
        # Obtener el ID de la reserva seleccionada
        id_reserva = self._obtener_reserva_seleccionada()
        
        # Si no hay reserva seleccionada, salir
        if not id_reserva:
            return
        
        try:
            # Buscar la reserva en el sistema
            reserva = next((r for r in self.sistema.obtener_reservas() if r.id == id_reserva), None)
            
            # Si no se encuentra la reserva, mostrar error
            if not reserva:
                messagebox.showerror("Error", "No se encontró la reserva")
                return
            
            # ========== VALIDACIÓN: RESERVA VENCIDA ==========
            # Verificar si la reserva está vencida
            if reserva.esta_vencida():
                # Calcular fecha de finalización
                fecha_fin = reserva.fecha_reserva + datetime.timedelta(hours=reserva.duracion_horas)
                fecha_fin_str = fecha_fin.strftime('%Y-%m-%d %H:%M')
                
                # Mostrar mensaje de error
                messagebox.showerror(
                    "Error", 
                    f"❌ No se puede confirmar la reserva #{id_reserva} porque ya está VENCIDA.\n"
                    f"📅 Finalizó el: {fecha_fin_str}\n"
                    f"💡 Las reservas vencidas no se pueden modificar."
                )
                return
            
            # Confirmar la reserva
            self.sistema.confirmar_reserva(id_reserva)
            
            # Actualizar las tablas
            self._actualizar_tablas()
            
            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", "Reserva confirmada correctamente")
            
        except Exception as e:
            # Mostrar error si ocurre algún problema
            messagebox.showerror("Error", str(e))
    
    # =====================================================================================================
    # MÉTODO: _cancelar_reserva_seleccionada, cancela la reserva seleccionada (solicita motivo)
    # =====================================================================================================
    def _cancelar_reserva_seleccionada(self):
        
        id_reserva = self._obtener_reserva_seleccionada()
        if not id_reserva:
            return
        
        # askstring(): solicita una cadena de texto al usuario
        motivo = simpledialog.askstring("Motivo", "Ingrese el motivo de cancelación:")
        
        try:
            self.sistema.cancelar_reserva(id_reserva, motivo or "")
            self._actualizar_tablas()
            messagebox.showinfo("Éxito", "Reserva cancelada correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    # =====================================================================================================
    # MÉTODO: _completar_reserva_seleccionada
    # Completa la reserva seleccionada en la tabla
    # No permite completar reservas vencidas
    # =====================================================================================================
    def _completar_reserva_seleccionada(self):
        
        # Obtener el ID de la reserva seleccionada
        id_reserva = self._obtener_reserva_seleccionada()
        
        # Si no hay reserva seleccionada, salir
        if not id_reserva:
            return
        
        try:
            # Buscar la reserva en el sistema
            reserva = next((r for r in self.sistema.obtener_reservas() if r.id == id_reserva), None)
            
            # Si no se encuentra la reserva, mostrar error
            if not reserva:
                messagebox.showerror("Error", "No se encontró la reserva")
                return
            
            # ========== VALIDACIÓN: RESERVA VENCIDA ==========
            # Verificar si la reserva está vencida
            if reserva.esta_vencida():
                # Calcular fecha de finalización
                fecha_fin = reserva.fecha_reserva + datetime.timedelta(hours=reserva.duracion_horas)
                fecha_fin_str = fecha_fin.strftime('%Y-%m-%d %H:%M')
                
                # Mostrar mensaje de error
                messagebox.showerror(
                    "Error", 
                    f"❌ No se puede completar la reserva #{id_reserva} porque ya está VENCIDA.\n"
                    f"📅 Finalizó el: {fecha_fin_str}\n"
                    f"💡 Las reservas vencidas ya no se pueden modificar."
                )
                return
            
            # Completar la reserva
            self.sistema.completar_reserva(id_reserva)
            
            # Actualizar las tablas
            self._actualizar_tablas()
            
            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", "Reserva completada correctamente")
            
        except Exception as e:
            # Mostrar error si ocurre algún problema
            messagebox.showerror("Error", str(e))
    
    # =====================================================================================================
    # MÉTODO: _aplicar_descuento_reserva, aplica descuento porcentual a la reserva seleccionada
    # muestra información ANTES y DESPUÉS del descuento
    # =====================================================================================================
    def _aplicar_descuento_reserva(self):
        # Obtener el ID de la reserva seleccionada
        id_reserva = self._obtener_reserva_seleccionada()
        
        # Si no hay reserva seleccionada, salir
        if not id_reserva:
            return
        
        # Buscar la reserva completa en el sistema
        reserva = next((r for r in self.sistema.obtener_reservas() if r.id == id_reserva), None)
        
        # Si no se encuentra la reserva, mostrar error
        if not reserva:
            messagebox.showerror("Error", "No se encontró la reserva")
            return
        
        # Obtener información actual de la reserva (antes del descuento)
        info = reserva.obtener_info()
        
        # ========== MOSTRAR INFORMACIÓN ACTUAL (ANTES DEL DESCUENTO) ==========
        # CORRECCIÓN: Las líneas dentro del f-string NO deben tener indentación
        mensaje_actual = f"""📊 INFORMACIÓN ACTUAL DE LA RESERVA:
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        📅 Reserva ID: {info['id']}
        👤 Cliente: {info['cliente']}
        🛠️ Servicio: {info['servicio']}
        ⏱️ Duración: {info['duracion']} horas
        📝 Parámetros: {info.get('parametros_extra', {})}
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        💰 Precio Base: ${info['precio_base']:,.0f}
        💸 Descuento actual: {info['porcentaje_descuento']:.0f}% (${info['valor_descuento']:,.0f})
        💵 Total actual: ${info['costo_total']:,.0f}
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        # Solicitar al usuario el nuevo porcentaje de descuento
        # askfloat() muestra un diálogo para ingresar un número decimal
        # minvalue=0 y maxvalue=100 limitan el rango permitido
        porcentaje = simpledialog.askfloat(
            "Aplicar Descuento",
            mensaje_actual + "\nIngrese el NUEVO porcentaje de descuento (0-100):\n(0 para eliminar descuento)",
            minvalue=0,
            maxvalue=100
        )
        
        # Si el usuario ingresó un porcentaje (no canceló)
        if porcentaje is not None:
            try:
                # Aplicar el descuento a la reserva
                self.sistema.aplicar_descuento_reserva(id_reserva, porcentaje)
                
                # Actualizar las tablas para reflejar el cambio
                self._actualizar_tablas()
                
                # Obtener la información actualizada de la reserva (después del descuento)
                reserva_actualizada = next(
                    (r for r in self.sistema.obtener_reservas() if r.id == id_reserva),
                    None
                )
                
                if reserva_actualizada:
                    info_nueva = reserva_actualizada.obtener_info()
                    
                    # ========== MOSTRAR RESULTADO (DESPUÉS DEL DESCUENTO) ==========
                    # CORRECCIÓN: Las líneas dentro del f-string NO deben tener indentación
                    mensaje_resultado = f"""✅ DESCUENTO APLICADO CORRECTAMENTE
                    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    💰 Precio Base: ${info_nueva['precio_base']:,.0f}
                    💸 Nuevo descuento: {info_nueva['porcentaje_descuento']:.0f}% (${info_nueva['valor_descuento']:,.0f})
                    💵 Total a pagar: ${info_nueva['costo_total']:,.0f}
                    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    💡 Ahorro total: ${info_nueva['valor_descuento']:,.0f}"""
                    
                    messagebox.showinfo("Descuento Aplicado", mensaje_resultado)
                    
            except Exception as e:
                # Mostrar error si ocurre algún problema
                messagebox.showerror("Error", str(e))
    
    # ==================== MÉTODOS DE EXPORTACIÓN ====================
    
    # =====================================================================================================
    # MÉTODO: _exportar_clientes, exporta la lista de clientes a un archivo CSV
    # =====================================================================================================
    def _exportar_clientes(self):
        
        try:
            self.sistema.exportar_clientes_csv()
            messagebox.showinfo("Éxito", "Clientes exportados a 'clientes_export.csv'")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")
    
    # =====================================================================================================
    # MÉTODO: _exportar_servicios, exporta la lista de servicios a un archivo CSV
    # =====================================================================================================
    def _exportar_servicios(self):
        
        try:
            self.sistema.exportar_servicios_csv()
            messagebox.showinfo("Éxito", "Servicios exportados a 'servicios_export.csv'")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")
    
    # =====================================================================================================
    # MÉTODO: _exportar_reservas, exporta la lista de reservas a un archivo CSV
    # =====================================================================================================
    def _exportar_reservas(self):
        
        try:
            self.sistema.exportar_reservas_csv()
            messagebox.showinfo("Éxito", "Reservas exportadas a 'reservas_export.csv'")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")
    
    # =====================================================================================================
    # MÉTODO: _guardar_backup_manual, guarda manualmente un backup de todos los datos
    # =====================================================================================================
    def _guardar_backup_manual(self):
        
        try:
            self.sistema.guardar_datos()
            messagebox.showinfo("Éxito", "Backup guardado correctamente en 'backup_sistema.pkl'")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el backup: {str(e)}")
    
    # ==================== OTROS MÉTODOS ====================
    
    # =====================================================================================================
    # MÉTODO: _ver_logs, muestra el archivo de logs en una ventana de texto con scroll
    # =====================================================================================================
    def _ver_logs(self):
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Registro de Logs del Sistema")
        dialog.transient(self.root)
        
        frame = ttk.Frame(dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # ScrolledText: área de texto con barras de desplazamiento automáticas
        text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=100, height=40, font=('Consolas', 9))
        text_area.pack(fill=tk.BOTH, expand=True)
        
        try:
            with open("logs.txt", "r", encoding='utf-8') as f:
                content = f.read()
                text_area.insert(tk.END, content)
        except FileNotFoundError:
            text_area.insert(tk.END, "No se encontró el archivo de logs")
        
        text_area.config(state=tk.DISABLED)  # Solo lectura (el usuario no puede editar)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Cerrar", command=dialog.destroy, style='Primary.TButton').pack()
        
        centrar_ventana(dialog, 900, 700)  # Para logs, tamaño fijo más grande
        
    # =====================================================================================================
    # MÉTODO: _acerca_de, muestra información acerca del sistema y los desarrolladores
    # =====================================================================================================
    def _acerca_de(self):
    
        acerca_texto = """🏢 SOFTWARE FJ - Sistema Integral de Gestión
        
        Versión: 1.0
        Fecha: Mayo 2026
        Desarrollado por: Grupo 146

        Integrantes:
        • Yuris Cerguey Reyes Mandón
        • Danna Valeria Uribe Santiago
        • Jose Daniel Machado Castellanos
        • Diego Alejandro Rocha Manzano

        Características incluidas:
        • Gestión completa de Clientes
        • Gestión de Servicios (Salas, Equipos, Asesorías)
        • Sistema de Reservas con estados
            - Pendiente - Confirmada - Cancelada - Completada
        • Validación de disponibilidad por fecha/hora
        • Backup automático y manual (pickle)
        • Exportación a CSV (Clientes, Servicios, Reservas)
        • Búsqueda y filtrado en todas las tablas
        • Manejo robusto de excepciones (logs)
        • Registro de logs automático
        • Interfaz gráfica moderna con Tkinter
        • Ventanas centradas y ajustables al contenido

        ¡Sistema 100% funcional y sin base de datos!"""
        
        messagebox.showinfo("Acerca de Software FJ", acerca_texto)
    
    # =====================================================================================================
    # MÉTODO: _mostrar_estadisticas, muestra estadísticas del sistema en un cuadro de diálogo
    # =====================================================================================================
    def _mostrar_estadisticas(self):
        
        clientes = self.sistema.obtener_clientes()
        servicios = self.sistema.obtener_servicios()
        reservas = self.sistema.obtener_reservas()
        
        # Cálculos estadísticos usando comprensión de listas y len()
        clientes_activos = len([c for c in clientes if c.activo])
        servicios_disponibles = len([s for s in servicios if s.disponible])
        
        reservas_pendientes = len([r for r in reservas if r.estado == "PENDIENTE"])
        reservas_confirmadas = len([r for r in reservas if r.estado == "CONFIRMADA"])
        reservas_canceladas = len([r for r in reservas if r.estado == "CANCELADA"])
        reservas_completadas = len([r for r in reservas if r.estado == "COMPLETADA"])
        
        # Suma total de ingresos: sum() suma todos los elementos de la lista
        ingreso_total = sum([r.obtener_info()['costo'] for r in reservas if r.estado in ["CONFIRMADA", "COMPLETADA"]])
        
        # f-string: formatea el texto con variables insertadas entre {}
        stats_texto = f"""📊 ESTADÍSTICAS DEL SISTEMA

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        👥 CLIENTES
        • Total clientes: {len(clientes)}
        • Clientes activos: {clientes_activos}
        • Clientes inactivos: {len(clientes) - clientes_activos}

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        🛠️ SERVICIOS
        • Total servicios: {len(servicios)}
        • Servicios disponibles: {servicios_disponibles}
        • Servicios no disponibles: {len(servicios) - servicios_disponibles}
        • Tipos de servicios:
            - Salas: {len([s for s in servicios if isinstance(s, ReservaSalas)])}
            - Equipos: {len([s for s in servicios if isinstance(s, AlquilerEquipos)])}
            - Asesorías: {len([s for s in servicios if isinstance(s, AsesoriaEspecializada)])}

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        📅 RESERVAS
        • Total reservas: {len(reservas)}
        • Pendientes: {reservas_pendientes}
        • Confirmadas: {reservas_confirmadas}
        • Canceladas: {reservas_canceladas}
        • Completadas: {reservas_completadas}

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        💰 FINANCIERO
        • Ingreso total: ${ingreso_total:,.0f}
        • Promedio por reserva: ${ingreso_total/len(reservas) if reservas else 0:,.0f}
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
        messagebox.showinfo("Estadísticas del Sistema", stats_texto)
    
    # =====================================================================================================
    # MÉTODO: _on_closing, maneja el cierre de la ventana principal
    # pregunta confirmación y guarda datos automáticamente
    # =====================================================================================================
    def _on_closing(self):
        
        # askokcancel(): muestra un diálogo con OK/Cancelar, retorna True si elige OK
        if messagebox.askokcancel("Salir", "¿Está seguro de que desea salir del sistema?\nLos datos se guardarán automáticamente."):
            self.sistema.guardar_datos()  # Guarda backup antes de salir
            self.root.destroy()            # Destruye la ventana principal (cierra el programa)
    
    # =====================================================================================================
    # MÉTODO: ejecutar, inicia la aplicación (entra en el bucle principal de Tkinter)
    # =====================================================================================================
    def ejecutar(self):

        self.root.mainloop()  # mainloop(): bucle infinito que espera eventos (clics, teclas, etc.)

    # =====================================================================================================
    # MÉTODO: _probar_sobrecarga_reserva, muestra un diálogo para seleccionar una reserva activa
    # y probar los métodos sobrecargados. Excluye reservas CANCELADAS
    # =====================================================================================================
    def _probar_sobrecarga_reserva(self):
        
        reservas = self.sistema.obtener_reservas()
        
        if not reservas:
            messagebox.showwarning("Advertencia", 
                "No hay reservas en el sistema.\n"
                "Primero cree una reserva válida desde la pestaña Reservas.")
            return
        
        # ========== FILTRAR RESERVAS ACTIVAS =============================================================
        # Solo reservas PENDIENTES, CONFIRMADAS y COMPLETADAS (excluye CANCELADAS)
        reservas_activas = [r for r in reservas if r.estado != "CANCELADA"]
        
        
        if not reservas_activas:
            messagebox.showwarning("Advertencia", 
                "No hay reservas activas (PENDIENTE o CONFIRMADA) para probar.\n"
                "Todas las reservas están CANCELADAS o COMPLETADAS.\n\n"
                "Cree una nueva reserva para probar los métodos sobrecargados.")
            return
        
        # ========== CREAR DIÁLOGO DE SELECCIÓN ===========================================================
        dialog = tk.Toplevel(self.root)
        dialog.title("Seleccionar Reserva - Probar Sobrecarga")
        dialog.transient(self.root)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(frame, text="📊 Seleccione una reserva para probar los métodos sobrecargados", 
                font=('Segoe UI', 12, 'bold')).pack(pady=(0, 10))
        
        ttk.Label(frame, text=f"Reservas activas disponibles: {len(reservas_activas)}", 
                font=('Segoe UI', 10), foreground="green").pack(pady=(0, 15))
        
        # Frame para el Treeview (tabla de selección)
        table_frame = ttk.Frame(frame)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Crear Treeview con scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("ID", "Cliente", "Servicio", "Duración", "Estado", "Costo")
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', 
                            height=10, yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        # Configurar columnas
        tree.heading("ID", text="ID")
        tree.heading("Cliente", text="Cliente")
        tree.heading("Servicio", text="Servicio")
        tree.heading("Duración", text="Duración (h)")
        tree.heading("Estado", text="Estado")
        tree.heading("Costo", text="Costo Total")
        
        tree.column("ID", width=60, anchor="center")
        tree.column("Cliente", width=180)
        tree.column("Servicio", width=180)
        tree.column("Duración", width=80, anchor="center")
        tree.column("Estado", width=100, anchor="center")
        tree.column("Costo", width=100, anchor="center")
        
        # Llenar la tabla con reservas activas
        for reserva in reservas_activas:
            info = reserva.obtener_info()
            # Asignar color según estado
            estado = info['estado']
            if estado == "PENDIENTE":
                estado_display = "⏳ PENDIENTE"
            elif estado == "CONFIRMADA":
                estado_display = "✅ CONFIRMADA"
            else:
                estado_display = estado
            
            tree.insert("", tk.END, values=(
                info['id'], 
                info['cliente'], 
                info['servicio'], 
                info['duracion'], 
                estado_display,
                f"${info['costo_total']:,.0f}"
            ), tags=(estado,))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Configurar colores para los estados
        tree.tag_configure("PENDIENTE", background="#FFF3E0")  # Naranja claro
        tree.tag_configure("CONFIRMADA", background="#E8F5E9")  # Verde claro
        
        # Instrucciones
        ttk.Label(frame, text="💡 Haga doble clic en una reserva para probar sus métodos sobrecargados", 
                font=('Segoe UI', 9), foreground="gray").pack(pady=10)
        
        # Variable para almacenar la reserva seleccionada
        reserva_seleccionada = None
        
        # =================================================================================================
        # Toma la reserva seleccionada y muestra la demostración
        # =================================================================================================
        def probar_metodos():
            
            nonlocal reserva_seleccionada
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Advertencia", "Por favor seleccione una reserva")
                return
            
            # Obtener el ID de la reserva seleccionada
            item = tree.item(selection[0])
            reserva_id = item['values'][0]
            
            # Buscar la reserva en la lista de activas
            reserva_seleccionada = next((r for r in reservas_activas if r.id == reserva_id), None)
            
            if not reserva_seleccionada:
                messagebox.showerror("Error", "No se encontró la reserva seleccionada")
                return
            
            # Verificar si la reserva tiene el método demostrar_todas_sobrecargas
            if not hasattr(reserva_seleccionada, 'demostrar_todas_sobrecargas'):
                messagebox.showwarning("Advertencia", 
                    "La reserva seleccionada no tiene implementados los métodos sobrecargados.\n"
                    "Asegúrese de tener la versión actualizada de reserva.py")
                return
            
            # Cerrar el diálogo de selección
            dialog.destroy()
            
            # Mostrar la demostración
            mostrar_demostracion(reserva_seleccionada)
        
        # =================================================================================================
        # Muestra la demostración de sobrecarga para una reserva específica
        # =================================================================================================
        def mostrar_demostracion(reserva):
            
            # Obtener la demostración
            demostracion = reserva.demostrar_todas_sobrecargas()
            
            # Mostrar en una ventana
            demo_dialog = tk.Toplevel(self.root)
            demo_dialog.title(f"Demostración de Métodos Sobrecargados - Reserva #{reserva.id} - {reserva._cliente.nombre}")
            demo_dialog.transient(self.root)
            
            demo_frame = ttk.Frame(demo_dialog, padding="10")
            demo_frame.pack(fill=tk.BOTH, expand=True)
            
            # Información de la reserva seleccionada
            info_label = ttk.Label(demo_frame, 
                text=f"🗂️ Reserva #{reserva.id} | Cliente: {reserva._cliente.nombre} | "
                    f"Servicio: {reserva._servicio.nombre} | Estado: {reserva.estado}",
                font=('Segoe UI', 10, 'bold'), foreground="#1a237e")
            info_label.pack(pady=(0, 10))
            
            text_area = scrolledtext.ScrolledText(demo_frame, wrap=tk.WORD, width=85, height=35, font=('Consolas', 9))
            text_area.pack(fill=tk.BOTH, expand=True)
            text_area.insert(tk.END, demostracion)
            text_area.config(state=tk.DISABLED)
            
            btn_frame = ttk.Frame(demo_frame)
            btn_frame.pack(pady=10)
            
            # Botón para probar otra reserva
            ttk.Button(btn_frame, text="🔄 Probar otra reserva", 
                    command=lambda: [demo_dialog.destroy(), self._probar_sobrecarga_reserva()],
                    style='Primary.TButton').pack(side=tk.LEFT, padx=5)
            
            ttk.Button(btn_frame, text="Cerrar", 
                    command=demo_dialog.destroy, 
                    style='Danger.TButton').pack(side=tk.LEFT, padx=5)
            
            centrar_ventana(demo_dialog, 900, 750)
        
        # =================================================================================================
        # Maneja el doble clic en la tabla
        # =================================================================================================
        def doble_clic(event):
            
            probar_metodos()
        
        # Botones
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="✅ Probar Métodos", 
                command=probar_metodos, 
                style='Success.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, text="❌ Cancelar", 
                command=dialog.destroy, 
                style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        
        # Vincular doble clic
        tree.bind("<Double-1>", doble_clic)
        
        # Centrar y mostrar
        centrar_ventana(dialog, 900, 550)

    # =====================================================================================================
    # MÉTODO: _probar_sobrecarga_reserva_seleccionada, prueba los métodos sobrecargados
    # con la reserva SELECCIONADA en la tabla. Excluye reservas CANCELADAS
    # =====================================================================================================    
    def _probar_sobrecarga_reserva_seleccionada(self):
    
        # Obtener la reserva seleccionada
        id_reserva = self._obtener_reserva_seleccionada()
        if not id_reserva:
            return
        
        # Buscar la reserva
        reserva = next((r for r in self.sistema.obtener_reservas() if r.id == id_reserva), None)
        if not reserva:
            messagebox.showerror("Error", "No se encontró la reserva seleccionada")
            return
        
        # Validar estado
        if reserva.estado not in ["PENDIENTE", "CONFIRMADA", "COMPLETADA"]:
            messagebox.showwarning("Advertencia", f"No se puede probar en reserva {reserva.estado}")
            return
        
        # Verificar método
        if not hasattr(reserva, 'demostrar_todas_sobrecargas'):
            messagebox.showwarning("Advertencia", 
                "La reserva seleccionada no tiene implementados los métodos sobrecargados.")
            return
        
        # Obtener la demostración
        demostracion = reserva.demostrar_todas_sobrecargas()
        
        # Mostrar en una ventana (usando Toplevel como en el menú)
        demo_dialog = tk.Toplevel(self.root)
        demo_dialog.title(f"Demostración de Métodos Sobrecargados - Reserva #{reserva.id} - {reserva._cliente.nombre}")
        demo_dialog.transient(self.root)
        
        demo_frame = ttk.Frame(demo_dialog, padding="10")
        demo_frame.pack(fill=tk.BOTH, expand=True)
        
        # Información de la reserva seleccionada (IGUAL que en el menú)
        info_label = ttk.Label(demo_frame, 
            text=f"🗂️ Reserva #{reserva.id} | Cliente: {reserva._cliente.nombre} | "
                f"Servicio: {reserva._servicio.nombre} | Estado: {reserva.estado}",
            font=('Segoe UI', 10, 'bold'), foreground="#1a237e")
        info_label.pack(pady=(0, 10))
        
        text_area = scrolledtext.ScrolledText(demo_frame, wrap=tk.WORD, width=85, height=35, font=('Consolas', 9))
        text_area.pack(fill=tk.BOTH, expand=True)
        text_area.insert(tk.END, demostracion)
        text_area.config(state=tk.DISABLED)
        
        btn_frame = ttk.Frame(demo_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="❌ Cerrar", 
                command=demo_dialog.destroy, 
                style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        
        # Centrar ventana (mismo que usa el menú)
        centrar_ventana(demo_dialog)

    # =====================================================================================================
    # DEMOSTRACIONES DE MANEJO DE EXCEPCIONES (try/except/else)
    # El bloque 'else' se ejecuta SOLO si NO ocurrió una excepción en el 'try'
    # =====================================================================================================
    def _demostracion_try_except_else(self):
        
        logger = LoggerSistema()
        sistema = self.sistema  # Usar el sistema existente
        
        logger.registrar_evento("=== INICIO DEMOSTRACIÓN try/except/else ===")
        
        # Caso 1: Sin error (el else se ejecuta)
        try:
            logger.registrar_evento("  Intentando registrar cliente VÁLIDO...")
            sistema.registrar_cliente("Demo Válido", "demo_valido@email.com", "3001112223", "999888777")
            logger.registrar_evento("  Cliente registrado en el bloque try")
        except Exception as e:
            logger.registrar_error(e, "try/except/else - caso válido")
        else:
            logger.registrar_evento("  ✅ Bloque 'else' ejecutado correctamente")
        
        # Caso 2: Con error (el else NO se ejecuta)
        try:
            logger.registrar_evento("  Intentando registrar cliente INVÁLIDO...")
            sistema.registrar_cliente("", "", "", "")
        except Exception as e:
            logger.registrar_error(e, "try/except/else - caso inválido")
        else:
            logger.registrar_evento("  El bloque 'else' NO debería ejecutarse")
        
        logger.registrar_evento("=== FIN DEMOSTRACIÓN try/except/else ===")


    # =====================================================================================================
    # DEMOSTRACIONES DE MANEJO DE EXCEPCIONES (try/except/finally)
    # =====================================================================================================
    def _demostracion_try_except_finally(self):
        
        logger = LoggerSistema()
        
        logger.registrar_evento("=== INICIO DEMOSTRACIÓN try/except/finally ===")
        
        # Caso 1: Sin error
        archivo = None
        try:
            archivo = open("demo_correcto.tmp", "w", encoding="utf-8")
            archivo.write("Prueba")
            logger.registrar_evento("  Archivo escrito correctamente")
        except Exception as e:
            logger.registrar_error(e, "try/except/finally - caso correcto")
        finally:
            if archivo:
                archivo.close()
                logger.registrar_evento("  Archivo cerrado en finally")
            if os.path.exists("demo_correcto.tmp"):
                os.remove("demo_correcto.tmp")
        
        # Caso 2: Con error
        archivo = None
        try:
            archivo = open("Z:/ruta_inexistente/demo_error.tmp", "w", encoding="utf-8")
            archivo.write("Esto no se ejecuta")
        except Exception as e:
            logger.registrar_error(e, "try/except/finally - caso con error")
        finally:
            logger.registrar_evento("  Bloque 'finally' ejecutado (aunque hubo error)")
        
        logger.registrar_evento("=== FIN DEMOSTRACIÓN try/except/finally ===")


    # =====================================================================================================
    # EJECUTA TODAS LAS DEMOSTRACIONES DE MANEJO DE EXCEPCIONES
    # =====================================================================================================
    def _ejecutar_validaciones_completas(self):
        
        logger = LoggerSistema()
        
        logger.registrar_evento("=" * 60)
        logger.registrar_evento("INICIO DE VALIDACIONES COMPLETAS")
        logger.registrar_evento("=" * 60)
        
        self._demostracion_try_except_else()
        self._demostracion_try_except_finally()
        
        # Demostración de encadenamiento de excepciones
        try:
            logger.registrar_evento("  Demostrando encadenamiento de excepciones...")
            try:
                x = int("no es un numero")
            except ValueError as error_base:
                from excepciones import ReservaInvalidaError
                raise ReservaInvalidaError("Error al procesar la reserva") from error_base
        except ReservaInvalidaError as e:
            logger.registrar_error(e, "Encadenamiento de excepciones")
        
        logger.registrar_evento("VALIDACIONES COMPLETADAS CON ÉXITO")


    # =====================================================================================================
    # MÉTODO: _ejecutar_validaciones_demo
    # =====================================================================================================    
    def _ejecutar_validaciones_demo(self):
        
        # Redirigir la salida
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        try:
            self._ejecutar_validaciones_completas()
            output = sys.stdout.getvalue()
        except Exception as e:
            output = f"Error al ejecutar validaciones: {str(e)}"
        finally:
            sys.stdout = old_stdout
        
        if not output:
            output = "Validaciones ejecutadas correctamente. Revise logs.txt para detalles."
        
        # Mostrar en ventana
        dialog = tk.Toplevel(self.root)
        dialog.title("Validaciones - try/except/else/finally")
        dialog.transient(self.root)
        
        frame = ttk.Frame(dialog, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="📋 Resultado de las Validaciones", 
                font=('Segoe UI', 12, 'bold')).pack(pady=(0, 10))
        
        text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=20, font=('Consolas', 9))
        text_area.pack(fill=tk.BOTH, expand=True)
        text_area.insert(tk.END, output)
        text_area.config(state=tk.DISABLED)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Cerrar", command=dialog.destroy, style='Primary.TButton').pack()
        
        centrar_ventana(dialog, 700, 450)
    
    # =====================================================================================================
    # MÉTODO: _ver_detalles_reserva_doble_clic, muestra una ventana con TODOS
    # los detalles completos de la reserva
    # Esto permite ver los parámetros extra sin que se corten en la tabla
    # event - evento de tkinter (doble clic)
    # ===================================================================================================== 
    def _ver_detalles_reserva_doble_clic(self, event):
        
        # ========== OBTENER RESERVA SELECCIONADA ==========
        # Obtener el ID de la reserva seleccionada en la tabla
        id_reserva = self._obtener_reserva_seleccionada()
        
        # Si no hay ninguna reserva seleccionada, mostrar advertencia y salir
        if not id_reserva:
            messagebox.showwarning("Advertencia", "Por favor seleccione una reserva")
            return
        
        # Buscar la reserva completa en el sistema por su ID
        reserva = next((r for r in self.sistema.obtener_reservas() if r.id == id_reserva), None)
        
        # Si no se encuentra la reserva, mostrar error
        if not reserva:
            messagebox.showerror("Error", "No se encontró la reserva")
            return
        
        # Obtener toda la información de la reserva como diccionario
        info = reserva.obtener_info()
        
        # ========== CREAR VENTANA DE DETALLES (SIN SCROLLBAR) ==========
        # Toplevel() crea una ventana hija de la ventana principal
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Detalles de la Reserva #{id_reserva}")
        dialog.transient(self.root)  # Hace que sea hija de la ventana principal
        dialog.grab_set()  # Ventana modal (bloquea otras ventanas)
        
        # ========== FRAME PRINCIPAL (SIN SCROLLBAR) ==========
        # Frame con padding de 15 píxeles
        frame = ttk.Frame(dialog, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # ========== TÍTULO PRINCIPAL ==========
        titulo = ttk.Label(
            frame, 
            text="📋 DETALLES COMPLETOS DE LA RESERVA", 
            font=('Segoe UI', 14, 'bold'), 
            foreground=self.colores["primary"]
        )
        titulo.pack(pady=(0, 15))
        
        # ========== SECCIÓN 1: INFORMACIÓN GENERAL ==========
        # Frame con borde y título
        general_frame = ttk.LabelFrame(frame, text="Información General", padding="10")
        general_frame.pack(fill=tk.X, pady=5)
        
        # Configurar grid para 2 columnas
        general_frame.columnconfigure(0, weight=0)
        general_frame.columnconfigure(1, weight=1)
        
        # Mostrar ID de la reserva
        ttk.Label(general_frame, text="ID de Reserva:", font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=3)
        ttk.Label(general_frame, text=f"{info['id']}", font=('Segoe UI', 10)).grid(row=0, column=1, sticky=tk.W, padx=10, pady=3)
        
        # Mostrar nombre del cliente
        ttk.Label(general_frame, text="Cliente:", font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=3)
        ttk.Label(general_frame, text=f"{info['cliente']}", font=('Segoe UI', 10)).grid(row=1, column=1, sticky=tk.W, padx=10, pady=3)
        
        # Mostrar nombre del servicio
        ttk.Label(general_frame, text="Servicio:", font=('Segoe UI', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=3)
        ttk.Label(general_frame, text=f"{info['servicio']}", font=('Segoe UI', 10)).grid(row=2, column=1, sticky=tk.W, padx=10, pady=3)
        
        # Mostrar duración en horas
        ttk.Label(general_frame, text="Duración:", font=('Segoe UI', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=3)
        ttk.Label(general_frame, text=f"{info['duracion']} horas", font=('Segoe UI', 10)).grid(row=3, column=1, sticky=tk.W, padx=10, pady=3)
        
        # Mostrar estado con emoji para mejor visualización
        ttk.Label(general_frame, text="Estado:", font=('Segoe UI', 10, 'bold')).grid(row=4, column=0, sticky=tk.W, pady=3)
        estado_emoji = {
            "PENDIENTE": "⏳ Pendiente",
            "CONFIRMADA": "✅ Confirmada",
            "CANCELADA": "❌ Cancelada",
            "COMPLETADA": "🏁 Completada"
        }.get(info['estado'], info['estado'])
        ttk.Label(general_frame, text=estado_emoji, font=('Segoe UI', 10)).grid(row=4, column=1, sticky=tk.W, padx=10, pady=3)
        
        # Mostrar fecha de la reserva
        ttk.Label(general_frame, text="Fecha:", font=('Segoe UI', 10, 'bold')).grid(row=5, column=0, sticky=tk.W, pady=3)
        ttk.Label(general_frame, text=f"{info['fecha']}", font=('Segoe UI', 10)).grid(row=5, column=1, sticky=tk.W, padx=10, pady=3)
        
        # Mostrar si la reserva está vencida (con color rojo)
        if reserva.esta_vencida():
            ttk.Label(general_frame, text="⚠️ Esta reserva ya VENCIÓ", 
                    font=('Segoe UI', 9, 'bold'), foreground="red").grid(row=6, column=0, columnspan=2, pady=5)
        
        # ========== SECCIÓN 2: PARÁMETROS EXTRA (COMPLETOS) ==========
        params_frame = ttk.LabelFrame(frame, text="📝 Parámetros Extra Usados", padding="10")
        params_frame.pack(fill=tk.X, pady=5)
        
        # Verificar si hay parámetros extra
        if info.get("parametros_extra") and len(info["parametros_extra"]) > 0:
            # Configurar grid para 2 columnas
            params_frame.columnconfigure(0, weight=0)
            params_frame.columnconfigure(1, weight=1)
            
            # Recorrer cada parámetro y mostrarlo en una fila
            row = 0
            for key, value in info["parametros_extra"].items():
                # Convertir booleanos a texto legible
                if isinstance(value, bool):
                    value_str = "✅ Sí" if value else "❌ No"
                else:
                    value_str = str(value)
                
                # Mostrar clave (nombre del parámetro)
                ttk.Label(params_frame, text=f"{key}:", font=('Segoe UI', 10, 'bold')).grid(row=row, column=0, sticky=tk.W, pady=2)
                # Mostrar valor del parámetro
                ttk.Label(params_frame, text=value_str, font=('Segoe UI', 10)).grid(row=row, column=1, sticky=tk.W, padx=10, pady=2)
                row += 1
        else:
            # Mensaje si no hay parámetros
            ttk.Label(params_frame, text="No se especificaron parámetros extra", 
                    font=('Segoe UI', 10), foreground="gray").pack()
        
        # ========== SECCIÓN 3: INFORMACIÓN FINANCIERA COMPLETA ==========
        financial_frame = ttk.LabelFrame(frame, text="💰 Información Financiera", padding="10")
        financial_frame.pack(fill=tk.X, pady=5)
        
        # Configurar grid para 2 columnas
        financial_frame.columnconfigure(0, weight=0)
        financial_frame.columnconfigure(1, weight=1)
        
        # Mostrar precio base (sin descuento)
        ttk.Label(financial_frame, text="Precio Base:", font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=3)
        ttk.Label(financial_frame, text=f"${info['precio_base']:,.0f}", font=('Segoe UI', 10)).grid(row=0, column=1, sticky=tk.W, padx=10, pady=3)
        
        # Mostrar descuento si hay
        if info['porcentaje_descuento'] > 0:
            ttk.Label(financial_frame, text="Descuento aplicado:", font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=3)
            ttk.Label(financial_frame, text=f"{info['porcentaje_descuento']:.0f}% (${info['valor_descuento']:,.0f})", 
                font=('Segoe UI', 10), foreground="green").grid(row=1, column=1, sticky=tk.W, padx=10, pady=3)
        
        # Mostrar total a pagar (con descuento aplicado) - más grande y en negrita
        ttk.Label(financial_frame, text="TOTAL A PAGAR:", font=('Segoe UI', 12, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Label(financial_frame, text=f"${info['costo_total']:,.0f}", 
                font=('Segoe UI', 14, 'bold'), foreground=self.colores["primary"]).grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)
        
        # ========== BOTÓN CERRAR ==========
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="Cerrar", command=dialog.destroy, style='Primary.TButton').pack()
        
        # ========== CALCULAR TAMAÑO ÓPTIMO DE LA VENTANA ==========
        # Forzar actualización para obtener las dimensiones reales
        dialog.update_idletasks()
        
        # Obtener el ancho y alto que la ventana NECESITA para mostrar todo el contenido
        ancho_necesario = dialog.winfo_reqwidth() + 40  # +40 de margen
        alto_necesario = dialog.winfo_reqheight() + 40  # +40 de margen
        
        # Limitar tamaños máximos (opcional, para pantallas pequeñas)
        ancho_final = min(ancho_necesario, 800)  # Máximo 800 píxeles de ancho
        alto_final = min(alto_necesario, 600)   # Máximo 600 píxeles de alto
        
        # Centrar la ventana con el tamaño calculado
        centrar_ventana(dialog, ancho_final, alto_final) 
    # ===================================================================================================== 
    # Fuerza la actualización visual de la tabla de reservas
    # =====================================================================================================     
    def _forzar_actualizacion_tablas(self):
        
        try:
            # Forzar actualización de la tabla
            for item in self.reservas_tree.get_children():
                # Esto fuerza el refresco visual
                self.reservas_tree.item(item, values=self.reservas_tree.item(item, 'values'))
            self.reservas_tree.update_idletasks()
            self.reservas_tree.update()
            self.status_bar.config(text="✅ Tablas actualizadas correctamente")
        except Exception as e:
            print(f"Error en actualización forzada: {e}")
        
# ==================== PUNTO DE ENTRADA PRINCIPAL =========================================================
# Este bloque se ejecuta SOLO cuando el script se ejecuta directamente
# (no cuando se importa como módulo desde otro script)
# =========================================================================================================
if __name__ == "__main__":
    
    # __name__ es una variable especial de Python que vale "__main__" cuando el script
    # se ejecuta directamente, y vale el nombre del módulo cuando se importa.
    
    app = AplicacionFJ()  # Crea la instancia de la aplicación
    app.ejecutar()        # Inicia la aplicación (muestra la ventana)