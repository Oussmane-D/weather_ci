pipeline {
    agent {
        docker {
            image 'python:3.10-slim'
            args  '-u 0:0'          // optionnel : évite des soucis de droits
            reuseNode true
        }
    }

    environment {
        TEST_REPORTS = 'tests/reports/*.xml'
        // éventuellement d’autres variables (AIRFLOW_, etc.)
    }

    stages {
        stage('Install deps') {
            steps {
                sh 'pip install -r requirements-dev.txt'
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
            junit allowEmptyResults: true, testResults: "${env.TEST_REPORTS}"
        }
        failure {
            echo "❌ Build ${currentBuild.displayName} KO"
        }
        success {
            echo "✅ Build ${currentBuild.displayName} OK"
        }
    }
}
