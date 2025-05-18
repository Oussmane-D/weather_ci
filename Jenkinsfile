pipeline {
    agent any             // ← Pas de Docker pour l’instant

    environment {
        TEST_REPORTS = 'tests/reports/*.xml'
    }

    stages {
        stage('Install deps') {
            steps {
                sh 'python -m pip install -r requirements-dev.txt'
            }
        }
        stage('Tests') {
            steps {
                sh 'pytest -q -s --junitxml=${TEST_REPORTS}'
            }
        }
    }

    post {
        always {
            junit "${env.TEST_REPORTS}"
        }
    }
}
