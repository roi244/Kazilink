# KaziLink MVP (Django)

Plateforme web panafricaine de mise en relation entre clients et prestataires verifies.

## Stack
- Django
- Django REST Framework
- Stripe Checkout (optionnel)
- Paiement manuel (Mobile Money / virement)
- PostgreSQL (prod) / SQLite (dev)
- HTML/CSS responsive

## Modules
- `accounts`: inscription, connexion, profil et role (client/prestataire)
- `services`: categories et services publies par les prestataires
- `orders`: demandes de mission, suivi de statut, commission (10%), paiement Stripe ou manuel
- `reviews`: notes et avis sur missions terminees

## Lancement local
1. `py -m pip install -r requirements.txt`
2. `py manage.py migrate`
3. `py manage.py createsuperuser`
4. `py manage.py runserver`

## Variables d'environnement (important)
- `SECRET_KEY`
- `DEBUG` (`1` en local, `0` en production)
- `ALLOWED_HOSTS` (ex: `kazilink.onrender.com`)
- `CSRF_TRUSTED_ORIGINS` (ex: `https://kazilink.onrender.com`)
- `DATABASE_URL` (PostgreSQL en production)

### Paiement manuel (recommande pour demarrage rapide)
Variables optionnelles:
- `MANUAL_PAYMENT_ENABLED=1`
- `MANUAL_PAYMENT_LABEL="Mobile Money / Virement"`
- `MANUAL_PAYMENT_NUMBER="+250 7XX XXX XXX"`
- `MANUAL_PAYMENT_HOLDER="KaziLink"`
- `MANUAL_PAYMENT_NOTE="Apres paiement, saisissez la reference de transaction."`

### Paiement Stripe (optionnel)
Variables:
- `STRIPE_SECRET_KEY`
- `STRIPE_PUBLISHABLE_KEY`
- `STRIPE_WEBHOOK_SECRET`

Routes:
- Checkout client: `GET /missions/paiement/<order_id>/checkout/`
- Paiement manuel: `GET/POST /missions/paiement/<order_id>/manuel/`
- Validation manuelle: `GET /missions/paiement/<order_id>/valider-manuel/`
- Webhook Stripe: `POST /missions/webhooks/stripe/`

## Deploiement Render (recommande)
1. Pousser ce projet sur GitHub.
2. Creer une base PostgreSQL sur Render.
3. Creer un `Web Service` Render connecte au repo.
4. Build command: `./build.sh`
5. Start command: `gunicorn config.wsgi:application`
6. Ajouter les variables d'environnement (`SECRET_KEY`, `DEBUG=0`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `DATABASE_URL`).
7. Redeployer.

## API
- `GET /api/accounts/profiles/`
- `GET /api/services/categories/`
- `GET/POST /api/services/providers/`
- `GET/POST /api/orders/missions/` (auth requis)
- `GET/POST /api/reviews/`
