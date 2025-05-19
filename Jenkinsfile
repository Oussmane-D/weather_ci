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

    stage('Lint & Tests') {
      agent {
        docker {
          image 'python:3.10-slim'
          args  '-v $PWD:/usr/src/app -w /usr/src/app'
        }
      }
      steps {
        sh '''
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

    stage('Deploy (Docker Compose)') {
      steps {
        sh '''
          docker-compose -f docker-compose.prod.yml pull
          docker-compose -f docker-compose.prod.yml up -d
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
