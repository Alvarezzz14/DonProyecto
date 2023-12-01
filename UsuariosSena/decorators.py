from functools import wraps
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse

def verificar_cuentadante(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        # Verificar si el usuario tiene el atributo 'cuentadante' con los valores permitidos
        if request.user.is_authenticated and request.user.cuentadante in ['superAdmin', 'adminD']:
            # Si tiene los permisos, ejecutar la función original de la vista
            return func(request, *args, **kwargs)
        else:
            # Si no tiene los permisos, redirigir a alguna página o mostrar un mensaje
            return JsonResponse({'mensaje': 'No tiene permisos para acceder a esta vista.'}, status=403)

    return wrapper


def verificar_superadmin(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        # Verificar si el usuario tiene el atributo 'cuentadante' con los valores permitidos
        if request.user.is_authenticated and request.user.cuentadante in ['superAdmin']:
            # Si tiene los permisos, ejecutar la función original de la vista
            return func(request, *args, **kwargs)
        else:
            # Si no tiene los permisos, redirigir a alguna página o mostrar un mensaje
            return JsonResponse({'mensaje': 'No tiene permisos para acceder a esta vista.'}, status=403)
        
    return wrapper
