pipeline {
  agent { label 'docker' }         // ou node docker-ready

  environment {
    CI_IMAGE = 'oussmaned/airflow-ci:2.9.1'
    IMAGE_TAG = "myrepo/weather-ci:${env.BUILD_NUMBER}"
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
          docker.image(CI_IMAGE).inside {
            sh 'flake8 dags tests'
            sh 'pytest -q --junitxml=tests/pytest.xml'
          }
        }
        junit 'tests/pytest.xml'
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          docker.build(IMAGE_TAG)
        }
      }
    }

    stage('Push Image') {
      steps {
        script {
          docker.withRegistry('https://index.docker.io/v1/', 'docker-creds') {
            docker.image(IMAGE_TAG).push()
          }
        }
      }
    }

    stage('Deploy') {
      steps {
        script {
          // Ex : mise à jour d’un stack docker-compose sur prod
          sh 'ssh deploy@server "cd /srv/weather && docker-compose pull && docker-compose up -d"'
        }
      }
    }
  }

  post {
    always {
      cleanWs()
    }
    success {
      mail to: 'team@exemple.com', subject: "Build #${env.BUILD_NUMBER} réussi", body: "Bravo !"
    }
    failure {
      mail to: 'team@exemple.com', subject: "Build #${env.BUILD_NUMBER} échoué", body: "Oups…"
    }
  }
}
