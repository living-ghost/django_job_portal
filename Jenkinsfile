pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials-id'
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

        WKHTMLTOPDF_PATH = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
        WKHTMLTOIMAGE_PATH = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltoimage.exe"
    }

    stages {
        stage('Clone Repository') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'fdc92cdd-ab3a-497c-8976-218341fc7caa', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                        git branch: 'test',
                            url: "https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/living-ghost/Job_Portal.git"
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${BUILD_TAG}", "--build-arg SECRET_KEY=${env.SECRET_KEY} --build-arg DB_NAME=${env.DB_NAME} --build-arg DB_USER=${env.DB_USER} --build-arg DB_PASSWORD=${env.DB_PASSWORD} --build-arg DB_HOST=${env.DB_HOST} --build-arg DB_PORT=${env.DB_PORT} --build-arg CELERY_BROKER_URL=${env.CELERY_BROKER_URL} --build-arg CELERY_ACCEPT_CONTENT=${env.CELERY_ACCEPT_CONTENT} --build-arg CELERY_RESULT_SERIALIZER=${env.CELERY_RESULT_SERIALIZER} --build-arg CELERY_TASK_SERIALIZER=${env.CELERY_TASK_SERIALIZER} --build-arg CELERY_TIMEZONE=${env.CELERY_TIMEZONE} --build-arg CELERY_RESULT_BACKEND=${env.CELERY_RESULT_BACKEND} --build-arg PGADMIN_DEFAULT_EMAIL=${env.PGADMIN_DEFAULT_EMAIL} --build-arg PGADMIN_DEFAULT_PASSWORD=${env.PGADMIN_DEFAULT_PASSWORD} --build-arg DEFAULT_FROM_EMAIL=${env.DEFAULT_FROM_EMAIL} --build-arg EMAIL_HOST_PASSWORD=${env.EMAIL_HOST_PASSWORD} --build-arg ALLOWED_HOSTS=${env.ALLOWED_HOSTS} .")
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

        stage('Deploy Containers') {
            steps {
                script {
                    try {
                        echo "Starting Docker Compose..."
                        set EMAIL_HOST_PASSWORD="${EMAIL_HOST_PASSWORD}"
                        bat 'docker-compose up -d --build'
                        echo "Docker Compose started"

                        // Capture logs for debugging
                        bat 'docker-compose logs'
                    } catch (Exception e) {
                        echo "Docker Compose failed: ${e.getMessage()}"
                        error("Stopping pipeline due to Docker Compose failure.")
                    }
                }
            }
        }

        stage('Run Django Make Migrations') {
            steps {
                bat '''
                    docker-compose exec django python manage.py makemigrations portal_admin_app
                    docker-compose exec django python manage.py makemigrations portal_user_app
                    docker-compose exec django python manage.py makemigrations portal_resume_app
                    docker-compose exec django python manage.py makemigrations portal_converter_app
                '''
            }
        }

        stage('Run Django Migrations') {
            steps {
                bat 'docker-compose exec django python manage.py migrate'
            }
        }

        stage('Collect Static Files') {
            steps {
                bat 'docker-compose exec django python manage.py collectstatic --noinput'
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