from django.contrib import admin
from .models import Symptom, Disease, DiagnosisRequest

admin.site.register(Symptom)


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'recommended_specialization')
    filter_horizontal = ('typical_symptoms',)
    search_fields = ('name',)


@admin.register(DiagnosisRequest)
class DiagnosisRequestAdmin(admin.ModelAdmin):
    list_display = ('patient', 'predicted_disease', 'confidence_score', 'recommended_doctor', 'created_at')
    list_filter = ('predicted_disease',)
    readonly_fields = ('created_at',)
