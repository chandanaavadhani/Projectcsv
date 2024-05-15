pipeline {
    agent any

    environment {
        AWS_CREDENTIALS = 'saml-jenkins-creds'
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

        stage('Build Lambda Package') {
            steps {
                bat '''
                venv\\Scripts\\activate.bat
                "C:\\Program Files\\Amazon\\AWSSAMCLI\\bin\\sam.exe" build
                '''
            }
        }

        stage('Deploy to AWS') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: AWS_CREDENTIALS]]) {
                    bat 'sam deploy --no-fail-on-empty-changeset --stack-name my-lambda-function --capabilities CAPABILITY_IAM --region %AWS_DEFAULT_REGION%'
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
