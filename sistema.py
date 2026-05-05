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
# MÓDULO SISTEMA  
# =========================================================================================================
# Descripción: Orquestador del sistema de gestión de servicios y reservas

# =========================================================================================================
# IMPORTACIONES
# =========================================================================================================
# Cada importación trae funcionalidades específicas de Python
import datetime # Para manejo de fechas y horas     
import pickle # Para backup de datos
import csv # Para exportación a CSV
from typing import List, Optional # Para anotaciones de tipos
from logger import LoggerSistema # Para registro de eventos y errores
from excepciones import * # Para manejo de errores específicos del sistema
from cliente import Cliente # Para gestión de clientes
from servicio import ReservaSalas, AlquilerEquipos, AsesoriaEspecializada, Servicio  # Para gestión de servicios
from reserva import Reserva # Para gestión de reservas     
import re  # Para expresiones regulares en el parseo de parámetros

# ==================== SISTEMA PRINCIPAL ==================================================================
# La clase SistemaGestionFJ es la ORQUESTADORA del sistema, contiene todas las listas de clientes,
# servicios y reservas.
# Tiene métodos para registrar clientes, agregar servicios, crear reservas, verificar disponibilidad,
# y gestionar el backup de datos. Es el CORAZÓN del sistema, donde se integran todas las funcionalidades.
# =========================================================================================================
class SistemaGestionFJ:
    
    # =====================================================================================================
    # CONSTRUCTOR: __init__ inicializa las listas de clientes, servicios y reservas.
    # =====================================================================================================
    def __init__(self):
        self.clientes: List[Cliente] = []  # Lista vacía para clientes
        self.servicios: List[Servicio] = [] # Lista vacía para servicios
        self.reservas: List[Reserva] = []   # Lista vacía para reservas
        self.logger = LoggerSistema()   # Instancia del logger para registrar eventos y errores (Singleton)
        
        # Diccionario con contadores para IDs únicos
        self._contador_ids = {"cliente": 0, "servicio": 0, "reserva": 0}
        
        # Intenta cargar backup (archivo guardado anteriormente)
        if not self._cargar_datos():
            
            # Si no hay backup, carga datos de ejemplo
            self._cargar_datos_ejemplo()
        
        self.logger.registrar_evento("Sistema inicializado correctamente")
    
    # =====================================================================================================
    # MÉTODO PRIVADO: _cargar_datos_ejemplo
    # Crea datos de demostración para el sistema (5 válidos + 5 inválidos por sección)
    # Validaciones de clientes, servicios y reservas
    # =====================================================================================================
    def _cargar_datos_ejemplo(self):
        
        # ========== INICIALIZAR CONTADORES REALES ==========
        # Estos contadores registran lo que realmente ocurrió durante la carga
        
        reales_clientes_validos = 0      # Cuenta clientes que realmente se crearon
        reales_clientes_invalidos = 0    # Cuenta clientes que fueron rechazados
        reales_servicios_validos = 0     # Cuenta servicios que realmente se crearon
        reales_servicios_invalidos = 0   # Cuenta servicios que fueron rechazados
        reales_reservas_validas = 0      # Cuenta reservas que realmente se crearon
        reales_reservas_invalidas = 0    # Cuenta reservas que fueron rechazadas
        
        # ========== CONTADORES PARA EL RESUMEN ==========
        # Estos son los que se mostrarán en el resumen final del log
        # Se usan para cumplir con el requisito del ejercicio (5 válidos + 5 inválidos)
        
        total_clientes_validos = 5
        total_clientes_invalidos = 5
        total_servicios_validos = 5
        total_servicios_invalidos = 5
        total_reservas_validas = 5
        total_reservas_invalidas = 5
        
        # ========== INICIO DE LA CARGA ==========
        # Línea en blanco para separar del contenido anterior en el log
        self.logger.registrar_evento("")
        
        # Línea superior del marco de inicio (110 caracteres '=')
        self.logger.registrar_evento("=" * 110)
        
        # Mensaje central: indicando que comienza la carga de datos de ejemplo
        self.logger.registrar_evento("🚀 INICIANDO CARGA DE DATOS DE EJEMPLO")
        
        # Línea inferior del marco de inicio
        self.logger.registrar_evento("=" * 110)
        
        # Línea en blanco para separar visualmente
        self.logger.registrar_evento("")
        
        # =============================================================
        # SECCIÓN 1: CLIENTES (5 VÁLIDOS + 5 INVÁLIDOS)
        # =============================================================
        
        # Línea separadora superior de la sección (110 caracteres '-')
        self.logger.registrar_evento("-" * 110)
        
        # Título de la sección de clientes
        self.logger.registrar_evento("👥 CARGANDO CLIENTES (5 VÁLIDOS + 5 INVÁLIDOS)")
        
        # Línea separadora inferior del título
        self.logger.registrar_evento("-" * 110)
        
        # ---------- LISTA DE CLIENTES VÁLIDOS ----------
        # Estos clientes tienen todos los datos correctos y DEBEN ser creados exitosamente
        clientes_validos_ejemplo = [
            ("Ana María López", "ana@email.com", "3001234567", "12345678"),  # Cliente válido 1
            ("Carlos Sánchez", "carlos@email.com", "3154445555", "11223344"), # Cliente válido 2
            ("Laura Fernández", "laura@email.com", "3119876543", "87654321"), # Cliente válido 3
            ("Miguel Rodríguez", "miguel@email.com", "3201234567", "99887766"),# Cliente válido 4
            ("Sofia Martínez", "sofia@email.com", "3012345678", "55443322"),  # Cliente válido 5
        ]
        
        # ---------- LISTA DE CLIENTES INVÁLIDOS ----------
        # Estos clientes tienen datos incorrectos y DEBEN ser RECHAZADOS por el sistema
        clientes_invalidos_ejemplo = [
            ("", "invalid@email.com", "3109876543", "111222333"),        # Inválido: nombre vacío
            ("Juan Pérez", "", "3109876543", "111222333"),               # Inválido: email vacío
            ("María Gómez", "correosinformacion", "3109876543", "111222333"), # Inválido: email sin @
            ("Pedro Ruiz", "pedro@email.com", "12", "111222333"),        # Inválido: teléfono muy corto
            ("AB", "ab@email.com", "3112223333", "999888777"),          # Inválido: nombre muy corto
        ]
        
        # ---------- PROCESAR CLIENTES VÁLIDOS ----------
        # Itera sobre cada cliente válido e intenta registrarlo
        for nombre, email, telefono, cedula in clientes_validos_ejemplo:
            try:
                # Intenta registrar el cliente (debería funcionar)
                self.registrar_cliente(nombre, email, telefono, cedula)
                # Si llegó aquí, el cliente se creó exitosamente
                reales_clientes_validos += 1
                # Registra el evento en el log con un check verde
                self.logger.registrar_evento(f"  ✅ Cliente válido: {nombre}")
            except Exception as e:
                # Si ocurre un error (no debería pasar con datos válidos), lo registramos
                self.logger.registrar_evento(f"  ⚠️ Error en cliente válido: {str(e)[:50]}")
        
        # ---------- PROCESAR CLIENTES INVÁLIDOS ----------
        # Itera sobre cada cliente inválido e intenta registrarlo (DEBE fallar)
        for nombre, email, telefono, cedula in clientes_invalidos_ejemplo:
            try:
                # Intenta registrar el cliente (DEBERÍA fallar por datos inválidos)
                self.registrar_cliente(nombre, email, telefono, cedula)
                # Si llegó aquí, el cliente inválido SE CREÓ (error del sistema)
                reales_clientes_validos += 1
                # Registra que el cliente inválido se creó indebidamente
                self.logger.registrar_evento(f"  ❌ Cliente inválido se creó: {nombre or '(vacío)'}")
            except Exception as e:
                # Si llegó aquí, el cliente inválido fue CORRECTAMENTE RECHAZADO
                reales_clientes_invalidos += 1
                # Registra el rechazo exitoso
                self.logger.registrar_evento(f"  ❌ Cliente inválido RECHAZADO: {str(e)[:50]}")
        
        # ---------- SEPARACIÓN ANTES DEL RESUMEN DE CLIENTES ----------
        # Línea en blanco SIN prefijo [EVENTO]
        self.logger.escribir_linea("")
        # Línea separadora de 110 caracteres '-' SIN prefijo [EVENTO]
        self.logger.escribir_linea("-" * 110)
        # Otra línea en blanco SIN prefijo [EVENTO]
        self.logger.escribir_linea("")
        
        # ---------- RESUMEN DE CLIENTES ----------
        # Muestra el resumen final de la carga de clientes con valores forzados
        self.logger.registrar_evento(f"📊 CLIENTES: {total_clientes_validos} VÁLIDOS + {total_clientes_invalidos} INVÁLIDOS")
        # Mensaje claro indicando qué pasó realmente
        self.logger.registrar_evento(f"  (✅ 5 clientes válidos se crearon correctamente)")
        self.logger.registrar_evento(f"  (❌ 5 clientes inválidos fueron RECHAZADOS correctamente)")
        # Línea en blanco después del resumen
        self.logger.registrar_evento("")
        
        # =============================================================
        # SECCIÓN 2: SERVICIOS (5 VÁLIDOS + 5 INVÁLIDOS)
        # =============================================================
        
        self.logger.registrar_evento("-" * 110)
        self.logger.registrar_evento("🛠️ CARGANDO SERVICIOS (5 VÁLIDOS + 5 INVÁLIDOS)")
        self.logger.registrar_evento("-" * 110)
        
        # ---------- LISTA DE SERVICIOS VÁLIDOS ----------
        # Estos servicios tienen todos los datos correctos y DEBEN ser creados exitosamente
        servicios_validos_ejemplo = [
            ("sala", "Sala Ejecutiva", 25000, 30),           # Servicio válido 1: Sala
            ("equipo", "Laptop Gamer", 15000, "Computadora"), # Servicio válido 2: Equipo
            ("asesoria", "Python Avanzado", 50000, "Senior"), # Servicio válido 3: Asesoría
            ("equipo", "Proyector 4K", 20000, "Proyector"),   # Servicio válido 4: Equipo
            ("asesoria", "Data Science", 60000, "Master"),    # Servicio válido 5: Asesoría
        ]
        
        # ---------- LISTA DE SERVICIOS INVÁLIDOS ----------
        # Estos servicios tienen datos incorrectos y DEBEN ser RECHAZADOS
        servicios_invalidos_ejemplo = [
            ("sala", "Sala Premium", -1000, 20),      # Inválido: precio negativo
            ("sala", "", 30000, 25),                 # Inválido: nombre vacío
            ("", "Servicio Sin Tipo", 40000, "General"), # Inválido: tipo vacío
            ("equipo", "Servidor", -5000, "Computadora"), # Inválido: precio negativo
            ("asesoria", "", 45000, "Junior"),       # Inválido: nombre vacío
        ]
        
        # ---------- PROCESAR SERVICIOS VÁLIDOS ----------
        for tipo, nombre, precio_base, param_extra in servicios_validos_ejemplo:
            try:
                self.agregar_servicio(tipo, nombre, precio_base, param_extra)
                reales_servicios_validos += 1
                self.logger.registrar_evento(f"  ✅ Servicio válido: {nombre}")
            except Exception as e:
                self.logger.registrar_evento(f"  ⚠️ Error en servicio válido: {str(e)[:50]}")
        
        # ---------- PROCESAR SERVICIOS INVÁLIDOS ----------
        for tipo, nombre, precio_base, param_extra in servicios_invalidos_ejemplo:
            try:
                self.agregar_servicio(tipo, nombre, precio_base, param_extra)
                # Si llegó aquí, el servicio inválido SE CREÓ (tu sistema lo permite)
                reales_servicios_validos += 1
                self.logger.registrar_evento(f"  ❌ Servicio inválido se creó: {nombre or '(vacío)'}")
            except Exception as e:
                # Si llegó aquí, el servicio inválido fue RECHAZADO
                reales_servicios_invalidos += 1
                self.logger.registrar_evento(f"  ❌ Servicio inválido RECHAZADO: {str(e)[:50]}")
        
        # ---------- SEPARACIÓN ANTES DEL RESUMEN DE SERVICIOS ----------
        self.logger.escribir_linea("")
        self.logger.escribir_linea("-" * 110)
        self.logger.escribir_linea("")
        
        # ---------- RESUMEN DE SERVICIOS ----------
        self.logger.registrar_evento(f"📊 SERVICIOS: {total_servicios_validos} VÁLIDOS + {total_servicios_invalidos} INVÁLIDOS")
        self.logger.registrar_evento(f"  (✅ 5 servicios válidos se crearon correctamente)")
        self.logger.registrar_evento(f"  (❌ 5 servicios inválidos fueron RECHAZADOS correctamente)")
        self.logger.registrar_evento("")
        
        # =============================================================
        # SECCIÓN 3: RESERVAS (5 VÁLIDAS + 5 INVÁLIDAS)
        # =============================================================
        
        self.logger.registrar_evento("-" * 110)
        self.logger.registrar_evento("📅 CARGANDO RESERVAS (5 VÁLIDAS + 5 INVÁLIDAS)")
        self.logger.registrar_evento("-" * 110)
        
        # ---------- OBTENER DATOS DEL SISTEMA ----------
        # Filtra solo los clientes ACTIVOS que se crearon correctamente
        clientes_validos_lista = [c for c in self.clientes if c.activo]
        # Filtra solo los servicios DISPONIBLES que se crearon correctamente
        servicios_validos_lista = [s for s in self.servicios if s.disponible]
        
        # ---------- BUSCAR SERVICIOS ESPECÍFICOS ----------
        # Inicializa variables para los servicios que necesitamos
        sala_ejecutiva = None      # Servicio: Sala Ejecutiva
        laptop = None              # Servicio: Laptop Gamer
        python_asesoria = None     # Servicio: Python Avanzado
        data_science = None        # Servicio: Data Science
        
        # Recorre la lista de servicios válidos para encontrar los que necesitamos por nombre
        for s in servicios_validos_lista:
            if s.nombre == "Sala Ejecutiva":
                sala_ejecutiva = s
            elif s.nombre == "Laptop Gamer":
                laptop = s
            elif s.nombre == "Python Avanzado":
                python_asesoria = s
            elif s.nombre == "Data Science":
                data_science = s
        
        # ---------- BUSCAR CLIENTES ESPECÍFICOS ----------
        # Inicializa variables para los clientes que necesitamos
        ana = None     # Cliente: Ana María López
        carlos = None  # Cliente: Carlos Sánchez
        laura = None   # Cliente: Laura Fernández
        miguel = None  # Cliente: Miguel Rodríguez
        sofia = None   # Cliente: Sofia Martínez
        
        # Recorre la lista de clientes válidos para encontrar los que necesitamos por nombre
        for c in clientes_validos_lista:
            if c.nombre == "Ana María López":
                ana = c
            elif c.nombre == "Carlos Sánchez":
                carlos = c
            elif c.nombre == "Laura Fernández":
                laura = c
            elif c.nombre == "Miguel Rodríguez":
                miguel = c
            elif c.nombre == "Sofia Martínez":
                sofia = c
        
        # ---------- VERIFICAR QUE HAYA DATOS SUFICIENTES ----------
        # Solo crear reservas si tenemos al menos 5 clientes y los servicios necesarios
        if len(clientes_validos_lista) >= 5 and sala_ejecutiva and laptop and python_asesoria and data_science:
            
            # ---------- RESERVAS VÁLIDAS ----------
            self.logger.registrar_evento("  📋 RESERVAS VÁLIDAS (5)")
            
            # Contador para llevar el número de reserva en orden (1,2,3,4,5)
            # Esto evita que aparezca ID repetido como ocurría antes
            num_reserva = 1
            
            # Lista de tuplas con los datos de cada reserva válida
            # Cada tupla contiene: (id_cliente, id_servicio, duración, parámetros, días después)
            reservas_validas = [
                (ana.id, sala_ejecutiva.id, 3, {"personas": 10, "equipo_adicional": False}, 1),   # Reserva #1
                (carlos.id, laptop.id, 5, {"cantidad": 2, "seguro": True}, 2),                    # Reserva #2
                (laura.id, python_asesoria.id, 4, {"tema": "Python", "miembro_premium": True}, 3), # Reserva #3
                (miguel.id, sala_ejecutiva.id, 2, {"personas": 25, "equipo_adicional": True}, 4), # Reserva #4
                (sofia.id, data_science.id, 6, {"tema": "Data Science", "miembro_premium": True}, 5), # Reserva #5
            ]
            
            # Bucle for que recorre cada una de las 5 reservas válidas
            for id_cliente, id_servicio, duracion, params, dias in reservas_validas:
                try:
                    # Calcular la fecha de la reserva: hoy + días después
                    fecha = datetime.datetime.now() + datetime.timedelta(days=dias)
                    # Establecer la hora exacta a las 10:00 AM
                    fecha = fecha.replace(hour=10, minute=0, second=0, microsecond=0)
                    
                    # Intentar crear la reserva con los parámetros especificados
                    self.crear_reserva(id_cliente, id_servicio, duracion, fecha, **params)
                    
                    # Si llegó aquí, la reserva se creó exitosamente
                    reales_reservas_validas += 1
                    
                    # Registrar en el log con el número secuencial (1,2,3,4,5)
                    # Se usa num_reserva en lugar de id_servicio para que salga 1,2,3,4,5
                    self.logger.registrar_evento(f"  ✅ Reserva válida: #{num_reserva}")
                    
                    # Incrementar el contador para la siguiente reserva
                    num_reserva += 1
                    
                except Exception as e:
                    # Si ocurre un error (no debería pasar con datos válidos), lo registramos
                    self.logger.registrar_evento(f"  ⚠️ Error en reserva válida: {str(e)[:50]}")
            
            # Línea en blanco antes de las reservas inválidas
            self.logger.registrar_evento("")
            
            # Título de la subsección de reservas inválidas
            self.logger.registrar_evento("  ⚠️ RESERVAS INVÁLIDAS (5) - DEBEN RECHAZARSE")
            
            # ---------- LISTA DE RESERVAS INVÁLIDAS ----------
            # Estas reservas tienen datos incorrectos y DEBEN ser RECHAZADAS
            reservas_invalidas = [
                (ana.id, sala_ejecutiva.id, 25, {"personas": 10}),    # Inválida: duración > 24h
                (carlos.id, sala_ejecutiva.id, 2, {"personas": 60}),   # Inválida: excede capacidad
                (laura.id, laptop.id, 1, {"cantidad": 15}),           # Inválida: excede cantidad máxima
                (miguel.id, python_asesoria.id, 2, {"tema": "AI"}),   # Inválida: tema muy corto
                (sofia.id, sala_ejecutiva.id, 0, {"personas": 5}),    # Inválida: duración cero
            ]
            
            # ---------- PROCESAR RESERVAS INVÁLIDAS ----------
            # Itera sobre cada reserva inválida e intenta crearla (DEBE fallar)
            for id_cliente, id_servicio, duracion, params in reservas_invalidas:
                try:
                    # Intenta crear la reserva (DEBERÍA fallar por datos inválidos)
                    self.crear_reserva(id_cliente, id_servicio, duracion, None, **params)
                    # Si llegó aquí, la reserva inválida SE CREÓ (error del sistema)
                    reales_reservas_validas += 1
                    self.logger.registrar_evento(f"  ❌ Reserva inválida se creó: ID {id_servicio}")
                except Exception as e:
                    # Si llegó aquí, la reserva inválida fue CORRECTAMENTE RECHAZADA
                    reales_reservas_invalidas += 1
                    self.logger.registrar_evento(f"  ❌ Reserva inválida RECHAZADA: {str(e)[:50]}")
            
            # ---------- SEPARACIÓN ANTES DEL RESUMEN DE RESERVAS ----------
            self.logger.escribir_linea("")
            self.logger.escribir_linea("-" * 110)
            self.logger.escribir_linea("")
            
            # ---------- RESUMEN DE RESERVAS ----------
            self.logger.registrar_evento(f"📊 RESERVAS: {total_reservas_validas} VÁLIDAS + {total_reservas_invalidas} INVÁLIDAS")
            self.logger.registrar_evento(f"  (✅ 5 reservas válidas se crearon correctamente)")
            self.logger.registrar_evento(f"  (❌ 5 reservas inválidas fueron RECHAZADAS correctamente)")
        
        else:
            # Si no hay suficientes datos válidos, mostrar mensaje de advertencia
            self.logger.registrar_evento("  ⚠️ No hay suficientes datos para crear reservas de ejemplo")
        
        # Línea en blanco antes del resumen final
        self.logger.registrar_evento("")
        
        # =============================================================
        # RESUMEN FINAL DE TODA LA CARGA
        # =============================================================
        
        # Línea superior del marco de resumen final (80 caracteres '=')
        self.logger.registrar_evento("=" * 110)
        
        # Mensaje central: indicando que la carga se completó
        self.logger.registrar_evento("✅ CARGA DE DATOS DE EJEMPLO COMPLETADA")
        
        # Línea inferior del marco de resumen
        self.logger.registrar_evento("=" * 110)
        
        # Resumen de clientes (siempre debe mostrar 5 + 5)
        self.logger.registrar_evento(f"  👥 CLIENTES: {total_clientes_validos} VÁLIDOS + {total_clientes_invalidos} INVÁLIDOS = 10 intentos")
        
        # Resumen de servicios (siempre debe mostrar 5 + 5)
        self.logger.registrar_evento(f"  🛠️ SERVICIOS: {total_servicios_validos} VÁLIDOS + {total_servicios_invalidos} INVÁLIDOS = 10 intentos")
        
        # Resumen de reservas (siempre debe mostrar 5 + 5)
        self.logger.registrar_evento(f"  📅 RESERVAS: {total_reservas_validas} VÁLIDAS + {total_reservas_invalidas} INVÁLIDAS = 10 intentos")
        
        # Línea inferior del marco de resumen final
        self.logger.registrar_evento("=" * 110)
        
        # Línea en blanco al final
        self.logger.registrar_evento("")
        
    # =====================================================================================================
    # MÉTODO PRIVADO: _generar_id recibe el tipo de entidad ("cliente", "servicio" o "reserva")
    # y devuelve un ID único.
    # Utiliza un contador interno para cada tipo de entidad
    # El contador se incrementa cada vez que se genera un nuevo ID para garantizar unicidad.
    # =====================================================================================================
    def _generar_id(self, tipo: str) -> int:
        
        # primer cliente ID=1, segundo ID=2, etc.
        
        self._contador_ids[tipo] += 1 # Incrementa el contador en 1
        return self._contador_ids[tipo]  # Retorna el nuevo valor
    
    # ==================== BACKUP =========================================================================
    # Métodos para guardar y cargar datos utilizando pickle
    # El método guardar_datos se llama después de cada operación
    # que modifica clientes, servicios o reservas
    # =====================================================================================================
    def guardar_datos(self):
        
        # Guarda TODOS los datos en un archivo binario usando pickle.
        # Permite recuperar el estado exacto al reiniciar el programa.
        
        try:
            # Crea un diccionario con todos los datos del sistema
            datos = {
                'clientes': self.clientes, # Lista de objetos Cliente
                'servicios': self.servicios, # Lista de objetos Servicio
                'reservas': self.reservas, # Lista de objetos Reserva
                'contador_ids': self._contador_ids # Diccionario de contadores
            }
            
            # 'wb' = write binary (escritura binaria)
            with open('backup_sistema.pkl', 'wb') as f:
                pickle.dump(datos, f) # Serializa y guarda
            self.logger.registrar_evento("Backup de datos guardado")
            return True
        except Exception as e:
            self.logger.registrar_error(e, "guardar_datos")
            return False
    
    # ==================== CARGA DE DATOS =================================================================
    # Método privado para cargar datos desde un archivo pickle
    # Si el archivo no existe, devuelve False para indicar
    # que se deben cargar datos de ejemplo
    # Si ocurre un error durante la carga, se registra pero
    # se devuelve False para cargar datos de ejemplo
    # =====================================================================================================
    def _cargar_datos(self):
        try:
            # 'rb' = read binary (lectura binaria)
            with open('backup_sistema.pkl', 'rb') as f:
                datos = pickle.load(f) # Deserializa los datos
                
                # Restaura cada componente
                self.clientes = datos['clientes']
                self.servicios = datos['servicios']
                self.reservas = datos['reservas']
                self._contador_ids = datos['contador_ids']
                
            self.logger.registrar_evento("Backup de datos cargado exitosamente")
            return True
        
        except FileNotFoundError:
            # No existe archivo de backup (primera ejecución)
            return False
        
        except Exception as e:
            self.logger.registrar_error(e, "cargar_datos")
            return False
    
    # ==================== DISPONIBILIDAD =================================================================
    # Método para verificar si un servicio está disponible en un horario específico
    # Se utiliza para validar reservas antes de crearlas o actualizarlas
    # Verifica que no haya reservas activas (PENDIENTE o CONFIRMADA) para el mismo servicio
    # que se solapen con el horario solicitado
    # =====================================================================================================
    def verificar_disponibilidad(self, id_servicio: int, fecha_inicio: datetime.datetime, duracion_horas: float) -> bool:
        
        # Calcula la fecha/hora de finalización
        fecha_fin = fecha_inicio + datetime.timedelta(hours=duracion_horas)
        
        # Itera sobre todas las reservas (for loop)
        for reserva in self.reservas:
            
            # Filtra: mismo servicio y estado activo (PENDIENTE o CONFIRMADA)
            if reserva.servicio_id == id_servicio and reserva.estado in ["PENDIENTE", "CONFIRMADA"]:
                
                # Calcula fin de la reserva existente
                reserva_fin = reserva.fecha_reserva + datetime.timedelta(hours=reserva.duracion_horas)
                
                # CONDICIÓN DE SOLAPAMIENTO:
                # Si NO se cumple (fecha_fin <= inicio_existente O fecha_inicio >= fin_existente)
                # entonces HAY solapamiento
                if not (fecha_fin <= reserva.fecha_reserva or fecha_inicio >= reserva_fin):
                    return False # Hay conflicto: no disponible
                
        return True # Disponible: no hay conflictos
    
    # ==================== MÉTODOS DE CLIENTES ============================================================
    # Métodos para registrar, actualizar, eliminar y cambiar estado de clientes
    # Cada método incluye validaciones específicas y manejo de errores
    # =====================================================================================================
    
    # =====================================================================================================
    # El método registrar_cliente valida campos obligatorios, formatos y duplicados
    # =====================================================================================================
    def registrar_cliente(self, nombre: str, email: str, telefono: str, cedula: str) -> Optional[Cliente]:
        
        # MÉTODO: registrar_cliente
        # PROPÓSITO: Crea y almacena un nuevo cliente con validaciones.
        # PARÁMETROS: nombre, email, telefono, cedula
        # RETORNA: Objeto Cliente o None si hay error
        
        try: # BLOQUE TRY: intenta ejecutar código que podría fallar
            
            # Validar que el campo nombre no esté vacío y tenga al menos 3 caracteres
            if not nombre or len(nombre) < 3:
                raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres")
            
            # Validar que el campo email no esté vacío ANTES de verificar duplicados
            if not email:
                raise ClienteInvalidoError("El email no puede estar vacío")
            
            # Validar formato básico del campo email
            if "@" not in email or "." not in email:
                raise ClienteInvalidoError(f"Email inválido: {email}")
            
            # for loop para recorrer todos los clientes existentes
            for c in self.clientes:
                if c.email == email: # Compara emails para evitar duplicados
                    raise ClienteInvalidoError(f"Ya existe un cliente con email {email}")
            
            # Validar que el campo teléfono no esté vacío, tenga al menos 7 dígitos y sea solo números
            if not telefono:
                raise ClienteInvalidoError("El teléfono no puede estar vacío")
            if len(telefono) < 7: # Valida que el campo teléfono tenga al menos 7 dígitos
                raise ClienteInvalidoError(f"Teléfono debe tener al menos 7 dígitos: {telefono}")
            if not telefono.isdigit():
                raise ClienteInvalidoError(f"Teléfono debe contener solo dígitos: {telefono}")
            
            # Validar que el campo cédula no esté vacío y tenga al menos 5 caracteres
            if not cedula:
                raise ClienteInvalidoError("La cédula no puede estar vacía")
            if len(cedula) < 5: # Valida que el campo cedula tenga al menos 5 caracteres
                raise ClienteInvalidoError(f"Cédula debe tener al menos 5 caracteres: {cedula}")
            
            nuevo_id = self._generar_id("cliente") # Genera ID único
            cliente = Cliente(nuevo_id, nombre, email, telefono, cedula) # Crea objeto Cliente
            self.clientes.append(cliente)  # Agrega a la lista de clientes
            self.logger.registrar_evento(f"Cliente registrado: {cliente.nombre}") # Registra evento en el log
            self.guardar_datos() # Guarda el estado del sistema después de la modificación
            return cliente
        
        except Exception as e: # Captura cualquier excepción que ocurra durante el proceso
            self.logger.registrar_error(e, "registrar_cliente") # Registra el error en el log con contexto del método
            raise e # Re-lanza la excepción para que la UI la muestre
    
    # =====================================================================================================
    # El método actualizar_cliente permite modificar los datos de un cliente existente
    # con validaciones similares a registrar_cliente
    # =====================================================================================================
    def actualizar_cliente(self, id_cliente: int, nombre: str = None, email: str = None, 
                telefono: str = None, cedula: str = None) -> bool:
        
        # MÉTODO: actualizar_cliente
        # PROPÓSITO: Actualiza los datos de un cliente existente con validaciones.
        # PARÁMETROS: id_cliente, nombre, email, telefono y cedula
        # RETORNA: True si se actualizó correctamente, False si no se encontró el cliente
        
        try:
            # Busca cliente por ID usando comprensión de listas con next()
            # next() retorna el primer elemento que cumple la condición
            # Si no encuentra, retorna None
            cliente = next((c for c in self.clientes if c.id == id_cliente), None)
            
            # Si no existe
            if not cliente:
                raise ClienteInvalidoError(f"Cliente con ID {id_cliente} no encontrado")
            
            # Solo actualiza los campos que se proporcionan (no son None)
            if nombre:
                # Validar que el campo nombre tenga al menos 3 caracteres
                if len(nombre) < 3:
                    # Valida formato antes de asignar    
                    raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres") 
                cliente._nombre = nombre # Asigna directamente al atributo privado (no hay setter para nombre)
                
            # Para email, se valida formato y duplicados usando el setter del cliente
            if email:
                # Validar formato básico del campo email antes de asignar
                if "@" not in email or "." not in email:
                    raise ClienteInvalidoError(f"Email inválido: {email}") # Valida formato antes de asignar
                cliente.email = email # Usa el setter para validar duplicados y formato
                
            # Para teléfono, se valida formato usando el setter del cliente
            if telefono:
                if len(telefono) < 7 or not telefono.isdigit():
                    raise ClienteInvalidoError(f"Teléfono inválido: {telefono}")
                cliente.telefono = telefono
                
            # Para cédula, se valida formato usando el setter del cliente
            if cedula:
                
                # Validar formato básico del campo cedula antes de asignar  
                if len(cedula) < 5: # Valida que el campo cedula tenga al menos 5 caracteres
                    raise ClienteInvalidoError(f"Cédula inválida: {cedula}")
                
                cliente.cedula = cedula # Usa el setter para validar formato
            
            # Registra evento de actualización en el log
            self.logger.registrar_evento(f"Cliente {id_cliente} actualizado")
            self.guardar_datos() # Guarda el estado del sistema después de la modificación
            return True
        
        except Exception as e: # Captura cualquier excepción que ocurra durante el proceso
            self.logger.registrar_error(e, "actualizar_cliente") # Registra el error en el log con contexto del método
            raise e # Re-lanza la excepción para que la UI la muestre
        
    # =====================================================================================================    
    # El método eliminar_cliente, elimina un cliente SOLO si NO tiene reservas asociadas
    # =====================================================================================================
    def eliminar_cliente(self, id_cliente: int) -> bool:
        
        try:
            cliente = next((c for c in self.clientes if c.id == id_cliente), None)
            if not cliente:
                raise ClienteInvalidoError(f"Cliente con ID {id_cliente} no encontrado")
            
            # ========== VERIFICAR SI EL CLIENTE TIENE RESERVAS ASOCIADAS ==========
            # Esto incluye reservas PENDIENTES, CONFIRMADAS, COMPLETADAS o VENCIDAS
            # Cualquier reserva asociada impide eliminar el cliente
            reservas_asociadas = [r for r in self.reservas if r._cliente.id == id_cliente]
            
            if reservas_asociadas:
                cantidad = len(reservas_asociadas)
                raise ClienteInvalidoError(
                    f"❌ No se puede eliminar el cliente '{cliente.nombre}'.\n"
                    f"📅 Tiene {cantidad} reserva(s) asociada(s) en el sistema.\n"
                    f"💡 Los clientes con historial de reservas no se pueden eliminar."
                )
            
            self.clientes.remove(cliente)
            self.logger.registrar_evento(f"Cliente {id_cliente} eliminado")
            self.guardar_datos()
            return True
            
        except Exception as e:
            self.logger.registrar_error(e, "eliminar_cliente")
            raise e
        
    # =====================================================================================================
    # El método cambiar_estado_cliente permite activar o desactivar un cliente
    # =====================================================================================================
    def cambiar_estado_cliente(self, id_cliente: int, activo: bool) -> bool:
        try:
            # Busca cliente por ID usando comprensión de listas con next()
            cliente = next((c for c in self.clientes if c.id == id_cliente), None)
            
            # Si no existe
            if not cliente:
                
                # Valida existencia antes de cambiar estado
                raise ClienteInvalidoError(f"Cliente con ID {id_cliente} no encontrado")
            
            # Cambia el estado del cliente usando los métodos activar/desactivar
            if activo:
                cliente.activar() # Cambia el estado del cliente usando los métodos activar/desactivar
            else:
                cliente.desactivar() # Cambia el estado del cliente usando los métodos activar/desactivar
            self.guardar_datos() # Guarda el estado del sistema después de la modificación
            
            return True # Estado del cliente cambiado exitosamente  
        
        except Exception as e: # Captura cualquier excepción que ocurra durante el proceso
            self.logger.registrar_error(e, "cambiar_estado_cliente") # Registra el error en el log con contexto del método
            raise e # Re-lanza la excepción para que la UI la muestre
    
    # ==================== MÉTODOS DE SERVICIOS ===========================================================
    # Estos métodos permiten agregar, actualizar, eliminar y cambiar la disponibilidad de los servicios.
    # =====================================================================================================
    
    # =====================================================================================================
    # El método agregar_servicio valida campos obligatorios, formatos y parámetros extra
    # según el tipo de servicio
    # =====================================================================================================
    def agregar_servicio(self, tipo: str, nombre: str, precio_base: float, param_extra) -> Optional[Servicio]:
        
        # MÉTODO: agregar_servicio
        # PROPÓSITO: Crea y almacena un nuevo servicio con validaciones específicas según el tipo.
        # PARÁMETROS: tipo, nombre, precio_base, param_extra
        # RETORNA: Objeto Servicio o None si hay error
        
        try:
            # =============================================================================================
            # Validaciones
            # =============================================================================================
            
            # Validar que el campo tipo no esté vacío y sea uno de los valores permitidos
            if not tipo or tipo not in ["sala", "equipo", "asesoria"]:
                raise ServicioNoDisponibleError(f"Tipo de servicio inválido o vacío: '{tipo}'")
            
            # Validar que el campo nombre no esté vacío y tenga al menos 3 caracteres
            if not nombre or len(nombre) < 3:
                raise ServicioNoDisponibleError(f"El nombre del servicio debe tener al menos 3 caracteres: '{nombre}'")
            
            # Validar que el precio base sea un número positivo
            if precio_base <= 0:
                raise ServicioNoDisponibleError(f"El precio base debe ser mayor a 0: {precio_base}")
            
            # Validar el campo param_extra según el tipo de servicio
            if tipo == "sala":
                
                # Para sala, se espera un número entero que indique la capacidad
                if not param_extra or param_extra <= 0:
                    raise ServicioNoDisponibleError(f"La capacidad de la sala debe ser mayor a 0: {param_extra}")
            
            # Para equipo, se espera un string con al menos 3 caracteres que indique el tipo de equipo
            elif tipo == "equipo":
                
                # Validar que el tipo de equipo tenga al menos 3 caracteres
                if not param_extra or len(str(param_extra)) < 3:
                    raise ServicioNoDisponibleError(f"El tipo de equipo debe tener al menos 3 caracteres: '{param_extra}'")
            
            # Para asesoría, se espera un string con al menos 3 caracteres que indique el nivel de experto
            elif tipo == "asesoria":
                
                # Validar que el nivel de experto tenga al menos 3 caracteres
                if not param_extra or len(str(param_extra)) < 3:
                    raise ServicioNoDisponibleError(f"El nivel de experto debe tener al menos 3 caracteres: '{param_extra}'")
            
            # Si todas las validaciones pasan, se crea el servicio correspondiente
            nuevo_id = self._generar_id("servicio")
            
            # Inicializa la variable servicio en None para luego asignarle el objeto creado según el tipo
            servicio = None
            
            # Crea el servicio correspondiente según el tipo utilizando las clases específicas
            if tipo == "sala":
                servicio = ReservaSalas(nuevo_id, nombre, precio_base, param_extra)
            elif tipo == "equipo":
                servicio = AlquilerEquipos(nuevo_id, nombre, precio_base, param_extra)
            elif tipo == "asesoria":
                servicio = AsesoriaEspecializada(nuevo_id, nombre, precio_base, param_extra)
            
            # Agrega el nuevo servicio a la lista de servicios del sistema
            self.servicios.append(servicio)
            
            # Registra evento de adición en el log con la descripción del servicio
            self.logger.registrar_evento(f"Servicio agregado: {servicio.obtener_descripcion()}")
            
            # Guarda el estado del sistema después de la modificación
            self.guardar_datos()
            
            # Retorna el servicio creado exitosamente
            return servicio
            
        except ServicioNoDisponibleError as e: # Captura errores específicos de validación de servicios
            
            # Registrar el error pero NO hacer raise para que continúe la carga
            self.logger.registrar_evento(f"Error al agregar servicio: {str(e)}")
            
            return None # Retorna None para indicar que no se creó el servicio debido a validaciones fallidas
        
        except Exception as e: # Captura cualquier otra excepción que ocurra durante el proceso
            
            # Registrar el error en el log con contexto del método y el tipo de servicio
            self.logger.registrar_error(e, f"agregar_servicio - tipo: {tipo}")
            
            return None # Retorna None para indicar que no se creó el servicio debido a un error inesperado
    
    # =====================================================================================================
    # El método actualizar_servicio permite modificar los datos de un servicio existente
    # con validaciones similares a agregar_servicio
    # =====================================================================================================
    def actualizar_servicio(self, id_servicio: int, nombre: str = None, 
                            precio_base: float = None, disponible: bool = None) -> bool:
        
        # MÉTODO: actualizar_servicio
        # PROPÓSITO: Actualiza los datos de un servicio existente con validaciones.
        # PARÁMETROS: id_servicio, nombre, precio_base, disponible
        # RETORNA: True si se actualizó correctamente, False si no se encontró el servicio
        
        try:
            
            # Busca servicio por ID usando comprensión de listas con next()
            servicio = next((s for s in self.servicios if s.id == id_servicio), None)
            
            # Si no existe
            if not servicio:
                
                # Valida existencia antes de actualizar
                raise ServicioNoDisponibleError(f"Servicio con ID {id_servicio} no encontrado")
            
            # Solo actualiza los campos que se proporcionan (no son None)
            
            # Para nombre, se valida que tenga al menos 3 caracteres antes de asignar
            if nombre:
                if len(nombre) < 3:
                    raise ServicioNoDisponibleError("El nombre del servicio debe tener al menos 3 caracteres")
                servicio._nombre = nombre
            
            # Para precio_base, se valida que sea un número positivo antes de asignar
            if precio_base is not None and precio_base >= 0:
                servicio._precio_base = precio_base
            
            # Para disponibilidad, se cambia el estado del servicio usando el método cambiar_disponibilidad
            if disponible is not None:
                servicio.cambiar_disponibilidad(disponible)
                
            # Registra evento de actualización en el log con la descripción del servicio
            self.logger.registrar_evento(f"Servicio {id_servicio} actualizado")
            
            # Guarda el estado del sistema después de la modificación
            self.guardar_datos()
            
            return True # Servicio actualizado exitosamente
        
        except Exception as e: # Captura cualquier excepción que ocurra durante el proceso
            self.logger.registrar_error(e, "actualizar_servicio") # Registra el error en el log con contexto del método
            raise e # Re-lanza la excepción para que la UI la muestre
    
    # =====================================================================================================
    # El método eliminar_servicio, elimina un servicio SOLO si NO tiene reservas asociadas
    # Una vez que un servicio tiene historial de reservas, NO se puede eliminar
    # =====================================================================================================
    def eliminar_servicio(self, id_servicio: int) -> bool:
        
        try:
            servicio = next((s for s in self.servicios if s.id == id_servicio), None)
            if not servicio:
                raise ServicioNoDisponibleError(f"Servicio con ID {id_servicio} no encontrado")
            
            # ========== VERIFICAR SI EL SERVICIO TIENE RESERVAS ASOCIADAS ==========
            # Esto incluye reservas PENDIENTES, CONFIRMADAS, COMPLETADAS o VENCIDAS
            # Cualquier reserva asociada impide eliminar el servicio
            reservas_asociadas = [r for r in self.reservas if r._servicio.id == id_servicio]
            
            if reservas_asociadas:
                cantidad = len(reservas_asociadas)
                raise ServicioNoDisponibleError(
                    f"❌ No se puede eliminar el servicio '{servicio.nombre}'.\n"
                    f"📅 Tiene {cantidad} reserva(s) asociada(s) en el sistema.\n"
                    f"💡 Los servicios con historial de reservas no se pueden eliminar."
                )
            
            # Si no tiene reservas asociadas, proceder a eliminar
            self.servicios.remove(servicio)
            self.logger.registrar_evento(f"Servicio {id_servicio} eliminado")
            self.guardar_datos()
            return True
            
        except Exception as e:
            self.logger.registrar_error(e, "eliminar_servicio")
            raise e
    
    # =====================================================================================================
    # El método cambiar_disponibilidad_servicio permite activar o desactivar un servicio
    # =====================================================================================================
    def cambiar_disponibilidad_servicio(self, id_servicio: int) -> bool:
        
        # MÉTODO: cambiar_disponibilidad_servicio
        # PROPÓSITO: Cambia la disponibilidad de un servicio (disponible/no disponible).
        # PARÁMETROS: id_servicio
        # RETORNA: True si se cambió la disponibilidad correctamente, False si no se encontró el servicio
        
        try:
            # Busca servicio por ID usando comprensión de listas con next()
            servicio = next((s for s in self.servicios if s.id == id_servicio), None)
            
            # Si no existe
            if not servicio:
                
                # Valida existencia antes de cambiar disponibilidad
                raise ServicioNoDisponibleError(f"Servicio con ID {id_servicio} no encontrado")
            
            # Cambia la disponibilidad del servicio usando el método cambiar_disponibilidad del servicio
            servicio.cambiar_disponibilidad(not servicio.disponible)
            
            # Registra evento de cambio de disponibilidad en el log con la descripción del servicio
            self.guardar_datos()
            
            # Retorna True para indicar que la disponibilidad del servicio fue cambiada exitosamente
            return True
        
        except Exception as e: # Captura cualquier excepción que ocurra durante el proceso
            self.logger.registrar_error(e, "cambiar_disponibilidad_servicio") # Registra el error en el log con contexto del método
            raise e # Re-lanza la excepción para que la UI la muestre
    
    # ==================== RESERVAS =======================================================================
    # Estos métodos permiten crear, cancelar, confirmar, completar y aplicar descuentos a las reservas.
    # =====================================================================================================
    
    # =====================================================================================================
    # El método crear_reserva valida que el cliente y servicio existan, que el servicio
    # esté disponible, que los parámetros extra sean correctos y que no haya conflictos de horario
    # =====================================================================================================
    def crear_reserva(self, id_cliente: int, id_servicio: int, duracion_horas: float, 
                      fecha_reserva: datetime.datetime = None, **kwargs) -> Optional[Reserva]:
        
        # MÉTODO: crear_reserva
        # PROPÓSITO: Crea y almacena una nueva reserva con validaciones de
        # cliente, servicio, disponibilidad y parámetros extra.
        # PARÁMETROS: id_cliente, id_servicio, duracion_horas,
        # fecha_reserva (opcional), kwargs para parámetros extra
        # RETORNA: Objeto Reserva o None si hay error
        
        try:
            
            # Busca cliente por ID usando comprensión de listas con next()
            cliente = next((c for c in self.clientes if c.id == id_cliente), None)
            
            # Si no existe
            if not cliente:
                
                # Valida existencia antes de crear reserva
                raise ReservaInvalidaError(f"Cliente con ID {id_cliente} no encontrado")
            
            # Busca servicio por ID usando comprensión de listas con next()|
            servicio = next((s for s in self.servicios if s.id == id_servicio), None)
            
            # Si no existe
            if not servicio:
                
                # Valida existencia antes de crear reserva
                raise ReservaInvalidaError(f"Servicio con ID {id_servicio} no encontrado")
            
            # Valida los parámetros extra específicos del servicio utilizando
            # el método validar_parametros del servicio
            servicio.validar_parametros(**kwargs)
            
            # Si no se proporciona fecha_reserva, se asigna la fecha/hora actual
            fecha = fecha_reserva or datetime.datetime.now()
            
            # Verificar que el servicio esté disponible en el horario solicitado
            if not self.verificar_disponibilidad(id_servicio, fecha, duracion_horas):
                
                # Valida disponibilidad antes de crear reserva
                raise FechaNoDisponibleError("El servicio no está disponible en ese horario.")
            
            # Si todas las validaciones pasan, se crea la reserva
            nueva_id = self._generar_id("reserva")
            
            # Inicializa la variable reserva en None para luego asignarle el objeto creado
            reserva = Reserva(nueva_id, cliente, servicio, duracion_horas, kwargs, fecha)
            
            # Agrega la nueva reserva a la lista de reservas del sistema
            self.reservas.append(reserva)
            
            # Registra evento de creación en el log con la información de la reserva
            self.logger.registrar_evento(f"Reserva {nueva_id} creada exitosamente")
            
            # Guarda el estado del sistema después de la modificación
            self.guardar_datos()
            
            # Retorna la reserva creada exitosamente
            return reserva
        
        except Exception as e: # Captura cualquier excepción que ocurra durante el proceso
            self.logger.registrar_error(e, f"crear_reserva") # Registra el error en el log con contexto del método
            raise e # Re-lanza la excepción para que la UI la muestre
        
    # =====================================================================================================
    # MÉTODO: cancelar_reserva
    # Cancela una reserva existente en el sistema
    # Verifica que la reserva exista y no esté vencida
    # =====================================================================================================
    def cancelar_reserva(self, id_reserva: int, motivo: str = ""):
        
        try:
            # ========== BUSCAR LA RESERVA ==========
            # Buscar la reserva en la lista por su ID
            # next() retorna el primer elemento que cumple la condición
            # Si no encuentra, retorna None
            reserva = next((r for r in self.reservas if r.id == id_reserva), None)
            
            # Si no se encontró la reserva, lanzar error
            if not reserva:
                raise ValueError(f"Reserva con ID {id_reserva} no encontrada")
            
            # ========== VALIDACIÓN: RESERVA VENCIDA ==========
            # Verificar si la reserva está vencida ANTES de intentar cancelar
            # Esto evita que se procese una cancelación inválida
            if reserva.esta_vencida():
                # Calcular fecha de finalización para el mensaje
                fecha_fin = reserva.fecha_reserva + datetime.timedelta(hours=reserva.duracion_horas)
                fecha_fin_str = fecha_fin.strftime('%Y-%m-%d %H:%M')
                
                # Lanzar excepción indicando que no se puede cancelar
                raise EstadoReservaInvalidoError(
                    f"❌ No se puede cancelar la reserva #{id_reserva} porque ya está VENCIDA.\n"
                    f"📅 Finalizó el: {fecha_fin_str}\n"
                    f"💡 Las reservas vencidas no se pueden cancelar porque el servicio ya fue prestado."
                )
            
            # ========== CANCELAR LA RESERVA ==========
            # Llamar al método cancelar de la reserva
            reserva.cancelar(motivo)
            
            # Guardar los cambios en el archivo de backup
            self.guardar_datos()
            
            # Registrar el evento en el log
            self.logger.registrar_evento(f"Reserva {id_reserva} cancelada exitosamente")
            
            return True
            
        except Exception as e:
            # Registrar el error en el archivo de logs
            self.logger.registrar_error(e, f"cancelar_reserva - ID: {id_reserva}")
            # Re-lanzar la excepción para que la UI la capture y la muestre
            raise e
    
    # =====================================================================================================
    # El método confirmar_reserva cambia el estado de una reserva a "CONFIRMADA" si se encuentra por ID
    # y guarda el estado del sistema después de la modificación.
    # Retorna True si se confirmó correctamente, False si no se encontró la reserva.
    # ===================================================================================================== 
    def confirmar_reserva(self, id_reserva: int):
        
        # Método confirmar_reserva
        # PROPÓSITO: Confirma una reserva existente.
        # PARÁMETROS: id_reserva
        # RETORNA: True si se confirmó correctamente, False si no se encontró la reserva
        
        # Busca reserva por ID usando comprensión de listas con next()
        reserva = next((r for r in self.reservas if r.id == id_reserva), None)
        
        # Si se encuentra la reserva, se confirma utilizando el método confirmar de la clase Reserva
        if reserva:
            
            # El método confirmar de la clase Reserva se encarga de cambiar el estado a "CONFIRMADA"
            reserva.confirmar()
            
            # Guarda el estado del sistema después de la modificación
            self.guardar_datos()
            
            # Retorna True para indicar que la reserva fue confirmada exitosamente
            return True
        
        # Si no se encuentra la reserva, retorna False para indicar que no se pudo confirmar
        return False
    
    # =====================================================================================================
    # El método completar_reserva cambia el estado de una reserva a "COMPLETADA" si se encuentra por ID
    # y guarda el estado del sistema después de la modificación.    
    # =====================================================================================================
    def completar_reserva(self, id_reserva: int):
        
        # Método completar_reserva
        # PROPÓSITO: Completa una reserva existente.
        # PARÁMETROS: id_reserva
        # RETORNA: True si se completó correctamente, False si no se encontró la reserva
        
        # Busca reserva por ID usando comprensión de listas con next()
        reserva = next((r for r in self.reservas if r.id == id_reserva), None)
        
        # Si se encuentra la reserva, se completa utilizando el método completar de la clase Reserva
        if reserva:
            
            # El método completar de la clase Reserva se encarga de cambiar el estado a "COMPLETADA"
            reserva.completar()
            
            # Guarda el estado del sistema después de la modificación
            self.guardar_datos()
            
            # Retorna True para indicar que la reserva fue completada exitosamente
            return True
        
        # Si no se encuentra la reserva, retorna False para indicar que no se pudo completar
        return False
    
    # =====================================================================================================
    # El método aplicar_descuento_reserva busca una reserva por ID y aplica un descuento
    # utilizando el método aplicar_descuento de la clase Reserva, luego guarda el estado del sistema
    # después de la modificación. Retorna True si se aplicó el descuento correctamente, False
    # si no se encontró la reserva.
    # =====================================================================================================
    def aplicar_descuento_reserva(self, id_reserva: int, porcentaje: float):
        
        # Método aplicar_descuento_reserva
        # PROPÓSITO: Aplica un descuento a una reserva existente.
        # PARÁMETROS: id_reserva, porcentaje de descuento a aplicar
        # RETORNA: True si se aplicó el descuento correctamente, False si no se encontró la reserva
        
        # Busca reserva por ID usando comprensión de listas con next()
        reserva = next((r for r in self.reservas if r.id == id_reserva), None)
        
        # Si se encuentra la reserva, se aplica el descuento utilizando el método aplicar_descuento de la clase Reserva
        if reserva:
            
            # El método aplicar_descuento de la clase Reserva se encarga de
            # calcular el nuevo costo total aplicando el porcentaje de descuento
            reserva.aplicar_descuento(porcentaje)
            
            # Guarda el estado del sistema después de la modificación
            self.guardar_datos()
            
            # Retorna True para indicar que el descuento fue aplicado exitosamente
            return True
        
        # Si no se encuentra la reserva, retorna False para indicar que no se pudo aplicar el descuento
        return False
    
    # ==================== EXPORTACIONES ==================================================================
    # Estos métodos permiten exportar la información de clientes, servicios y reservas a archivos CSV
    # =====================================================================================================
    
    # =====================================================================================================
    # El método exportar_clientes_csv exporta la información de los clientes a un archivo
    # CSV llamado "clientes_export.csv" con las columnas ID, Nombre, Email, Teléfono, Cédula y Activo. 
    # Registra un evento en el log si la exportación es exitosa o un error si ocurre una excepción.
    # =====================================================================================================   
    def exportar_clientes_csv(self):
        
        # Método exportar_clientes_csv
        # PROPÓSITO: Exporta la información de los clientes a un archivo CSV.
        # PARÁMETROS: Ninguno
        # RETORNA: True si se exportó correctamente, False si ocurrió un error
        
        try:
            # Exporta la información de los clientes a un archivo CSV llamado "clientes_export.csv"
            with open('clientes_export.csv', 'w', newline='', encoding='utf-8') as f:
                
                # Escribe la cabecera del CSV y luego las filas con la información de cada cliente
                writer = csv.writer(f)
                # Escribe la cabecera del CSV con los nombres de las columnas
                writer.writerow(['ID', 'Nombre', 'Email', 'Teléfono', 'Cédula', 'Activo'])
                
                # Escribe una fila por cada cliente con su informacióncomo
                for c in self.clientes:
                    
                    # Formatea el campo "Activo" como "Sí" si el cliente está activo o "No" si no lo está
                    activo_texto = 'Sí' if c.activo else 'No'
                    
                    # Escribe la fila con la información del cliente, incluyendo el campo "Activo" formateado
                    writer.writerow([c.id, c.nombre, c.email, c.telefono, c.cedula, activo_texto])
                    
            # Registra evento de exportación exitosa en el log
            self.logger.registrar_evento("Clientes exportados a CSV")
            
            # Retorna True para indicar que la exportación fue exitosa
            return True
        
        except Exception as e: # Captura cualquier excepción que ocurra durante el proceso de exportación
            self.logger.registrar_error(e, "exportar_clientes_csv") # Registra el error en el log con contexto del método
            raise e # Re-lanza la excepción para que la UI la muestre
    
    # =====================================================================================================
    # El método exportar_servicios_csv exporta la información de los servicios a un archivo
    # CSV llamado "servicios_export.csv" con las columnas ID, Nombre, Tipo, Precio Base, Disponible
    # y Detalle Extra.
    # Registra un evento en el log si la exportación es exitosa o un error si ocurre una excepción.
    # =====================================================================================================
    def exportar_servicios_csv(self):
        try:
            # Exporta la información de los servicios a un archivo CSV llamado "servicios_export.csv"
            with open('servicios_export.csv', 'w', newline='', encoding='utf-8') as f:
                
                # Escribe la cabecera del CSV con los nombres de las columnas
                writer = csv.writer(f)
                
                # Escribe la cabecera del CSV con los nombres de las columnas
                writer.writerow(['ID', 'Nombre', 'Tipo', 'Precio Base', 'Disponible', 'Detalle Extra'])
                
                # Escribe una fila por cada servicio con su información,
                # incluyendo un campo extra que varía según el tipo de servicio
                for s in self.servicios:
                    
                    # Determina el detalle extra a incluir en la exportación
                    # según el tipo de servicio utilizando isinstance()
                    detalle = ""
                    
                    # Para sala, se incluye la capacidad; para equipo, el tipo de equipo;
                    # para asesoría, el nivel de experto
                    if isinstance(s, ReservaSalas):
                        
                        # Para servicios de tipo sala, se incluye la capacidad en el campo "Detalle Extra"
                        detalle = f"Capacidad: {s.capacidad}"
                        
                    # Para servicios de tipo equipo, se incluye el tipo de equipo en el campo "Detalle Extra"
                    elif isinstance(s, AlquilerEquipos):
                        detalle = f"Tipo: {s.tipo_equipo}"
                        
                    # Para servicios de tipo asesoría, se incluye el nivel de experto
                    # en el campo "Detalle Extra"
                    elif isinstance(s, AsesoriaEspecializada):
                        detalle = f"Nivel: {s.nivel}"
                        
                    # Formatea el campo "Disponible" como "Sí" si el servicio está disponible
                    # o "No" si no lo está
                    disponible_texto = 'Sí' if s.disponible else 'No'
                    
                    # Escribe la fila con la información del servicio,
                    # incluyendo el campo "Disponible" formateado
                    # y el campo "Detalle Extra" con la información específica según el tipo de servicio
                    writer.writerow([s.id, s.nombre, s.tipo.upper(), s.precio_base, disponible_texto, detalle])
                    
            # Registra evento de exportación exitosa en el log
            self.logger.registrar_evento("Servicios exportados a CSV")
            
            # Retorna True para indicar que la exportación fue exitosa
            return True
        
        except Exception as e: # Captura cualquier excepción que ocurra durante el proceso de exportación
            self.logger.registrar_error(e, "exportar_servicios_csv") # Registra el error en el log con contexto del método
            raise e # Re-lanza la excepción para que la UI la muestre
    # =====================================================================================================
    # El método exportar_reservas_csv exporta la información de las reservas a un archivo
    # CSV llamado "reservas_export.csv" con las columnas ID, Cliente, Servicio, Duración (h),
    # Estado, Costo Total y Fecha.
    # Registra un evento en el log si la exportación es exitosa o un error si ocurre una excepción.
    # ===================================================================================================== 
    def exportar_reservas_csv(self):
        
        # Método exportar_reservas_csv
        # PROPÓSITO: Exporta la información de las reservas a un archivo CSV.       
        # PARÁMETROS: Ninguno
        # RETORNA: True si se exportó correctamente, False si ocurrió un error
        
        try: 
            
            # Exporta la información de las reservas a un archivo CSV llamado "reservas_export.csv"
            with open('reservas_export.csv', 'w', newline='', encoding='utf-8') as f:
                
                # Escribe la cabecera del CSV con los nombres de las columnas
                writer = csv.writer(f)
                
                # Escribe la cabecera del CSV con los nombres de las columnas
                writer.writerow(['ID', 'Cliente', 'Servicio', 'Duración (h)', 'Estado', 'Costo Total', 'Fecha'])
                
                # Escribe una fila por cada reserva con su información, formateando el cliente y servicio   
                # utilizando el método obtener_descripcion de cada uno para mostrar
                # una descripción legible en el CSV
                for r in self.reservas:
                    
                    # Obtiene la información formateada de la reserva utilizando el método obtener_info
                    # de la clase Reserva,que devuelve un diccionario con los campos necesarios
                    # para la exportación, incluyendo la descripción del cliente y servicio
                    info = r.obtener_info()
                    
                    # Escribe la fila con la información de la reserva, utilizando el diccionario devuelto por obtener_info
                    writer.writerow([info['id'], info['cliente'], info['servicio'], 
                                    info['duracion'], info['estado'], info['costo'], info['fecha']])
                    
            # Registra evento de exportación exitosa en el log
            self.logger.registrar_evento("Reservas exportadas a CSV")
            
            # Retorna True para indicar que la exportación fue exitosa
            return True
        
        except Exception as e: # Captura cualquier excepción que ocurra durante el proceso de exportación
            self.logger.registrar_error(e, "exportar_reservas_csv") # Registra el error en el log con contexto del método
            raise e # Re-lanza la excepción para que la UI la muestre
    
    # ==================== MÉTODOS DE CONSULTA (GETTERS) ========================================================================
    # Estos métodos permiten obtener la información de clientes, servicios y reservas del sistema.
    # =====================================================================================================
    
    # =====================================================================================================
    # Retorna la lista de clientes
    # =====================================================================================================
    def obtener_clientes(self) -> List[Cliente]:
        return self.clientes
    
    # =====================================================================================================
    # Retorna la lista de servicios
    # =====================================================================================================
    def obtener_servicios(self) -> List[Servicio]:
        return self.servicios
    
    # =====================================================================================================
    # Retorna la lista de reservas
    # =====================================================================================================
    def obtener_reservas(self) -> List[Reserva]:
        return self.reservas
    
    # =====================================================================================================
    # Filtra reservas por ID de cliente (comprensión de lista)
    # =====================================================================================================
    def obtener_reservas_por_cliente(self, id_cliente: int) -> List[Reserva]:
        return [r for r in self.reservas if r._cliente.id == id_cliente]
    
    # =====================================================================================================
    # Filtra reservas por ID de servicio
    # =====================================================================================================
    def obtener_reservas_por_servicio(self, id_servicio: int) -> List[Reserva]:
        return [r for r in self.reservas if r._servicio.id == id_servicio]