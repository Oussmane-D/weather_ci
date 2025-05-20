FROM python:3.10-slim

# 1) Définir un répertoire de travail
WORKDIR /app

# 2) Copier et installer les dépendances
COPY requirements-dev.txt /app/requirements-dev.txt
RUN pip install --no-cache-dir -r requirements-dev.txt

# 3) Copier le reste de votre code
COPY . /app

# 4) Commande par défaut (à adapter)
CMD ["bash"]
