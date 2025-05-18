pipeline {
    /* 1️⃣  Agent docker – nécessite Docker accessible */
    agent {
        docker {
            image 'python:3.10-slim'
            reuseNode true               // conserve le workspace
            args '-u root:root'          // pip install en root si besoin
        }
    }

    /* 2️⃣  Variables disponibles partout */
    environment {
        TEST_REPORTS = 'tests/reports/junit.xml'
    }

    stages {

        stage('Install deps') {
            steps {
                sh 'pip install -r requirements-dev.txt'
            }
        }

        stage('Lint') {
            steps {
                sh 'pip install flake8 && flake8 dags tests'
            }
        }

        stage('Unit tests') {
            steps {
                sh 'pytest -q -s --junitxml=${TEST_REPORTS}'
            }
        }

        /* autres stages (Build, Push, Deploy…) */
    }

    /* 3️⃣  Post-actions : toujours au moins une étape par branche */
    post {
        always {
            junit "${env.TEST_REPORTS}"
        }
        success {
            echo "✅ Build ${env.BUILD_NUMBER} OK"
        }
        failure {
            echo "❌ Build ${env.BUILD_NUMBER} KO"
            // mail(...)  <-- commentez ou configurez SMTP avant
        }
    }
}
