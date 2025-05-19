pipeline {
  // 1) On exécute sur n’importe quel agent (le master a Docker via le socket)
  agent any

  environment {
    // 2) On sépare le nom et le tag de l’image pour pouvoir les réutiliser proprement
    AIRFLOW_CI_IMAGE_NAME = 'oussmaned/airflow-ci'
    AIRFLOW_CI_IMAGE_TAG  = '2.9.1'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Lint & Tests') {
      steps {
        script {
          // 3) On utilise l’image CI qui contient déjà flake8 & pytest
          docker.image("${env.AIRFLOW_CI_IMAGE_NAME}:${env.AIRFLOW_CI_IMAGE_TAG}").inside {
            sh 'flake8 dags tests'
            sh 'pytest -q --junitxml=tests/pytest.xml'
          }
        }
      }
      post {
        always {
          junit 'tests/pytest.xml'
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          // 4) On build l’image avec le bon nom et tag
          docker.build(
            "${env.AIRFLOW_CI_IMAGE_NAME}:${env.AIRFLOW_CI_IMAGE_TAG}",
            '-f Dockerfile .'
          )
        }
      }
    }

    stage('Push Image') {
      steps {
        script {
          // 5) On push sur DockerHub (ou autre registry)
          docker.withRegistry('', 'dockerhub-credentials') {
            docker.image("${env.AIRFLOW_CI_IMAGE_NAME}:${env.AIRFLOW_CI_IMAGE_TAG}")
                  .push()
          }
        }
      }
    }

    stage('Deploy') {
      steps {
        // 6) Ton déploiement via docker-compose
        sh 'docker-compose up -d'
      }
    }
  }

  post {
    cleanup {
      cleanWs()
    }
  }
}
