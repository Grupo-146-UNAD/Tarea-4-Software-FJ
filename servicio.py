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
# CLASE SERVICIO (ABSTRACTA Y CONCRETA)
# =========================================================================================================

# Importa ABC (Abstract Base Class) y abstractmethod para crear clases abstractas
from abc import ABC, abstractmethod

# Importa EntidadBase desde el módulo cliente (clase base para todas las entidades)
from cliente import EntidadBase

# Importa la excepción personalizada para errores de servicios
from excepciones import ServicioNoDisponibleError

# Importa el logger singleton para registrar eventos
from logger import LoggerSistema

# =========================================================================================================
# CLASE ABSTRACTA SERVICIO
# =========================================================================================================

# Definición de la clase Servicio que hereda de EntidadBase y ABC
# EntidadBase: le da atributos como id, nombre, fecha_creacion
# ABC: la convierte en clase abstracta (no se puede instanciar directamente)
class Servicio(EntidadBase, ABC):
    
    # Clase abstracta que define la estructura básica de todos los servicios
    
    # =====================================================================================================
    # Método constructor: se ejecuta al crear un nuevo servicio
    # id_servicio: int - identificador único del servicio
    # nombre: str - nombre descriptivo del servicio
    # precio_base: float - costo por hora del servicio
    # disponible: bool - True por defecto, indica si el servicio está disponible
    # =====================================================================================================
    def __init__(self, id_servicio: int, nombre: str, precio_base: float, disponible: bool = True):
        
        # super() llama al constructor de la clase padre (EntidadBase)
        # Le pasa id_servicio y nombre para que los procese la clase base
        super().__init__(id_servicio, nombre)
        
        # Validación: si el precio_base es negativo (menor que cero)
        if precio_base < 0:
            # Lanza una excepción personalizada ServicioNoDisponibleError
            # Interrumpe la creación del servicio
            raise ServicioNoDisponibleError(f"Precio base negativo: {precio_base}")
        
        # Asigna el precio_base al atributo privado _precio_base
        self._precio_base = precio_base
        
        # Asigna la disponibilidad al atributo privado _disponible
        self._disponible = disponible
        
    # =====================================================================================================
    # Decorador @abstractmethod: Declara que este método es abstracto, 
    # las clases hijas DEBEN implementarlo obligatoriamente
    # =====================================================================================================
    # Método para calcular el costo del servicio
    # duracion_horas: float - cantidad de horas del servicio
    # **kwargs: parámetros adicionales variables (personas, seguro, tema, etc.)
    # Retorna: float - costo total calculado
    # =====================================================================================================
    @abstractmethod 
    def calcular_costo(self, duracion_horas: float, **kwargs) -> float:
        pass  # Sin implementación - las clases hijas deben definirla
    
    # =====================================================================================================
    # Decorador @abstractmethod: Declara que este método es abstracto
    # =====================================================================================================
    # Método para validar parámetros específicos de cada servicio
    # **kwargs: parámetros a validar (personas, cantidad, tema, etc.)
    # Retorna: bool - True si válido, lanza excepción si no
    # =====================================================================================================
    @abstractmethod 
    def validar_parametros(self, **kwargs) -> bool:
        pass  # Sin implementación - las clases hijas deben definirla
    
    # =====================================================================================================
    # Decorador @property: Convierte el método en getter (propiedad de solo lectura)
    # Permite acceder al precio_base como servicio.precio_base
    # =====================================================================================================
    # Getter de precio_base: retorna el valor del atributo privado
    # El tipo de retorno es float (número decimal)
    # =====================================================================================================
    @property
    def precio_base(self) -> float:
        return self._precio_base
    
    # =====================================================================================================
    # Decorador @property: Getter para la disponibilidad
    # =====================================================================================================
    # Getter de disponible: retorna True si disponible, False si no
    # El tipo de retorno es bool (booleano)
    # =====================================================================================================
    @property
    def disponible(self) -> bool:
        return self._disponible
    
    # =====================================================================================================
    # Método para cambiar la disponibilidad del servicio
    # estado: bool - True = disponible, False = no disponible
    # =========================================================================================================
    def cambiar_disponibilidad(self, estado: bool):
        
        # Cambia el atributo _disponible al nuevo estado
        self._disponible = estado
        
        # Operador ternario: "disponible" si estado es True, "no disponible" si False
        estado_texto = "disponible" if estado else "no disponible"
        
        # Registra el cambio en el archivo de logs
        LoggerSistema().registrar_evento(f"Servicio {self._nombre} ahora {estado_texto}")
    
    # =====================================================================================================
    # Método para obtener una descripción del servicio
    # Este método SÍ tiene implementación (no es abstracto)
    # Puede ser sobrescrito por las clases hijas si lo desean
    # =====================================================================================================
    def obtener_descripcion(self) -> str:
        
        # :.2f formatea el float con 2 decimales
        # Ejemplo: 25000.00 se muestra como 25000.00
        return f"{self._nombre} - ${self._precio_base:.2f}/hora"

