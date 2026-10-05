from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ViajeSonadoForm
from .models import ViajeSonado


@login_required(login_url="/admin/login/")
def lista_viajes(request):
    todos = ViajeSonado.objects.filter(usuario=request.user)

    estadisticas = {
        "total": todos.count(),
        "visitados": todos.filter(visitado=True).count(),
        "pendientes": todos.filter(visitado=False).count(),
        "presupuesto_pendiente": todos.filter(visitado=False).aggregate(
            total=Sum("presupuesto")
        )["total"]
        or 0,
    }

    viajes = todos

    pais = request.GET.get("pais", "").strip()
    visitado = request.GET.get("visitado", "")

    if pais:
        viajes = viajes.filter(pais__icontains=pais)
    if visitado == "si":
        viajes = viajes.filter(visitado=True)
    elif visitado == "no":
        viajes = viajes.filter(visitado=False)

    paginador = Paginator(viajes, 3)
    pagina = paginador.get_page(request.GET.get("page"))

    parametros = request.GET.copy()
    parametros.pop("page", None)

    contexto = {
        "viajes": pagina,
        "pais": pais,
        "visitado": visitado,
        "parametros": parametros.urlencode(),
        "estadisticas": estadisticas,
    }
    return render(request, "modulo/lista.html", contexto)


@login_required(login_url="/admin/login/")
def detalle_viaje(request, pk):
    viaje = get_object_or_404(ViajeSonado, pk=pk, usuario=request.user)
    return render(request, "modulo/detalle.html", {"viaje": viaje})


@login_required(login_url="/admin/login/")
def crear_viaje(request):
    if request.method == "POST":
        form = ViajeSonadoForm(request.POST)
        if form.is_valid():
            viaje = form.save(commit=False)
            viaje.usuario = request.user
            viaje.save()
            messages.success(request, f"¡Viaje a {viaje.destino} agregado a tu lista!")
            return redirect("modulo:lista")
    else:
        form = ViajeSonadoForm()
    return render(
        request,
        "modulo/formulario.html",
        {"form": form, "titulo": "Nuevo viaje soñado"},
    )


@login_required(login_url="/admin/login/")
def editar_viaje(request, pk):
    viaje = get_object_or_404(ViajeSonado, pk=pk, usuario=request.user)
    if request.method == "POST":
        form = ViajeSonadoForm(request.POST, instance=viaje)
        if form.is_valid():
            form.save()
            messages.success(request, f"Los cambios en {viaje.destino} se guardaron.")
            return redirect("modulo:detalle", pk=viaje.pk)
    else:
        form = ViajeSonadoForm(instance=viaje)
    return render(
        request,
        "modulo/formulario.html",
        {"form": form, "titulo": "Editar viaje soñado"},
    )


@login_required(login_url="/admin/login/")
def eliminar_viaje(request, pk):
    viaje = get_object_or_404(ViajeSonado, pk=pk, usuario=request.user)
    if request.method == "POST":
        destino = viaje.destino
        viaje.delete()
        messages.success(request, f"El viaje a {destino} fue eliminado.")
        return redirect("modulo:lista")
    return render(request, "modulo/eliminar.html", {"viaje": viaje})