pipeline {
    agent any

    environment {
        AWS_CREDENTIALS = 'saml-jenkins-creds'  // Make sure this is properly configured in Jenkins Credentials
        AWS_DEFAULT_REGION = 'us-east-2'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                script {
                    bat '''
                    "C:\\Program Files\\python.exe" -m venv venv
                    venv\\Scripts\\activate.bat
                    pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Deploy Using Serverless') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: AWS_CREDENTIALS]]) {
                    bat '''
                    venv\\Scripts\\activate.bat
                    set AWS_ACCESS_KEY_ID=%AWS_ACCESS_KEY_ID%
                    set AWS_SECRET_ACCESS_KEY=%AWS_SECRET_ACCESS_KEY%
                    set AWS_SESSION_TOKEN=%AWS_SESSION_TOKEN%
                    serverless deploy --stage dev --region us-east-2
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment succeeded!'
        }
        failure {
            echo 'Deployment failed.'
        }
        always {
            bat 'echo Cleaning up...'
            bat 'rd /s /q venv'
        }
    }
}