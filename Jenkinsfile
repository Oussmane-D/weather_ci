pipeline {
  /*------------------------------------------
   | 1) On cible un noeud qui a Docker installé
   |   (ou monte le socket comme ci-dessus) */
  agent { label 'docker' }

  environment {
    AIRFLOW_CI_IMAGE = 'oussmaned/airflow-ci:2.9.1'
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
          // 2) On utilise l’image qui contient déjà flake8/pytest
          docker.image(env.AIRFLOW_CI_IMAGE).inside {
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
          docker.build("oussmaned/airflow-ci:${env.AIRFLOW_CI_IMAGE_TAG}", '-f Dockerfile .')
        }
      }
    }

    stage('Push Image') {
      steps {
        script {
          docker.withRegistry('', 'dockerhub-credentials') {
            docker.image("oussmaned/airflow-ci:${env.AIRFLOW_CI_IMAGE_TAG}").push()
          }
        }
      }
    }

    stage('Deploy') {
      steps {
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
