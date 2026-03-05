# KaziLink (Django)

Plateforme web de mise en relation entre clients et prestataires verifies.

## Stack
- Django
- Django REST Framework
- Stripe Checkout (optionnel)
- Paiement manuel (optionnel)
- PostgreSQL (production) / SQLite (local debug)
- HTML/CSS responsive

## Modules
- `accounts`: inscription, connexion, profil et role (client/prestataire)
- `services`: categories et services publies par les prestataires
- `orders`: demandes de mission, suivi de statut, commission (10%), paiement Stripe ou manuel
- `reviews`: notes et avis sur missions terminees

## Lancement local
1. `py -m pip install -r requirements.txt`
2. Copier `.env.example` vers `.env`
3. Mettre `DEBUG=1` dans `.env`
4. Ajouter au minimum `SECRET_KEY`, `ALLOWED_HOSTS` et `CSRF_TRUSTED_ORIGINS`
5. `py manage.py migrate`
6. `py manage.py createsuperuser`
7. `py manage.py runserver`

## Variables d'environnement
Variables obligatoires en production:
- `SECRET_KEY`
- `DEBUG=0`
- `ALLOWED_HOSTS` (ex: `kazilink.onrender.com`)
- `CSRF_TRUSTED_ORIGINS` (ex: `https://kazilink.onrender.com`)
- `DATABASE_URL` (PostgreSQL)

Variables optionnelles paiements:
- `STRIPE_SECRET_KEY`
- `STRIPE_PUBLISHABLE_KEY`
- `STRIPE_WEBHOOK_SECRET`
- `MANUAL_PAYMENT_ENABLED` (`1` pour activer, sinon `0`)
- `MANUAL_PAYMENT_LABEL`
- `MANUAL_PAYMENT_NUMBER`
- `MANUAL_PAYMENT_HOLDER`
- `MANUAL_PAYMENT_NOTE`

## Deploiement Render
1. Pousser le projet sur GitHub.
2. Creer une base PostgreSQL sur Render.
3. Creer un `Web Service` Render connecte au repo.
4. Build command: `./build.sh`
5. Start command: `gunicorn config.wsgi:application`
6. Verifier les variables d'environnement obligatoires.
7. Redeployer.

## API
- `GET /api/accounts/profiles/`
- `GET /api/services/categories/`
- `GET/POST /api/services/providers/`
- `GET/POST /api/orders/missions/` (auth requis)
- `GET/POST /api/reviews/`
