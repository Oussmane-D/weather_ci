pipeline {
    /* ───────────── 1. Agent par défaut (checkout + build/push/deploy) ───────────── */
    agent any

    environment {
        REGISTRY = 'docker.io'
        IMAGE    = 'ouss/weather-airflow'
        TAG      = "${env.BUILD_NUMBER}"
    }

    stages {

        /* ───────────── 2. Récupération du code ───────────── */
        stage('Checkout') {
            steps { checkout scm }
        }

        /* ───────────── 3. Lint & Tests ───────────── */
        stage('Lint & Tests') {
            agent {
                docker {
                    image 'python:3.10-slim'
                    /* on lance le conteneur en root pour que pip puisse écrire */
                    args  '-u 0:0'
                    reuseNode true
                }
            }
            steps {
                sh '''
                  pip install --no-cache-dir -r requirements-dev.txt
                  flake8 dags tests
                  pytest -q --junitxml=tests/pytest.xml
                '''
            }
            post {
                always {
                    /* ne casse pas le build si le rapport n’existe pas */
                    junit allowEmptyResults: true, testResults: 'tests/pytest.xml'
                }
            }
        }

        /* ───────────── 4. Build de l’image ───────────── */
        stage('Build image') {
            steps {
                sh 'docker build -t $REGISTRY/$IMAGE:$TAG .'
            }
        }

        /* ───────────── 5. Push vers Docker Hub ───────────── */
        stage('Push image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'docker-hub',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS')])
                {
                    sh '''
                      echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin $REGISTRY
                      docker push $REGISTRY/$IMAGE:$TAG
                    '''
                }
            }
        }

        /* ───────────── 6. Déploiement en prod ───────────── */
        stage('Deploy (Docker Compose)') {
            when { branch 'main' }
            steps {
                sshagent(credentials: ['ssh-prod']) {
                    sh '''
                      ssh prod "
                        docker pull $REGISTRY/$IMAGE:$TAG &&
                        docker compose -f ~/airflow_weather/docker-compose.yaml \
                          up -d --force-recreate webserver scheduler
                      "
                    '''
                }
            }
        }
    }

    /* ───────────── 7. Notifications globales ───────────── */
    post {
        failure {
            mail to: 'jenkins-ouss@ouss-d.com',
                 subject: "🟥 Build ${env.BUILD_TAG} KO",
                 body: "Le pipeline a échoué. Voir Jenkins pour les détails."
        }
    }
}
