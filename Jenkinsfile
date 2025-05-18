pipeline {
    agent any                     // Jenkins contrôleur ou agent qui a Docker

    environment {
        IMAGE_TAG = "weather-ci:${env.BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Lint & Tests') {
            agent { docker { image 'python:3.10' reuseNode true } }
            steps {
                sh '''
                  pip install -r requirements-dev.txt
                  pytest --junitxml=test-results/unit.xml
                '''
            }
            post {
                always {
                    junit 'test-results/**/*.xml'            // ← chemin réel
                }
            }
        }

        stage('Build image') {
            steps {
                sh "docker build -t $IMAGE_TAG ."
            }
        }

        stage('Push image') {
            when { branch 'main' }
            steps {
                withCredentials([string(credentialsId: 'dockerhub-token',
                                         variable: 'DOCKER_TOKEN')]) {
                    sh '''
                      echo "$DOCKER_TOKEN" | docker login -u youruser --password-stdin
                      docker tag $IMAGE_TAG youruser/weather-ci:$IMAGE_TAG
                      docker push youruser/weather-ci:$IMAGE_TAG
                    '''
                }
            }
        }

        stage('Deploy (Docker Compose)') {
            when { branch 'main' }
            steps {
                sh 'docker compose down --remove-orphans'
                sh 'docker compose pull && docker compose up -d'
            }
        }
    }

    post {
        failure {
            // retirer ou configurer correctement le mailer
            // mail to: 'ops@example.com', subject: "Build failed", body: "..."
        }
    }
}
