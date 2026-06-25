# NetBackup Proxy API

API FastAPI qui sert de proxy simple pour consommer les APIs Veritas NetBackup de plusieurs master-servers.

Architecture volontairement modulaire:

```text
app/
  api/
    routes/         # endpoints FastAPI
    controllers/    # orchestration HTTP
  modules/
    referential/    # lecture des master-servers et credentials
    netbackup/      # client, parser et service NetBackup
  shared/           # HTTP client, OData helpers, case conversion, responses
```

Les services dans `app/modules/*` sont independants des routes et peuvent etre reutilises dans d'autres projets.

## Python

Projet cible: Python 3.6.

```bash
python3.6 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Lancer

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Ou via le script dev:

```bash
chmod +x scripts/run_dev.sh
./scripts/run_dev.sh
```

Docs:

- `http://localhost:8000/docs`
- `http://localhost:8000/openapi.json`

Swagger UI est servi en mode offline. Les fichiers JS/CSS/images sont embarques dans:

```text
app/static/swagger/
```

La VM n'a donc pas besoin d'acces Internet pour afficher `/docs`.

## Nginx

Un exemple de reverse proxy est fourni dans:

```text
nginx/netbackup-proxy-api.conf
```

Il contient deux modes:

- `/netbackup-proxy/` pour un load balancer qui route plusieurs microservices par chemin;
- `/` si ce microservice possede son propre virtual host.

Installation exemple:

```bash
sudo cp nginx/netbackup-proxy-api.conf /etc/nginx/conf.d/netbackup-proxy-api.conf
sudo nginx -t
sudo systemctl reload nginx
```

## Referential API

Le Referential API fournit la liste des master-servers et les credentials.

Endpoints attendus, configurables dans `.env`:

```env
REFERENTIAL_MASTER_SERVERS_PATH=/api/netbackup/master-servers
REFERENTIAL_MASTER_SERVER_PATH=/api/netbackup/master-servers/{hostname}
```

Filtres envoyes au Referential API:

- `region`
- `locality`
- `datacentre`
- `is_baas`
- `is_raas`

Reponse minimale attendue:

```json
{
  "hostname": "nbu01",
  "apiUrl": "https://nbu01.example.local",
  "login": "admin",
  "password": "secret",
  "region": "emea",
  "locality": "paris",
  "datacentre": "dc1",
  "isBaas": true,
  "isRaas": false
}
```

## Endpoints

```text
GET /api/v1/master-servers
GET /api/v1/master-servers/{hostname}

GET /api/v1/netbackup/policies
GET /api/v1/netbackup/policies/{policy_name}?hostname=nbu01

GET /api/v1/netbackup/jobs
GET /api/v1/netbackup/jobs/{job_id}?hostname=nbu01

GET /api/v1/netbackup/images
GET /api/v1/netbackup/images/{image_id}?hostname=nbu01
```

`masters` accepte une liste separee par virgules ou points-virgules:

```bash
curl "http://localhost:8000/api/v1/netbackup/policies?masters=nbu01,nbu02&limit=100"
```

Si `masters` est vide, l'API interroge tous les master-servers retournes par le Referential API.

## Filtres et pagination

Policies:

- filtres simples: `policy_name`, `policy_type`
- ils sont convertis en OData NetBackup: `policyName eq '...'`
- pagination simplifiee: `limit`, `offset`
- envoyee a NetBackup comme `page[limit]`, `page[offset]`

Jobs et images:

- filtres simples: `policy_name`, `client_name`, `status_code` pour jobs
- pagination simplifiee: `limit`, `offset`
- NetBackup est appele avec `page[limit]`
- puis l'API suit `meta.pagination.after` via `page[after]` jusqu'a remplir la demande, recevoir une liste vide ou recevoir un 404.

Filtre OData brut:

```bash
curl "http://localhost:8000/api/v1/netbackup/policies?policy_name=daily&$filter=active eq true"
```

Raw:

```bash
curl "http://localhost:8000/api/v1/netbackup/jobs?masters=nbu01&raw=true"
```

Quand `raw=true`, la reponse contient aussi l'objet NetBackup complet en `snake_case`.

## Chemins NetBackup

Les chemins sont configurables dans `.env`:

```env
NETBACKUP_LOGIN_PATH=/netbackup/login
NETBACKUP_POLICIES_PATH=/netbackup/config/policies
NETBACKUP_POLICY_DETAIL_PATH=/netbackup/config/policies/{policy_name}
NETBACKUP_JOBS_PATH=/netbackup/admin/jobs
NETBACKUP_JOB_DETAIL_PATH=/netbackup/admin/jobs/{job_id}
NETBACKUP_IMAGES_PATH=/netbackup/catalog/images
NETBACKUP_IMAGE_DETAIL_PATH=/netbackup/catalog/images/{image_id}
```

Ils sont volontairement configurables pour rester alignes avec votre version NetBackup/Veritas.
