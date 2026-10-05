from django import forms

from .models import ViajeSonado


class ViajeSonadoForm(forms.ModelForm):
    class Meta:
        model = ViajeSonado
        fields = ["destino", "pais", "notas", "presupuesto", "fecha_tentativa", "visitado"]
        widgets = {
            "destino": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: Machu Picchu"}
            ),
            "pais": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ej: Perú"}
            ),
            "notas": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "presupuesto": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "fecha_tentativa": forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
                format="%Y-%m-%d",
            ),
            "visitado": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }