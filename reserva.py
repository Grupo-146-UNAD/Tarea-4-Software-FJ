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
# CLASE RESERVA - CON MÉTODOS SOBRECARGADOS
# =========================================================================================================

# ==================== IMPORTACIONES ======================================================================
# Cada importación trae funcionalidades específicas de Python
import datetime # Para manejar fechas, horas y realizar operaciones con tiempo
from excepciones import ReservaInvalidaError, EstadoReservaInvalidoError, ServicioNoDisponibleError # Para manejo de errores específicos del sistema
from logger import LoggerSistema # Para registro de eventos y errores
from servicio import ReservaSalas, AlquilerEquipos, AsesoriaEspecializada

# =========================================================================================================
# Integra cliente, servicio y gestiona el ciclo de vida de la reserva
# =========================================================================================================
class Reserva:
    
    # Atributo de CLASE (compartido por todas las instancias)
    ESTADOS = ["PENDIENTE", "CONFIRMADA", "CANCELADA", "COMPLETADA"]
    
    
    # =====================================================================================================
    # CONSTRUCTOR: __init__ recibe cliente, servicio, duración y parámetros extra para calcular el costo
    # =====================================================================================================
    def __init__(self, id_reserva: int, cliente, servicio, 
                duracion_horas: float, parametros_extra: dict = None,
                fecha_reserva: datetime.datetime = None):
        
        # Crea una nueva reserva con validaciones
        
        self._id = id_reserva                    # ID único de reserva
        self._cliente = cliente                  # Objeto Cliente (composición)
        self._servicio = servicio                # Objeto Servicio (composición)
        self._duracion_horas = duracion_horas    # Duración en horas
        self._parametros_extra = parametros_extra or {}  # Diccionario vacío si es None
        self._fecha_reserva = fecha_reserva or datetime.datetime.now()  # Fecha actual si no se especifica
        self._estado = "PENDIENTE"               # Estado inicial
        self._costo_total = 0.0                  # Costo inicial (se calculará)
        
        
        # Estos atributos permiten mostrar en la tabla el precio sin descuento
        self._precio_base_total = 0.0      # Almacena el precio sin descuento
        self._porcentaje_descuento = 0.0   # Almacena el % de descuento aplicado
        self._valor_descuento = 0.0        # Almacena el valor del descuento en pesos
        
        # Llama a métodos privados (con _) para validar y calcular
        self._validar_reserva()
        self._calcular_costo_inicial()
        
        LoggerSistema().registrar_evento(f"Reserva {self._id} creada para {cliente.nombre}")
    
    # =====================================================================================================
    # MÉTODOS PRIVADOS: _validar_reserva y _calcular_costo_inicial se encargan de validar los datos
    # =====================================================================================================
    def _validar_reserva(self):
        # Verifica que todos los datos sean correctos ANTES de crear la reserva
        
        # Validación 1: Cliente activo
        if not self._cliente.activo:
            raise ReservaInvalidaError("El cliente no está activo")
        
        # Validación 2: Servicio disponible
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError("El servicio no está disponible")
        
        # Validación 3: Duración positiva
        if self._duracion_horas <= 0:
            raise ReservaInvalidaError("La duración debe ser mayor a 0 horas")
        
        # Validación 4: Duración máxima de 24 horas
        if self._duracion_horas > 24:
            raise ReservaInvalidaError("No se permiten reservas de más de 24 horas")
    
    # =====================================================================================================
    # MÉTODO PRIVADO: _calcular_costo_inicial utiliza el polimorfismo del servicio
    # para calcular el costo total. Guarda el precio base SIN descuento para poder mostrar ambos valores
    # =====================================================================================================
    def _calcular_costo_inicial(self):
            
        try:
            # Calcula el precio base (sin descuento) usando los parámetros extra reales
            # El método calcular_costo() es polimórfico (diferente según el tipo de servicio)
            self._precio_base_total = self._servicio.calcular_costo(
                self._duracion_horas, 
                **self._parametros_extra  # Desempaqueta el diccionario de parámetros reales
            )
            # Inicialmente, el costo total es igual al precio base (sin descuento)
            self._costo_total = self._precio_base_total
                
        except Exception as e:
            # Encadenamiento de excepciones: preserva la causa original
            raise ReservaInvalidaError(f"Error calculando costo: {str(e)}") from e
    
    # ==================== MÉTODOS DE ESTADO ====================
    
    # =====================================================================================================
    # MÉTODOS DE NEGOCIO: confirmar Cambia estado a CONFIRMADA (solo desde PENDIENTE)
    # =====================================================================================================
    def confirmar(self):
        
        # Cambia estado a CONFIRMADA (solo desde PENDIENTE)
        
        # Verifica que el estado actual sea PENDIENTE
        if self._estado != "PENDIENTE":
            raise EstadoReservaInvalidoError(
                f"No se puede confirmar reserva en estado {self._estado}"
            )
        
        # Verifica nuevamente disponibilidad (pudo haber cambiado)
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError("El servicio ya no está disponible")
        
        self._estado = "CONFIRMADA"
        LoggerSistema().registrar_evento(f"Reserva {self._id} confirmada. Costo: ${self._costo_total}")
        
    # =====================================================================================================
    # MÉTODO: cancelar
    # PROPÓSITO: Cancela una reserva (solo si NO está vencida)
    # VALIDACIONES: 
    #   1. No se puede cancelar si ya está COMPLETADA o CANCELADA
    #   2. No se puede cancelar si la reserva ya VENCIÓ (fecha_fin < fecha_actual)
    # =====================================================================================================
    def cancelar(self, motivo: str = ""):
                
        # ========== VALIDACIÓN 1: ESTADO NO PERMITIDO ==========
        # Verificar que la reserva no esté ya COMPLETADA o CANCELADA
        # Si está en alguno de estos estados, no se puede cancelar
        if self._estado in ["COMPLETADA", "CANCELADA"]:
            # Lanzar excepción indicando que no se puede cancelar
            raise EstadoReservaInvalidoError(
                f"No se puede cancelar reserva en estado {self._estado}"
            )
        
        # ========== VALIDACIÓN 2: RESERVA VENCIDA (NUEVA) ==========
        # Verificar si la reserva ya pasó su fecha/hora de finalización
        # una reserva vencida NO se puede cancelar porque el servicio ya se prestó
        
        # Calcular la fecha/hora de finalización de la reserva
        # fecha_fin = fecha_inicio + duracion_en_horas
        fecha_fin = self._fecha_reserva + datetime.timedelta(hours=self._duracion_horas)
        
        # Obtener la fecha y hora actual del sistema
        ahora = datetime.datetime.now()
        
        # Si la fecha_fin es MENOR o IGUAL a la hora actual → la reserva está VENCIDA
        if fecha_fin <= ahora:
            # Formatear fechas para mostrar en el mensaje de error
            fecha_fin_str = fecha_fin.strftime('%Y-%m-%d %H:%M')
            fecha_reserva_str = self._fecha_reserva.strftime('%Y-%m-%d %H:%M')
            
            # Lanzar excepción indicando que no se puede cancelar porque está vencida
            raise EstadoReservaInvalidoError(
                f"❌ No se puede cancelar la reserva #{self._id} porque ya está VENCIDA.\n"
                f"📅 Fecha de reserva: {fecha_reserva_str}\n"
                f"⏱️ Duración: {self._duracion_horas} horas\n"
                f"🔚 Finalizó el: {fecha_fin_str}\n"
                f"💡 Las reservas vencidas no se pueden cancelar porque el servicio ya fue prestado."
            )
        
        # ========== CANCELAR LA RESERVA ==========
        # Si pasa todas las validaciones, cambiar el estado a "CANCELADA"
        self._estado = "CANCELADA"
        
        # Registrar el evento en el archivo de logs
        # Si no se proporcionó motivo, usar "No especificado"
        LoggerSistema().registrar_evento(
            f"Reserva {self._id} cancelada. Motivo: {motivo or 'No especificado'}"
        )
    
    # =====================================================================================================
    # MÉTODO: completar Cambia estado a COMPLETADA (solo desde CONFIRMADA) y registra el evento
    # =====================================================================================================
    def completar(self):
        
        # Solo desde estado CONFIRMADA
        
        if self._estado != "CONFIRMADA":
            raise EstadoReservaInvalidoError("Solo reservas confirmadas pueden completarse")
        self._estado = "COMPLETADA"
        LoggerSistema().registrar_evento(f"Reserva {self._id} completada")
    
    # =====================================================================================================
    # MÉTODO: aplicar_descuento Aplica un descuento porcentual al costo total
    # Guarda el porcentaje aplicado y valor del descuento para mostrar en la tabla
    # =====================================================================================================
    def aplicar_descuento(self, porcentaje: float):
        
        # Validar que el porcentaje esté en el rango permitido (0-100)
        if porcentaje < 0 or porcentaje > 100:
            raise ValueError("Porcentaje de descuento inválido")
            
        # Guardar el porcentaje aplicado (para mostrarlo en la tabla)
        self._porcentaje_descuento = porcentaje
            
        # Calcular el valor del descuento (cuánto dinero se resta)
        # Fórmula: precio_base * (porcentaje / 100)
        self._valor_descuento = round(self._precio_base_total * (porcentaje / 100), 2)
            
        # Calcular el nuevo costo total (precio base - descuento)
        self._costo_total = round(self._precio_base_total - self._valor_descuento, 2)
            
        # Registrar evento detallado en el log
        LoggerSistema().registrar_evento(
            f"Descuento {porcentaje}% aplicado a reserva {self._id}. "
            f"Valor descuento: ${self._valor_descuento:,.0f}, "
            f"Total final: ${self._costo_total:,.0f}"
        )
    
    # ==================== MÉTODOS SOBRECARGADOS PARA CÁLCULO DE COSTOS ====================
    # ======================================================================================
    # Métodos sobrecargados con diferentes variantes de cálculo de costos con impuestos,
    # descuentos y parámetros opcionales
    # ======================================================================================
    
    # ---------- SOBRECARGA 1: Parámetros por defecto (forma más pythonica) ----------
    
    # =====================================================================================================
    # MÉTODO: calcular_costo_con_impuesto, calcula el costo total incluyendo impuesto
    # Demuestra sobrecarga con parámetro opcional (impuesto con valor por defecto)
    # =====================================================================================================
    def calcular_costo_con_impuesto(self, impuesto_porcentaje: float = 19) -> float:
        
        # SOBRECARGA 1: Calcula el costo total incluyendo impuesto
        # =========================================================
        # Demuestra sobrecarga con parámetro opcional (impuesto con valor por defecto)
        
        # PARÁMETROS:
        #    impuesto_porcentaje (float): Porcentaje de impuesto (default: 19% IVA)
        
        # RETORNA:
        #    float: Costo total con impuesto incluido
        
        # EJEMPLOS:
        #    >>> reserva.calcular_costo_con_impuesto()      # Usa 19% por defecto
        #    >>> reserva.calcular_costo_con_impuesto(10)    # Usa 10% personalizado
        
        return round(self._costo_total * (1 + impuesto_porcentaje / 100), 2)
    
    # ---------- SOBRECARGA 2: Método con diferentes parámetros ----------
    
    # =====================================================================================================
    # MÉTODO: calcular_costo_con_descuento, calcula el costo total aplicando descuento
    # Demuestra sobrecarga con un método que recibe un parámetro diferente
    # =====================================================================================================
    def calcular_costo_con_descuento(self, porcentaje_descuento: float) -> float:
        # SOBRECARGA 2: Calcula el costo total aplicando descuento
        # ========================================================
        # Demuestra sobrecarga con un método que recibe un parámetro diferente
        
        # PARÁMETROS:
        #    porcentaje_descuento (float): Porcentaje de descuento a aplicar (0-100)
        
        # RETORNA:
        #    float: Costo total con descuento aplicado
        
        # EJEMPLO:
        #     >>> reserva.calcular_costo_con_descuento(15)   # 15% de descuento
        
        if porcentaje_descuento < 0 or porcentaje_descuento > 100:
            raise ValueError("El porcentaje de descuento debe estar entre 0 y 100")
        
        return round(self._costo_total * (1 - porcentaje_descuento / 100), 2)
    
    # ---------- SOBRECARGA 3: Múltiples parámetros opcionales ----------
    
    # =====================================================================================================
    # MÉTODO: calcular_costo_con_impuesto_y_descuento, calcula el costo con impuesto y descuento
    #  Demuestra sobrecarga con múltiples parámetros opcionales
    # =====================================================================================================
    def calcular_costo_con_impuesto_y_descuento(self, impuesto: float = 19, descuento: float = 0) -> float:
        
        # SOBRECARGA 3: Calcula el costo con impuesto y descuento
        # ========================================================
        # Demuestra sobrecarga con múltiples parámetros opcionales
        
        # PARÁMETROS:
        #    impuesto (float): Porcentaje de impuesto (default: 19%)
        #    descuento (float): Porcentaje de descuento (default: 0%)
        
        # RETORNA:
        #    float: Costo total con impuesto y descuento
        
        # EJEMPLOS:
        #    >>> reserva.calcular_costo_con_impuesto_y_descuento(19, 10)  # 19% impuesto, 10% descuento
        #    >>> reserva.calcular_costo_con_impuesto_y_descuento(16, 5)    # 16% impuesto, 5% descuento
        
        total = self._costo_total
        total = total * (1 + impuesto / 100)   # Aplicar impuesto
        total = total * (1 - descuento / 100)   # Aplicar descuento
        return round(total, 2)
    
    # ---------- SOBRECARGA 4: Cálculo por persona (útil para salas) ----------
    
    # =====================================================================================================
    # MÉTODO: calcular_costo_por_persona, calcula el costo por persona con opción de incluir impuesto
    # Demuestra sobrecarga con parámetro booleano que cambia el comportamiento
    # =====================================================================================================
    def calcular_costo_por_persona(self, num_personas: int, incluir_impuesto: bool = False) -> dict:
        
        # SOBRECARGA 4: Calcula el costo por persona con opción de incluir impuesto
        # ==========================================================================
        # Demuestra sobrecarga con parámetro booleano que cambia el comportamiento
        
        # PARÁMETROS:
        #    num_personas (int): Número de personas que pagan
        #    incluir_impuesto (bool): Si True, incluye 19% de impuesto
        
        # RETORNA:
        #    dict: Diccionario con desglose del cálculo por persona
        
        # EJEMPLO:
        #     >>> reserva.calcular_costo_por_persona(10)           # Sin impuesto
        #    >>> reserva.calcular_costo_por_persona(10, True)     # Con impuesto
        
        if num_personas <= 0:
            raise ValueError("El número de personas debe ser mayor a 0")
        
        costo_base_por_persona = self._costo_total / num_personas
        
        if incluir_impuesto:
            costo_final_por_persona = costo_base_por_persona * 1.19
            impuesto_aplicado = costo_final_por_persona - costo_base_por_persona
        else:
            costo_final_por_persona = costo_base_por_persona
            impuesto_aplicado = 0
        
        return {
            "costo_total_reserva": round(self._costo_total, 2),
            "num_personas": num_personas,
            "costo_por_persona_sin_impuesto": round(costo_base_por_persona, 2),
            "impuesto_por_persona": round(impuesto_aplicado, 2),
            "costo_por_persona_final": round(costo_final_por_persona, 2)
        }
    
    # ---------- SOBRECARGA 5: Parámetros flexibles con **kwargs ----------
    
    # =====================================================================================================
    # MÉTODO: calcular_costo_personalizado, calcula costo con parámetros flexibles usando **kwargs
    # Demuestra sobrecarga donde se pueden pasar múltiples parámetros opcionales
    # =====================================================================================================
    def calcular_costo_personalizado(self, **kwargs) -> dict:
        
        # SOBRECARGA 5: Calcula costo con parámetros flexibles usando **kwargs
        # =====================================================================
        # Demuestra sobrecarga donde se pueden pasar múltiples parámetros opcionales
        
        # PARÁMETROS POSIBLES en kwargs:
        #    - impuesto: porcentaje de impuesto
        #    - descuento: porcentaje de descuento
        #    - recargo_fijo: valor fijo adicional
        #    - motivo_recargo: texto explicativo del recargo
        #    - membresa: tipo de membresía (basica, premium, gold)
        
        # RETORNA:
        #    dict: Diccionario completo con desglose del cálculo
        
        # EJEMPLOS:
        #    >>> reserva.calcular_costo_personalizado(impuesto=19)
        #    >>> reserva.calcular_costo_personalizado(descuento=10)
        #    >>> reserva.calcular_costo_personalizado(impuesto=19, descuento=10, recargo_fijo=5000)
        #    >>> reserva.calcular_costo_personalizado(membresia="premium")
        
        total = self._costo_total
        aplicaciones = []
        
        # Diccionario de descuentos por tipo de membresía
        descuentos_membresia = {
            "basica": 0,
            "premium": 10,
            "gold": 15
        }
        
        # Aplicar descuento por membresía
        if 'membresia' in kwargs and kwargs['membresia'].lower() in descuentos_membresia:
            desc_membresia = descuentos_membresia[kwargs['membresia'].lower()]
            if desc_membresia > 0:
                valor_descuento = total * desc_membresia / 100
                total -= valor_descuento
                aplicaciones.append({
                    "concepto": f"Descuento membresía {kwargs['membresia']}",
                    "porcentaje": desc_membresia,
                    "valor": round(valor_descuento, 2)
                })
        
        # Aplicar impuesto
        if 'impuesto' in kwargs and kwargs['impuesto'] > 0:
            valor_impuesto = total * kwargs['impuesto'] / 100
            total += valor_impuesto
            aplicaciones.append({
                "concepto": "Impuesto",
                "porcentaje": kwargs['impuesto'],
                "valor": round(valor_impuesto, 2)
            })
        
        # Aplicar descuento adicional
        if 'descuento' in kwargs and kwargs['descuento'] > 0:
            valor_descuento = total * kwargs['descuento'] / 100
            total -= valor_descuento
            aplicaciones.append({
                "concepto": "Descuento adicional",
                "porcentaje": kwargs['descuento'],
                "valor": round(valor_descuento, 2)
            })
        
        # Aplicar recargo fijo
        if 'recargo_fijo' in kwargs and kwargs['recargo_fijo'] > 0:
            total += kwargs['recargo_fijo']
            aplicaciones.append({
                "concepto": kwargs.get('motivo_recargo', 'Recargo fijo'),
                "porcentaje": None,
                "valor": round(kwargs['recargo_fijo'], 2)
            })
        
        return {
            "costo_original": round(self._costo_total, 2),
            "aplicaciones": aplicaciones,
            "costo_final": round(total, 2),
            "ahorro_total": round(self._costo_total - total, 2) if total < self._costo_total else 0,
            "recargo_total": round(total - self._costo_total, 2) if total > self._costo_total else 0
        }
    
    # ---------- SOBRECARGA 6: Suma de múltiples costos (*args) ----------
    
    # =====================================================================================================
    # MÉTODO: calcular_costo_acumulado, suma el costo de la reserva con costos adicionales
    # Demuestra sobrecarga usando *args (número variable de argumentos)
    # =====================================================================================================
    def calcular_costo_acumulado(self, *costos_adicionales) -> float:
        
        # SOBRECARGA 6: Suma el costo de la reserva con costos adicionales
        # ================================================================
        # Demuestra sobrecarga usando *args (número variable de argumentos)
        
        # PARÁMETROS:
        #    *costos_adicionales: Uno o más costos adicionales para sumar
        
        # RETORNA:
        # float: Suma total incluyendo la reserva y todos los costos adicionales
        
        # EJEMPLOS:
        #    >>> reserva.calcular_costo_acumulado(5000)                        # +1 costo adicional
        #    >>> reserva.calcular_costo_acumulado(5000, 3000, 2000)            # +3 costos adicionales
        
        total = self._costo_total
        for costo in costos_adicionales:
            total += costo
        return round(total, 2)
    
    # ---------- SOBRECARGA 7: Con tipo de cliente (sobrecarga por comportamiento) ----------
    
    # =====================================================================================================
    # MÉTODO: calcular_costo_por_tipo_cliente, calcula costo según el tipo de cliente
    # Demuestra sobrecarga donde el comportamiento cambia según el tipo de parámetro
    # =====================================================================================================
    def calcular_costo_por_tipo_cliente(self, tipo_cliente: str, incluir_impuesto: bool = True) -> dict:
        
        # SOBRECARGA 7: Calcula costo según el tipo de cliente
        # =====================================================
        # Demuestra sobrecarga donde el comportamiento cambia según el tipo de parámetro
        
        # TIPOS DE CLIENTE:
        #    - "regular": Sin descuento
        #    - "frecuente": 5% descuento
        #    - "vip": 10% descuento
        #    - "corporativo": 15% descuento
        
        # PARÁMETROS:
        #    tipo_cliente (str): Tipo de cliente (regular, frecuente, vip, corporativo)
        #    incluir_impuesto (bool): Si True, incluye 19% de impuesto
        
        # RETORNA:
        #    dict: Diccionario con desglose completo
        
        #EJEMPLO:
        #    >>> reserva.calcular_costo_por_tipo_cliente("vip")
        
        descuentos = {
            "regular": 0,
            "frecuente": 5,
            "vip": 10,
            "corporativo": 15
        }
        
        tipo = tipo_cliente.lower()
        if tipo not in descuentos:
            raise ValueError(f"Tipo de cliente inválido: {tipo_cliente}. Opciones: regular, frecuente, vip, corporativo")
        
        descuento = descuentos[tipo]
        total = self._costo_total * (1 - descuento / 100)
        
        if incluir_impuesto:
            total = total * 1.19
            impuesto_aplicado = total - (self._costo_total * (1 - descuento / 100))
        else:
            impuesto_aplicado = 0
        
        return {
            "tipo_cliente": tipo,
            "costo_original": round(self._costo_total, 2),
            "descuento_aplicado": descuento,
            "valor_descuento": round(self._costo_total * descuento / 100, 2),
            "costo_con_descuento": round(self._costo_total * (1 - descuento / 100), 2),
            "impuesto_incluido": incluir_impuesto,
            "valor_impuesto": round(impuesto_aplicado, 2) if incluir_impuesto else 0,
            "costo_final": round(total, 2)
        }
    
    # ==================== MÉTODO DEMOSTRATIVO ====================
    
    # =====================================================================================================
    # MÉTODO: demostrar_todas_sobrecargas, muestra ejemplos de todas las sobrecargas
    # Útil para verificar que todos los métodos sobrecargados funcionan correctamente
    # =====================================================================================================
    
    # ==================================================================================
    # MÉTODO: demostrar_todas_sobrecargas
    # Demuestra el POLIMORFISMO y los MÉTODOS SOBRECARGADOS
    # Retorna un string con la demostración completa de los métodos sobrecargados
    # muestra cálculos detallados (personas, equipo adicional, cantidad, seguro, premium)
    # ==================================================================================
    def demostrar_todas_sobrecargas(self) -> str:
        
        # Importar dentro del método para evitar import circular
        from servicio import ReservaSalas, AlquilerEquipos, AsesoriaEspecializada
        
        # ========== OBTENER INFORMACIÓN BÁSICA ==========
        nombre_cliente = self._cliente.nombre
        nombre_servicio = self._servicio.nombre
        tipo_servicio = self._servicio.tipo.upper()
        duracion = self._duracion_horas
        parametros = self._parametros_extra
        precio_base_total = self._precio_base_total
        costo_total = self._costo_total
        precio_por_hora = self._servicio.precio_base
        
        linea_sep = "=" * 80
        
        # ========== INICIAR MENSAJE ==========
        mensaje = f"""
{linea_sep}
🧪 DEMOSTRACIÓN DE MÉTODOS SOBRECARGADOS (POLIMORFISMO)
{linea_sep}

📋 RESERVA ACTUAL:
   • ID: {self._id}
   • Cliente: {nombre_cliente}
   • Servicio: {nombre_servicio} ({tipo_servicio})
   • Duración: {duracion} horas
   • Estado: {self._estado}

{linea_sep}
📝 PARÁMETROS EXTRA DE ESTA RESERVA:
"""
        
        # Mostrar parámetros reales
        if parametros:
            for clave, valor in parametros.items():
                if isinstance(valor, bool):
                    valor_str = "✅ Sí" if valor else "❌ No"
                else:
                    valor_str = str(valor)
                mensaje += f"   • {clave} = {valor_str}\n"
        else:
            mensaje += "   • No se ingresaron parámetros extra\n"
        
        mensaje += f"""
{linea_sep}
💰 CÁLCULO DETALLADO DEL COSTO:
"""
        
        # ========== CASO 1: SERVICIO DE SALA ==========
        if isinstance(self._servicio, ReservaSalas):
            capacidad = self._servicio.capacidad
            personas = parametros.get("personas", 0)
            equipo_adicional = parametros.get("equipo_adicional", False)
            
            # Calcular precio base (sin descuento)
            precio_base_calculado = precio_por_hora * duracion
            
            mensaje += f"""
   🪑 **SERVICIO: SALA**
   ───────────────────────────────────────────────────────────────────────────────
   • Fórmula base: Precio Base × Horas
   • Precio por hora: ${precio_por_hora:,.0f}
   • Duración: {duracion} horas
   • Precio BASE: ${precio_por_hora:,.0f} × {duracion} = ${precio_base_calculado:,.0f}
   
   📊 **VALIDACIÓN DE CAPACIDAD:**
   • Personas ingresadas: {personas}
   • Capacidad máxima de la sala: {capacidad} personas
"""
            
            if personas <= capacidad:
                mensaje += f"   • ✅ Válido: {personas} no excede la capacidad máxima de {capacidad}\n"
            else:
                mensaje += f"   • ❌ ADVERTENCIA: {personas} excede la capacidad máxima de {capacidad}\n"
            
            mensaje += f"""
   🔄 **SOBRECARGA con 'equipo_adicional':**
"""
            
            if equipo_adicional:
                incremento = precio_base_calculado * 0.2
                precio_con_equipo = precio_base_calculado + incremento
                mensaje += f"""   • Equipo adicional: ✅ SÍ
   • Incremento: +20% sobre el precio base
   • Valor del incremento: ${incremento:,.0f}
   • Precio con equipo adicional: ${precio_base_calculado:,.0f} + ${incremento:,.0f} = ${precio_con_equipo:,.0f}
"""
            else:
                mensaje += f"""   • Equipo adicional: ❌ NO
   • No se aplica incremento
   • Precio sin equipo adicional: ${precio_base_calculado:,.0f}
"""
            
            precio_base_total = precio_base_calculado
            if equipo_adicional:
                precio_base_total = precio_base_calculado * 1.2
        
        # ========== CASO 2: SERVICIO DE EQUIPO ==========
        elif isinstance(self._servicio, AlquilerEquipos):
            tipo_equipo = self._servicio.tipo_equipo
            cantidad = parametros.get("cantidad", 1)
            seguro = parametros.get("seguro", False)
            
            # Calcular precio base (sin descuento)
            precio_base_calculado = precio_por_hora * duracion * cantidad
            
            mensaje += f"""
   💻 **SERVICIO: ALQUILER DE EQUIPOS**
   ───────────────────────────────────────────────────────────────────────────────
   • Fórmula base: Precio Base × Horas × Cantidad
   • Precio por hora por equipo: ${precio_por_hora:,.0f}
   • Duración: {duracion} horas
   • Cantidad de equipos: {cantidad}
   • Precio BASE: ${precio_por_hora:,.0f} × {duracion} × {cantidad} = ${precio_base_calculado:,.0f}
   
   🔄 **SOBRECARGA con 'seguro':**
"""
            
            if seguro:
                cargo_seguro = 5000
                precio_con_seguro = precio_base_calculado + cargo_seguro
                mensaje += f"""   • Seguro: ✅ SÍ
   • Cargo fijo por seguro: +${cargo_seguro:,.0f}
   • Precio con seguro: ${precio_base_calculado:,.0f} + ${cargo_seguro:,.0f} = ${precio_con_seguro:,.0f}
"""
            else:
                mensaje += f"""   • Seguro: ❌ NO
   • No se aplica cargo por seguro
   • Precio sin seguro: ${precio_base_calculado:,.0f}
"""
            
            precio_base_total = precio_base_calculado
            if seguro:
                precio_base_total = precio_base_calculado + 5000
        
        # ========== CASO 3: SERVICIO DE ASESORÍA ==========
        elif isinstance(self._servicio, AsesoriaEspecializada):
            nivel = self._servicio.nivel
            tema = parametros.get("tema", "No especificado")
            miembro_premium = parametros.get("miembro_premium", False)
            
            # Calcular precio base (sin descuento)
            precio_base_calculado = precio_por_hora * duracion
            
            mensaje += f"""
   📚 **SERVICIO: ASESORÍA ESPECIALIZADA**
   ───────────────────────────────────────────────────────────────────────────────
   • Fórmula base: Precio Base × Horas
   • Precio por hora: ${precio_por_hora:,.0f}
   • Duración: {duracion} horas
   • Precio BASE: ${precio_por_hora:,.0f} × {duracion} = ${precio_base_calculado:,.0f}
   • Nivel del experto: {nivel}
   • Tema de la asesoría: "{tema}"
   • Longitud del tema: {len(tema)} caracteres {'✅ Válido' if len(tema) >= 5 else '❌ Mínimo 5 caracteres'}
   
   🔄 **SOBRECARGA con 'miembro_premium':**
"""
            
            if miembro_premium:
                descuento = precio_base_calculado * 0.15
                precio_con_descuento = precio_base_calculado - descuento
                mensaje += f"""   • Miembro Premium: ✅ SÍ
   • Descuento aplicado: 15%
   • Valor del descuento: ${descuento:,.0f}
   • Precio con descuento: ${precio_base_calculado:,.0f} - ${descuento:,.0f} = ${precio_con_descuento:,.0f}
"""
            else:
                mensaje += f"""   • Miembro Premium: ❌ NO
   • No se aplica descuento
   • Precio sin descuento: ${precio_base_calculado:,.0f}
"""
            
            precio_base_total = precio_base_calculado
            if miembro_premium:
                precio_base_total = precio_base_calculado * 0.85
        
        # ========== SECCIÓN DE DESCUENTO ADICIONAL ==========
        if self._porcentaje_descuento > 0:
            valor_descuento = self._valor_descuento
            porcentaje = self._porcentaje_descuento
            mensaje += f"""
{linea_sep}
💸 **DESCUENTO ADICIONAL APLICADO A ESTA RESERVA:**
   • Porcentaje de descuento: {porcentaje:.0f}%
   • Valor del descuento: ${valor_descuento:,.0f}
   • Precio SIN descuento adicional: ${precio_base_total:,.0f}
   • Precio CON descuento adicional: ${costo_total:,.0f}
   • Ahorro total: ${valor_descuento:,.0f}
"""
        
        # ========== RESUMEN FINAL ==========
        mensaje += f"""
{linea_sep}
🎯 **RESUMEN FINAL DE ESTA RESERVA:**
   • Precio Base (sin ningún descuento): ${precio_base_total:,.0f}
   • Descuento aplicado: {self._porcentaje_descuento:.0f}%
   • Valor del descuento: ${self._valor_descuento:,.0f}
   • TOTAL A PAGAR: ${costo_total:,.0f}
{linea_sep}
✅ Esto demuestra que los MÉTODOS SOBRECARGADOS y el POLIMORFISMO
   están correctamente implementados en el sistema.
   
   El método `calcular_costo()` recibe parámetros variables (**kwargs)
   y se comporta de manera diferente según:
   1. El tipo de servicio (Sala, Equipo, Asesoría)
   2. Los parámetros extra ingresados (personas, equipo_adicional, cantidad, seguro, tema, miembro_premium)
"""
        
        return mensaje
    
    # ==================== MÉTODOS DE INFORMACIÓN =========================================================
    
    # =====================================================================================================
    # MÉTODO: obtener_info Retorna un diccionario con toda la información de la reserva
    # Incluye precio_base, porcentaje_descuento, valor_descuento y parametros_extra
    # =====================================================================================================
    def obtener_info(self) -> dict:
        
        return {
            "id": self._id, # ID de la reserva
            "cliente": self._cliente.nombre, # Nombre del Cliente
            "cliente_id": self._cliente.id, # ID del Cliente
            "servicio": self._servicio.nombre, # Nombre del servicio
            "servicio_id": self._servicio.id, # ID del servicio
            "duracion": self._duracion_horas, # Duración de horas
            "estado": self._estado, # Estado de la reserva
            "precio_base": self._precio_base_total,           # Precio sin descuento
            "costo_total": self._costo_total,                 # Precio con descuento
            "porcentaje_descuento": self._porcentaje_descuento, # % descuento aplicado
            "valor_descuento": self._valor_descuento,         # Valor en pesos del descuento
            "parametros_extra": self._parametros_extra,       # Parámetros reales usados
            "fecha": self._fecha_reserva.strftime("%Y-%m-%d %H:%M"),
            "fecha_obj": self._fecha_reserva
        }
    
    # ==================== PROPERTIES =====================================================================
    
    # =====================================================================================================
    # PROPERTIES (getters)
    # Permiten acceder a los atributos privados de forma controlada, sin exponerlos directamente.
    # =====================================================================================================
    
    # Retorna el ID
    @property
    def id(self) -> int:
        return self._id
    
    # Retorna el estado
    @property
    def estado(self) -> str:
        return self._estado
    
    # Retorna la fecha
    @property
    def fecha_reserva(self) -> datetime.datetime:
        return self._fecha_reserva
    
    # Retorna la duración de horas
    @property
    def duracion_horas(self) -> float:
        return self._duracion_horas
    
    # Retorna el tipo de servicio
    @property
    def servicio_id(self) -> int:
        return self._servicio.id
    
    # Retorna el precio base sin descuento
    @property
    def precio_base_total(self) -> float:
        
        return self._precio_base_total
    
    # Retorna el porcentaje del descuento
    @property
    def porcentaje_descuento(self) -> float:
        
        return self._porcentaje_descuento
    
    # Retorna el valor del descuento
    @property
    def valor_descuento(self) -> float:
        
        return self._valor_descuento
    
    # Retorna los parámetros extra que se usaron
    @property
    def parametros_extra(self) -> dict:
        
        return self._parametros_extra
    
    # Retorna el costo total
    @property
    def costo_total(self) -> float:
        
        return self._costo_total
    
    # =====================================================================================================
    # MÉTODO: esta_vencida, verifica si la reserva ya superó su fecha/hora de finalización
    # Retorna True si la reserva está vencida, False en caso contrario
    # =====================================================================================================
    def esta_vencida(self) -> bool:
        
        # Calcular la fecha/hora de finalización
        fecha_fin = self._fecha_reserva + datetime.timedelta(hours=self._duracion_horas)
        
        # Obtener la fecha/hora actual del sistema
        ahora = datetime.datetime.now()
        
        # Si la fecha_fin es menor o igual a ahora → la reserva ya venció
        return fecha_fin <= ahora
    
    