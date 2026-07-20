from django import forms
from .models import Symptom


class SymptomSelectForm(forms.Form):
    symptoms = forms.ModelMultipleChoiceField(
        queryset=Symptom.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Select the symptoms you're experiencing",
    )
    other_symptoms = forms.CharField(
        required=False,
        label="Other symptoms",
        widget=forms.Textarea(attrs={
            'placeholder': 'Describe any other symptoms here, such as dizziness, chills, or unusual sensations.',
            'rows': 4,
        }),
        help_text="Optional: include additional symptoms that are not listed above.",
    )
