# =========================================================================================================
# EXCEPCIONES PERSONALIZADAS DEL SISTEMA
# =========================================================================================================

# =========================================================================================================
# class SistemaFJError, clase base para todas las excepciones personalizadas del sistema
# =========================================================================================================
class SistemaFJError(Exception):
    
    pass

# =========================================================================================================
# class ClienteInvalidoError, Se lanza cuando el email, teléfono o cédula no cumplen el formato esperado
# =========================================================================================================
class ClienteInvalidoError(SistemaFJError):
    
    pass

# =========================================================================================================
# class ServicioNoDisponibleError, se lanza si el servicio está desactivado o sus parámetros son inválidos
# =========================================================================================================
class ServicioNoDisponibleError(SistemaFJError):
    
    pass

# =========================================================================================================
# class ReservaInvalidaErrorr, se lanza si la duración es inválida, cliente inactivo, etc
# =========================================================================================================
class ReservaInvalidaError(SistemaFJError):

    pass

# =========================================================================================================
# class EstadoReservaInvalidoError, se lanza cuando se intenta confirmar una reserva ya cancelada, etc
# =========================================================================================================
class EstadoReservaInvalidoError(SistemaFJError):
    
    pass

# =========================================================================================================
# class FechaNoDisponibleError, se lanza cuando se intenta reservar un servicio en un horario ya ocupado
# =========================================================================================================
class FechaNoDisponibleError(SistemaFJError):
    
    pass