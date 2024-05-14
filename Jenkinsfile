pipeline {
    agent any

    environment {
        AWS_CREDENTIALS = 'saml-jenkins-creds'  // ID for the stored AWS credentials in Jenkins
        AWS_DEFAULT_REGION = 'us-east-2'        // Region where your AWS resources are deployed
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
                    // Ensure the shell environment is appropriate for your Jenkins setup.
                    sh '''
                    python -m venv venv
                    source venv/bin/activate  // Use 'source' for Unix/Linux shells, adjust if on Windows
                    pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Build Lambda Package') {
            steps {
                sh 'sam build'
            }
        }

        stage('Deploy to AWS') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: AWS_CREDENTIALS]]) {
                    sh 'sam deploy --no-fail-on-empty-changeset --stack-name my-lambda-function --capabilities CAPABILITY_IAM --region $AWS_DEFAULT_REGION'
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
            script {
                // Clean up only if not on the master branch
                if (env.BRANCH_NAME != 'master') {
                    sh 'echo Cleaning up...'
                    sh 'rm -rf venv'
                }
            }
        }
    }
}
