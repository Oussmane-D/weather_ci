pipeline {
    /* ---------- AGENT ---------- */
    agent {
        docker {
            /* image officielle Python avec pip et pytest */
            image 'python:3.10-slim'
            /* on garde le même workspace */
            reuseNode true
            /* facultatif : exécuter en root pour installer libs */
            args '-u root:root'
        }
    }

    /* ---------- ENV / OPTIONS ---------- */
    environment {
        // exemple : répertoire virtuel où PyTest génère le rapport JUnit XML
        TEST_REPORTS = 'tests/reports/junit.xml'
    }
    options {
        // garde les 10 derniers builds
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    /* ---------- STAGES ---------- */
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
                // PyTest génère un rapport XML compréhensible par JUnit
                sh 'pytest -q -s --junitxml=${TEST_REPORTS}'
            }
        }

        stage('Build image') {
            steps {
                sh 'docker build -t weather_pipeline:$(git rev-parse --short HEAD) .'
            }
        }

        /* ajoutez ici vos étapes Push/Deploy si besoin */
    }

    /* ---------- POST ACTIONS ---------- */
    post {
        always {
            junit "${TEST_REPORTS}"                // récup. des résultats de tests
            archiveArtifacts artifacts: '**/*.log' // exemple
        }
        success {
            echo "✅ Build ${env.BUILD_NUMBER} OK"
        }
        failure {
            // envoyez un mail ou un Slack message (exemple avec mail)
            mail to: 'you@example.com',
                 subject: "❌ Job ${env.JOB_NAME} #${env.BUILD_NUMBER} FAILED",
                 body: "Voir les logs : ${env.BUILD_URL}"
        }
    }
}
