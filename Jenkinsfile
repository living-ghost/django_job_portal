pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS_ID = 'jenkins-docker-integration'
        DOCKER_IMAGE = 'living9host/job_portal'
        BUILD_TAG = "${DOCKER_IMAGE}:${BUILD_NUMBER}"

        // Environment variables
        DEBUG = "True"
        ALLOWED_HOSTS = 'localhost'
        SECRET_KEY = credentials('django-secret-key-id')
        
        DB_NAME = 'job_portal_dev'
        DB_USER = 'portal_dev'
        DB_PASSWORD = credentials('django-db-password-id')
        DB_HOST = 'db'
        DB_PORT = '5432'

        PGADMIN_DEFAULT_EMAIL = 'akhiiltkaniiparampiil@gmail.com'
        PGADMIN_DEFAULT_PASSWORD = credentials('django-db-password-id')
        
        EMAIL_HOST_PASSWORD = credentials('django-email-password-id')
    }

    stages {
        stage('Clone Repository') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'github-jenkins-integration', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                        git branch: 'dev-server',
                            url: "https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/living-ghost/Job_Portal.git"
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    try {
                        docker.build("${BUILD_TAG}", "--build-arg SECRET_KEY=${env.SECRET_KEY} --build-arg DB_NAME=${env.DB_NAME} --build-arg DB_USER=${env.DB_USER} --build-arg DB_PASSWORD=${env.DB_PASSWORD} --build-arg DB_HOST=${env.DB_HOST} --build-arg DB_PORT=${env.DB_PORT} --build-arg CELERY_BROKER_URL=${env.CELERY_BROKER_URL} --build-arg CELERY_ACCEPT_CONTENT=${env.CELERY_ACCEPT_CONTENT} --build-arg CELERY_RESULT_SERIALIZER=${env.CELERY_RESULT_SERIALIZER} --build-arg CELERY_TASK_SERIALIZER=${env.CELERY_TASK_SERIALIZER} --build-arg CELERY_TIMEZONE=${env.CELERY_TIMEZONE} --build-arg CELERY_RESULT_BACKEND=${env.CELERY_RESULT_BACKEND} --build-arg PGADMIN_DEFAULT_EMAIL=${env.PGADMIN_DEFAULT_EMAIL} --build-arg PGADMIN_DEFAULT_PASSWORD=${env.PGADMIN_DEFAULT_PASSWORD} --build-arg ALLOWED_HOSTS=${env.ALLOWED_HOSTS} .")
                    } catch (Exception e) {
                        echo "Error during Docker image build: ${e.getMessage()}"
                        error("Build failed")
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    def dockerImage = docker.image("${BUILD_TAG}")
                    docker.withRegistry('https://registry.hub.docker.com', DOCKER_CREDENTIALS_ID) {
                        try {
                            dockerImage.push()
                            echo 'Image pushed successfully'
                        } catch (Exception e) {
                            echo "Failed to push image: ${e.getMessage()}"
                        }
                    }
                }
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