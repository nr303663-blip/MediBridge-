# MediBridge — Testing & Deployment Checklist (Phase 6)

Run through this before considering the local build "live."

## Setup
- [ ] `./setup.sh` completes without errors (or manual steps in README)
- [ ] `python manage.py createsuperuser` done — admin can log in at `/admin/`
- [ ] `python manage.py seed_demo_data` run — demo doctors/patient/symptoms exist

## Automated tests
- [ ] `python manage.py test` passes (accounts, appointments, diagnostics)

## Manual walkthrough
- [ ] All modules functional — home, signup, login, dashboards load without error
- [ ] Patient signup → login → redirected to patient dashboard
- [ ] Doctor signup → account is `pending` → cannot reach dashboard until approved
- [ ] Admin approves a doctor from `/admin/` → doctor can now log in to dashboard
- [ ] Patient can search/filter doctors and view a doctor's profile
- [ ] Appointment booking flow works end-to-end (book → pending → visible to doctor)
- [ ] Doctor approve → patient sees "Approved" status
- [ ] Doctor decline → patient is auto-rebooked with another same-specialization doctor (or notified if none available)
- [ ] Self-diagnostic flow: select symptoms → prediction + confidence shown → recommended doctor → can book directly
- [ ] Responsive design holds up on a narrow (mobile) viewport — nav collapses to the ☰ toggle
- [ ] Non-owners can't access other users' data (e.g. a patient can't cancel another patient's appointment — enforced via `get_object_or_404(..., patient=request.user.patient_profile)`)
- [ ] CSRF tokens present on all forms (Django default — verify no `@csrf_exempt` was added)

## Backup & data safety
- [ ] `./backup.sh` produces a dated JSON dump + media tarball in `backups/`
- [ ] Restoring with `python manage.py loaddata <file>` on a clean DB works

## Go live (local)
- [ ] `DEBUG = False` for anything beyond your own machine, `ALLOWED_HOSTS` updated
- [ ] Real `DJANGO_SECRET_KEY` set via `.env`, not the default placeholder
- [ ] Payment gateway keys added to `.env` before enabling real transactions
- [ ] `python manage.py collectstatic` run if serving static files outside DEBUG mode

## Known gaps (documented, not silently missing)
- Payment gateway calls are modeled (Payment table + method/gateway choices) but not wired to live Stripe/Razorpay/PayPal APIs — currently a manual/COD-style status update. Swap in real SDK calls in `payments/views.py` when ready.
- The diagnostic engine (`diagnostics/ml_engine.py`) uses a transparent symptom-overlap scorer seeded via `seed_demo_data`, not a trained scikit-learn `.pkl`. It's built so a real model can replace the scoring function without changing any calling code — see the module docstring.
