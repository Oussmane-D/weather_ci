pipeline {
  /* --- Agent principal ---------------------------------------------------- */
  agent any

  /* --- Variables d’environnement partagées -------------------------------- */
  environment {
    REGISTRY = 'docker.io'
    IMAGE    = 'ouss/weather-airflow'
    TAG      = "${env.BUILD_NUMBER}"
  }

  /* ----------------------------- STAGES ----------------------------------- */
  stages {

    /* 1. Récupération du dépôt */
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    /* 2. Lint & Tests (dans un conteneur Python 3.10) */
    stage('Lint & Tests') {
      agent {
        docker {
          image 'python:3.10-slim'
          args  '-u root:root'      // évite les erreurs de permission pip
          reuseNode true
        }
      }
      steps {
        sh '''
          # Dépendances de dev + provider Airbyte
          pip install --no-cache-dir -r requirements-dev.txt \
               apache-airflow-providers-airbyte \
               apache-airflow-providers-snowflake


          # Lint : on loggue mais on ne bloque pas la build
          flake8 dags tests || true

          # Tests + rapport JUnit
          pytest -q --junitxml=tests/pytest.xml
        '''
      }
    }

    /* 3. Construction de l’image Docker */
    stage('Build image') {
      steps {
        sh 'docker build -t $REGISTRY/$IMAGE:$TAG .'
      }
    }

    /* 4. Push vers Docker Hub */
    stage('Push image') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'docker-hub',
                                          usernameVariable: 'DOCKER_USER',
                                          passwordVariable: 'DOCKER_PASS')]) {
          sh '''
            echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin $REGISTRY
            docker push $REGISTRY/$IMAGE:$TAG
          '''
        }
      }
    }

    /* 5. Déploiement (uniquement sur la branche main) */
    stage('Deploy (Docker Compose)') {
      when { branch 'main' }
      steps {
        sshagent(credentials: ['ssh-prod']) {
          sh '''
            ssh prod "docker pull $REGISTRY/$IMAGE:$TAG &&
                      docker compose -f ~/airflow_weather/docker-compose.yaml \
                        up -d --force-recreate webserver scheduler"
          '''
        }
      }
    }
  }

  /* --------------------------- POST ACTIONS ------------------------------- */
  post {
    /* Publie toujours les résultats de tests (même en échec) */
    always {
      junit 'tests/pytest.xml'
    }

    /* Notifie par mail en cas d’échec du pipeline */
    failure {
      mail to: 'jenkins-ouss@ouss-d.com',
           subject: "🟥 Build ${env.BUILD_TAG} KO",
           body: "La build Jenkins a échoué, voir la console pour le détail."
    }
  }
}