# =========================================================================================================
# CLASE CONCRETA: RESERVA DE SALAS
# =========================================================================================================
# Definición de la clase ReservaSalas que hereda de Servicio
# Es un servicio concreto para alquilar salas con capacidad máxima
class ReservaSalas(Servicio):
    
    # =====================================================================================================
    # Método constructor: crea una nueva sala
    # =====================================================================================================
    def __init__(self, id_servicio: int, nombre: str, precio_base: float, capacidad_maxima: int):
        
        # Llama al constructor de la clase padre (Servicio)
        super().__init__(id_servicio, nombre, precio_base)
        
        # Asigna la capacidad máxima al atributo privado _capacidad_maxima
        self._capacidad_maxima = capacidad_maxima
        
        # Asigna el tipo de servicio como "sala"
        self._tipo = "sala"
    
    # =====================================================================================================
    # Implementación del método abstracto calcular_costo
    # Calcula el costo de alquilar la sala
    # =====================================================================================================
    def calcular_costo(self, duracion_horas: float, **kwargs) -> float:
        
        # get() obtiene el valor de 'equipo_adicional' del diccionario kwargs
        # Si no existe, retorna False (valor por defecto)
        equipo_adicional = kwargs.get('equipo_adicional', False)
        
        # Cálculo base: precio_base × horas
        costo = self._precio_base * duracion_horas
        
        # Si hay equipo adicional, incrementa el costo en 20%
        if equipo_adicional:
            costo *= 1.2  # Multiplica por 1.2 (aumenta 20%)
        
        # round(valor, 2): Redondea a 2 decimales para valores monetarios
        return round(costo, 2)
    
    # =====================================================================================================
    # Implementación del método abstracto validar_parametros
    # Verifica que el número de personas no exceda la capacidad
    # =====================================================================================================
    def validar_parametros(self, **kwargs) -> bool:
        
        # get('personas', 0): obtiene 'personas' o 0 si no existe
        personas = kwargs.get('personas', 0)
        
        # Si el número de personas supera la capacidad máxima
        if personas > self._capacidad_maxima:
            # Lanza excepción con mensaje descriptivo
            raise ServicioNoDisponibleError(f"La sala solo soporta {self._capacidad_maxima} personas")
        
        # Si pasa la validación, retorna True
        return True
    
    # =====================================================================================================
    # Sobrescribe el método obtener_descripcion de la clase padre
    # Retorna una descripción específica para salas
    # =====================================================================================================
    def obtener_descripcion(self) -> str:
        return f"Sala: {self._nombre} | Cap:{self._capacidad_maxima} | ${self._precio_base}/h"
    
    # =====================================================================================================
    # Decorador @property: Getter para el tipo de servicio
    # =====================================================================================================
    @property
    def tipo(self) -> str:
        return self._tipo
    
    # =====================================================================================================
    # Decorador @property: Getter para la capacidad máxima
    # =====================================================================================================
    @property
    def capacidad(self) -> int:
        return self._capacidad_maxima

