pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'job_portal'
        BUILD_TAG = "${DOCKER_IMAGE}:${BUILD_NUMBER}"
    }

    stages {
        stage('Clone Repository') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'fdc92cdd-ab3a-497c-8976-218341fc7caa', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                        git branch: 'restapi',
                            url: "https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/living-ghost/Job_Portal.git"
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${BUILD_TAG}")
                }
            }
        }

        stage('Push to Docker Registry') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials-id', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        docker.withRegistry('https://hub.docker.com/repositories/living9host', 'dockerhub-credentials-id') {
                            docker.image("${BUILD_TAG}").push()
                        }
                    }
                }
            }
        }

        stage('Deploy Containers') {
            steps {
                sh 'docker-compose up -d'
            }
        }

        stage('Run Django Migrations') {
            steps {
                sh 'docker-compose exec django python manage.py migrate'
            }
        }

        stage('Collect Static Files') {
            steps {
                sh 'docker-compose exec django python manage.py collectstatic --noinput'
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed.'
        }
        success {
            echo 'Pipeline executed successfully.'
        }
        failure {
            echo 'Pipeline execution failed.'
        }
    }
}