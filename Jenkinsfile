pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials-id'
        DOCKER_IMAGE_PREFIX = 'living9host'
        BUILD_TAG = "${env.BUILD_NUMBER}"

        // Docker images
        DJANGO_IMAGE = "${DOCKER_IMAGE_PREFIX}/django:${BUILD_TAG}"
        CELERY_IMAGE = "${DOCKER_IMAGE_PREFIX}/celery:${BUILD_TAG}"
        FLOWER_IMAGE = "${DOCKER_IMAGE_PREFIX}/flower:${BUILD_TAG}"

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

        EMAIL_HOST_USER = 'akhiiltkaniiparampiil@gmail.com'
        DEFAULT_FROM_EMAIL = 'akhiiltkaniiparampiil@gmail.com'
        EMAIL_HOST_PASSWORD = credentials('django-email-password-id')

        WKHTMLTOPDF_PATH = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
        WKHTMLTOIMAGE_PATH = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltoimage.exe"
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

        stage('Build Docker Images') {
            steps {
                script {
                    // Build Docker images for each service
                    docker.build("${DJANGO_IMAGE}", "--build-arg SECRET_KEY=${env.SECRET_KEY} --build-arg DB_NAME=${env.DB_NAME} --build-arg DB_USER=${env.DB_USER} --build-arg DB_PASSWORD=${env.DB_PASSWORD} --build-arg DB_HOST=${env.DB_HOST} --build-arg DB_PORT=${env.DB_PORT} --build-arg CELERY_BROKER_URL=${env.CELERY_BROKER_URL} --build-arg CELERY_ACCEPT_CONTENT=${env.CELERY_ACCEPT_CONTENT} --build-arg CELERY_RESULT_SERIALIZER=${env.CELERY_RESULT_SERIALIZER} --build-arg CELERY_TASK_SERIALIZER=${env.CELERY_TASK_SERIALIZER} --build-arg CELERY_TIMEZONE=${env.CELERY_TIMEZONE} --build-arg CELERY_RESULT_BACKEND=${env.CELERY_RESULT_BACKEND} --build-arg PGADMIN_DEFAULT_EMAIL=${env.PGADMIN_DEFAULT_EMAIL} --build-arg PGADMIN_DEFAULT_PASSWORD=${env.PGADMIN_DEFAULT_PASSWORD} --build-arg ALLOWED_HOSTS=${env.ALLOWED_HOSTS} .")
                    docker.build("${CELERY_IMAGE}", "--build-arg SECRET_KEY=${env.SECRET_KEY} --build-arg CELERY_BROKER_URL=${env.CELERY_BROKER_URL} --build-arg CELERY_ACCEPT_CONTENT=${env.CELERY_ACCEPT_CONTENT} --build-arg CELERY_RESULT_SERIALIZER=${env.CELERY_RESULT_SERIALIZER} --build-arg CELERY_TASK_SERIALIZER=${env.CELERY_TASK_SERIALIZER} --build-arg CELERY_TIMEZONE=${env.CELERY_TIMEZONE} --build-arg CELERY_RESULT_BACKEND=${env.CELERY_RESULT_BACKEND} .")
                    docker.build("${FLOWER_IMAGE}", "--build-arg CELERY_BROKER_URL=${env.CELERY_BROKER_URL} --build-arg CELERY_ACCEPT_CONTENT=${env.CELERY_ACCEPT_CONTENT} --build-arg CELERY_RESULT_SERIALIZER=${env.CELERY_RESULT_SERIALIZER} --build-arg CELERY_TASK_SERIALIZER=${env.CELERY_TASK_SERIALIZER} --build-arg CELERY_TIMEZONE=${env.CELERY_TIMEZONE} --build-arg CELERY_RESULT_BACKEND=${env.CELERY_RESULT_BACKEND} .")
                }
            }
        }

        stage('Push Docker Images') {
            steps {
                script {
                    def registry = 'https://index.docker.io/v1/'
                    docker.withRegistry(registry, DOCKER_CREDENTIALS_ID) {
                        // Push Django image
                        def djangoImage = docker.image("${DJANGO_IMAGE}")
                        try {
                            djangoImage.push()
                            echo 'Django image pushed successfully'
                        } catch (Exception e) {
                            echo "Failed to push Django image: ${e.getMessage()}"
                        }

                        // Push Celery image
                        def celeryImage = docker.image("${CELERY_IMAGE}")
                        try {
                            celeryImage.push()
                            echo 'Celery image pushed successfully'
                        } catch (Exception e) {
                            echo "Failed to push Celery image: ${e.getMessage()}"
                        }

                        // Push Flower image
                        def flowerImage = docker.image("${FLOWER_IMAGE}")
                        try {
                            flowerImage.push()
                            echo 'Flower image pushed successfully'
                        } catch (Exception e) {
                            echo "Failed to push Flower image: ${e.getMessage()}"
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
                        bat 'docker-compose pull'
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