# =========================================================================================================
# CLASE CONCRETA: ALQUILER DE EQUIPOS
# =========================================================================================================
# Definición de la clase AlquilerEquipos que hereda de Servicio
# Servicio para alquilar equipos como laptops, proyectores, tablets
class AlquilerEquipos(Servicio):
    
    # =====================================================================================================
    # Método constructor: crea un nuevo servicio de alquiler de equipos
    # =====================================================================================================
    def __init__(self, id_servicio: int, nombre: str, precio_base: float, tipo_equipo: str):
        
        # Llama al constructor de la clase padre (Servicio)
        super().__init__(id_servicio, nombre, precio_base)
        
        # Asigna el tipo de equipo al atributo privado _tipo_equipo
        # Ejemplo: "Computadora", "Proyector", "Tablet"
        self._tipo_equipo = tipo_equipo
        
        # Asigna el tipo de servicio como "equipo"
        self._tipo = "equipo"
    
    # =====================================================================================================
    # Implementación del método calcular_costo
    # Calcula el costo de alquilar equipos
    # =====================================================================================================
    def calcular_costo(self, duracion_horas: float, **kwargs) -> float:
        
        # get('seguro', False): obtiene 'seguro' o False por defecto
        seguro = kwargs.get('seguro', False)
        
        # get('cantidad', 1): obtiene 'cantidad' o 1 por defecto
        cantidad = kwargs.get('cantidad', 1)
        
        # Cálculo: precio_base × horas × cantidad_de_equipos
        costo = self._precio_base * duracion_horas * cantidad
        
        # Si el cliente seleccionó seguro, suma $5000 fijos
        if seguro:
            costo += 5000
        
        # Redondea a 2 decimales y retorna
        return round(costo, 2)
    
    # =====================================================================================================
    # Implementación del método validar_parametros
    # Verifica que la cantidad de equipos sea válida
    # =====================================================================================================
    def validar_parametros(self, **kwargs) -> bool:
        
        # Obtiene la cantidad (o 1 por defecto)
        cantidad = kwargs.get('cantidad', 1)
        
        # Si la cantidad es menor o igual a cero
        if cantidad <= 0:
            raise ServicioNoDisponibleError("La cantidad debe ser mayor a 0")
        
        # Si la cantidad supera los 10 equipos
        if cantidad > 10:
            raise ServicioNoDisponibleError("No se pueden alquilar más de 10 equipos")
        
        # Si pasa las validaciones, retorna True
        return True
    
    # =====================================================================================================
    # Sobrescribe obtener_descripcion para equipos
    # =====================================================================================================
    def obtener_descripcion(self) -> str:
        return f"Equipo: {self._nombre} | {self._tipo_equipo} | ${self._precio_base}/h"
    
    # =====================================================================================================
    # Getter para el tipo de servicio
    # =====================================================================================================
    @property
    def tipo(self) -> str:
        return self._tipo
    
    # =====================================================================================================
    # Getter para el tipo de equipo
    # =====================================================================================================
    @property
    def tipo_equipo(self) -> str:
        return self._tipo_equipo

# =========================================================================================================
# CLASE CONCRETA: ASESORÍA ESPECIALIZADA
# =========================================================================================================
# Definición de la clase AsesoriaEspecializada que hereda de Servicio
# Servicio de asesorías personalizadas (Python, Data Science, etc.)
class AsesoriaEspecializada(Servicio):
    
    # =====================================================================================================
    # Método constructor: crea una nueva asesoría
    # =====================================================================================================
    def __init__(self, id_servicio: int, nombre: str, precio_base: float, nivel_experto: str):
        
        # Llama al constructor de la clase padre (Servicio)
        super().__init__(id_servicio, nombre, precio_base)
        
        # Asigna el nivel del experto al atributo privado _nivel_experto
        # Ejemplos: "Junior", "Senior", "Master"
        self._nivel_experto = nivel_experto
        
        # Asigna el tipo de servicio como "asesoria"
        self._tipo = "asesoria"
    
    # =====================================================================================================
    # Implementación del método calcular_costo
    # Calcula el costo de la asesoría con descuento para miembros premium
    # =====================================================================================================
    def calcular_costo(self, duracion_horas: float, **kwargs) -> float:
        
        # get('miembro_premium', False): verifica si es miembro premium
        miembro_premium = kwargs.get('miembro_premium', False)
        
        # Cálculo base: precio_base × horas
        costo = self._precio_base * duracion_horas
        
        # Si es miembro premium, aplica 15% de descuento
        if miembro_premium:
            costo *= 0.85  # Multiplica por 0.85 = 15% descuento
        
        # Redondea a 2 decimales
        return round(costo, 2)
    
    # =====================================================================================================
    # Implementación del método validar_parametros
    # Verifica que el tema de la asesoría sea válido
    # =====================================================================================================
    def validar_parametros(self, **kwargs) -> bool:
        
        # get('tema', ''): obtiene el tema o cadena vacía
        tema = kwargs.get('tema', '')
        
        # Si el tema está vacío O tiene menos de 5 caracteres
        if not tema or len(tema) < 5:
            # Lanza excepción
            raise ServicioNoDisponibleError("El tema de asesoría debe tener al menos 5 caracteres")
        
        # Si pasa la validación, retorna True
        return True
    
    # =====================================================================================================
    # Sobrescribe obtener_descripcion para asesorías
    # =====================================================================================================
    def obtener_descripcion(self) -> str:
        return f"Asesoría: {self._nombre} | Nivel:{self._nivel_experto} | ${self._precio_base}/h"
    
    # =====================================================================================================
    # Getter para el tipo de servicio
    # =====================================================================================================
    @property
    def tipo(self) -> str:
        return self._tipo
    
    # =====================================================================================================
    # Getter para el nivel del experto
    # =====================================================================================================
    @property
    def nivel(self) -> str:
        return self._nivel_experto
