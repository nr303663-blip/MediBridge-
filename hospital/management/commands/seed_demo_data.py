from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import User
from hospital.models import HospitalInfo, Department, Facility, Testimonial
from doctors.models import Specialization, Doctor
from patients.models import Patient
from diagnostics.models import Symptom, Disease


class Command(BaseCommand):
    help = "Seed MediBridge with demo data: hospital info, departments, specializations, doctors, a patient, symptoms/diseases."

    @transaction.atomic
    def handle(self, *args, **options):
        # Hospital Info
        if not HospitalInfo.objects.exists():
            HospitalInfo.objects.create(
                name="MediBridge Hospital",
                about="A fully connected hospital platform for patients and doctors.",
                address="123 Health Street, Wellness City, IN",
                contact_phone="+91 98765 43210",
                contact_email="contact@medibridge.example",
                working_hours="Mon-Sat, 8:00 AM - 8:00 PM",
            )
            self.stdout.write(self.style.SUCCESS("Created HospitalInfo"))

        # Departments
        dept_names = ["Cardiology", "Dermatology", "General Medicine", "Orthopedics", "Pediatrics", "ENT"]
        departments = {}
        for name in dept_names:
            dept, _ = Department.objects.get_or_create(name=name, defaults={
                'description': f"{name} department providing specialist care."
            })
            departments[name] = dept
        self.stdout.write(self.style.SUCCESS(f"Ensured {len(dept_names)} departments"))

        # Facilities
        for name, desc in [
            ("24/7 Emergency Care", "Round-the-clock emergency response team."),
            ("Diagnostic Lab", "In-house pathology and imaging."),
            ("Pharmacy", "On-site pharmacy for prescriptions."),
            ("ICU", "Fully-equipped intensive care unit."),
        ]:
            Facility.objects.get_or_create(name=name, defaults={'description': desc})

        # Testimonials
        if not Testimonial.objects.exists():
            Testimonial.objects.create(
                patient_name="Aditi Sharma", rating=5,
                message="Booking an appointment took two minutes and the doctor was excellent."
            )
            Testimonial.objects.create(
                patient_name="Rohan Mehta", rating=5,
                message="The self-diagnosis tool pointed me to the right specialist immediately."
            )

        # Specializations
        spec_map = {
            "Cardiology": "Cardiology",
            "Dermatology": "Dermatology",
            "General Medicine": "General Medicine",
            "Orthopedics": "Orthopedics",
            "Pediatrics": "Pediatrics",
            "ENT": "ENT",
        }
        specializations = {}
        for dept_name, spec_name in spec_map.items():
            spec, _ = Specialization.objects.get_or_create(
                name=spec_name, defaults={'department': departments[dept_name]}
            )
            specializations[spec_name] = spec
        self.stdout.write(self.style.SUCCESS(f"Ensured {len(specializations)} specializations"))

        # Demo doctors (one per specialization, approved & available)
        demo_doctors = [
            ("dr_asha", "Asha", "Verma", "Cardiology", 12, 1500),
            ("dr_karan", "Karan", "Singh", "Dermatology", 8, 900),
            ("dr_neha", "Neha", "Iyer", "General Medicine", 6, 500),
            ("dr_vikram", "Vikram", "Rao", "Orthopedics", 15, 1800),
            ("dr_priya", "Priya", "Nair", "Pediatrics", 10, 800),
            ("dr_arjun", "Arjun", "Das", "ENT", 7, 700),
        ]
        created_doctors = 0
        for username, first, last, spec_name, exp, fee in demo_doctors:
            if User.objects.filter(username=username).exists():
                continue
            user = User.objects.create_user(
                username=username, email=f"{username}@medibridge.example",
                password="DemoPass123!", first_name=first, last_name=last,
                role=User.Role.DOCTOR,
            )
            Doctor.objects.create(
                user=user, specialization=specializations[spec_name],
                experience_years=exp, qualification="MBBS, MD",
                consultation_fee=fee, is_available=True,
                approval_status=Doctor.ApprovalStatus.APPROVED,
                bio=f"Experienced {spec_name.lower()} specialist dedicated to patient care.",
            )
            created_doctors += 1
        self.stdout.write(self.style.SUCCESS(f"Created {created_doctors} demo doctors (password: DemoPass123!)"))

        # Demo patient
        if not User.objects.filter(username="demo_patient").exists():
            patient_user = User.objects.create_user(
                username="demo_patient", email="demo_patient@medibridge.example",
                password="DemoPass123!", first_name="Demo", last_name="Patient",
                role=User.Role.PATIENT,
            )
            Patient.objects.create(user=patient_user, age=29, gender='M', contact_number="9999999999")
            self.stdout.write(self.style.SUCCESS("Created demo patient (username: demo_patient / password: DemoPass123!)"))

        # Symptoms
        symptom_names = [
            "Fever", "Cough", "Headache", "Chest Pain", "Shortness of Breath",
            "Skin Rash", "Itching", "Joint Pain", "Swelling", "Sore Throat",
            "Runny Nose", "Fatigue", "Nausea", "Ear Pain", "Abdominal Pain",
            "Dizziness", "Chills", "Vomiting", "Diarrhea", "Palpitations",
            "Blurred Vision", "Anxiety", "Back Pain", "Loss of Appetite", "Facial Pain",
        ]
        symptoms = {}
        for name in symptom_names:
            s, _ = Symptom.objects.get_or_create(name=name)
            symptoms[name] = s
        self.stdout.write(self.style.SUCCESS(f"Ensured {len(symptom_names)} symptoms"))

        # Diseases mapped to specializations + typical symptoms (drives ml_engine scoring)
        disease_defs = [
            ("Common Cold", "General Medicine", ["Cough", "Runny Nose", "Sore Throat", "Fatigue"]),
            ("Influenza", "General Medicine", ["Fever", "Cough", "Headache", "Fatigue", "Chills"]),
            ("Coronary Artery Disease", "Cardiology", ["Chest Pain", "Shortness of Breath", "Fatigue", "Palpitations"]),
            ("Eczema", "Dermatology", ["Skin Rash", "Itching", "Swelling"]),
            ("Arthritis", "Orthopedics", ["Joint Pain", "Swelling", "Fatigue", "Back Pain"]),
            ("Ear Infection", "ENT", ["Ear Pain", "Fever", "Headache", "Runny Nose"]),
            ("Gastritis", "General Medicine", ["Abdominal Pain", "Nausea", "Fatigue", "Loss of Appetite"]),
            ("Migraine", "General Medicine", ["Headache", "Nausea", "Blurred Vision", "Sensitivity to Light"]),
            ("Food Poisoning", "General Medicine", ["Nausea", "Vomiting", "Diarrhea", "Abdominal Pain"]),
            ("Sinusitis", "ENT", ["Runny Nose", "Headache", "Sore Throat", "Facial Pain"]),
            ("Panic Attack", "General Medicine", ["Palpitations", "Shortness of Breath", "Dizziness", "Anxiety"]),
        ]
        for name, spec_name, symptom_list in disease_defs:
            disease, _ = Disease.objects.get_or_create(
                name=name,
                defaults={
                    'description': f"{name} — consult a {spec_name} specialist for proper diagnosis.",
                    'recommended_specialization': specializations[spec_name],
                }
            )
            disease.typical_symptoms.set([symptoms[s] for s in symptom_list])
        self.stdout.write(self.style.SUCCESS(f"Ensured {len(disease_defs)} diseases with symptom mappings"))

        self.stdout.write(self.style.SUCCESS(
            "\nDemo data ready. Log in as demo_patient or any dr_* account (password: DemoPass123!)."
        ))
