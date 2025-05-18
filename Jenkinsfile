pipeline {
  agent any

  environment {
    REGISTRY = 'docker.io'
    IMAGE    = 'ouss/weather-airflow'
    TAG      = "${env.BUILD_NUMBER}"
  }

  stages {

    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Lint & Tests') {
      /* image plus léger + lint non-bloquant + rapport JUnit */
      agent { docker { image 'python:3.10-slim' } }
      steps {
        sh '''
          pip install --no-cache-dir -r requirements-dev.txt
          # Lint : on log les erreurs mais on ne coupe pas le pipeline
          flake8 dags tests || true
          # Tests unitaires + rapport JUnit pour Jenkins
          pytest -q --junitxml=tests/pytest.xml
        '''
      }
    }

    stage('Build image') {
      steps {
        sh 'docker build -t $REGISTRY/$IMAGE:$TAG .'
      }
    }

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

  post {
    always  { junit 'tests/**/pytest.xml' }
    failure { mail to: 'jenkins-ouss@ouss-d.com',
              subject: "🟥 Build ${env.BUILD_TAG} KO",
              body: "Voir Jenkins pour les détails." }
  }
}
