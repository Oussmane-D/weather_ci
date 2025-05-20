pipeline {
  agent any

  environment {
    REGISTRY    = 'docker.io'
    REPOSITORY  = 'oussmaned/airflow-ci'
    IMAGE_TAG   = "${env.BUILD_NUMBER}"
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    // +----------------------------------------------------------------+
    // | 1) On vérifie que Docker est bien joignable                   |
    // +----------------------------------------------------------------+
    stage('Docker Info') {
      steps {
        sh 'docker version'
        sh 'docker info'
      }
    }

    // +----------------------------------------------------------------+
    // | 2) Lint & Tests sous Python (on force root pour pip)          |
    // +----------------------------------------------------------------+
    stage('Lint & Tests') {
      agent {
        docker {
          image 'python:3.10-slim'
          // run as root pour que pip installe en system-wide
          args  '-u root:root -v ${WORKSPACE}:/usr/src/app -w /usr/src/app'
        }
      }
      steps {
        sh '''
          pip install --upgrade pip setuptools
          pip install --no-cache-dir -r requirements-dev.txt \
            apache-airflow-providers-airbyte apache-airflow-providers-snowflake
          flake8 dags tests || true
          pytest -q --junitxml=tests/pytest.xml
        '''
      }
      post {
        always {
          junit 'tests/pytest.xml'
        }
      }
    }

    // +----------------------------------------------------------------+
    // | 3) Docker Login (nécessite un Credentials “docker-hub”)       |
    // +----------------------------------------------------------------+
    stage('Docker Login') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: 'docker-hub',
          usernameVariable: 'DOCKER_USER',
          passwordVariable: 'DOCKER_PASS'
        )]) {
          sh 'docker login -u $DOCKER_USER -p $DOCKER_PASS'
        }
      }
    }

    // +----------------------------------------------------------------+
    // | 4) Build & Push de l’image                                    |
    // +----------------------------------------------------------------+
    stage('Build Docker Image') {
      steps {
        sh 'docker build -t $REPOSITORY:$IMAGE_TAG .'
      }
    }

    stage('Push Docker Image') {
      steps {
        sh 'docker push $REPOSITORY:$IMAGE_TAG'
      }
    }

    // +----------------------------------------------------------------+
    // | 5) Déploiement via Docker Compose                             |
    // +----------------------------------------------------------------+
    stage('Deploy (Docker Compose)') {
      steps {
        // on utilise ‘docker compose’ (plugin Docker Compose v2)
        sh '''
          docker compose -f docker-compose.prod.yml pull
          docker compose -f docker-compose.prod.yml up -d
        '''
      }
    }
  }

  post {
    always {
      cleanWs()
    }
  }
}
