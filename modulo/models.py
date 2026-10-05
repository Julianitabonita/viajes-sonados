from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class ViajeSonado(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="viajes",
    )
    destino = models.CharField(max_length=100)
    pais = models.CharField(max_length=60)
    notas = models.TextField(blank=True)
    presupuesto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    fecha_tentativa = models.DateField()
    visitado = models.BooleanField(default=False)

    class Meta:
        ordering = ["fecha_tentativa"]
        verbose_name = "viaje soñado"
        verbose_name_plural = "viajes soñados"

    def clean(self):
        hoy = timezone.localdate()
        if self.fecha_tentativa:
            if not self.visitado and self.fecha_tentativa < hoy:
                raise ValidationError(
                    "Un viaje pendiente no puede tener una fecha tentativa pasada."
                )
            if self.visitado and self.fecha_tentativa > hoy:
                raise ValidationError(
                    "Un viaje visitado no puede tener una fecha futura."
                )

    @property
    def dias_restantes(self):
        return (self.fecha_tentativa - timezone.localdate()).days

    def __str__(self):
        return f"{self.destino}, {self.pais}"