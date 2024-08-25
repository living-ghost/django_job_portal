pipeline {
    agent any
    
    environment {
        // Define environment variables
        DOCKER_IMAGE = 'your-docker-image-name'
        DOCKER_REGISTRY = 'your-docker-registry-url'
        DOCKER_CREDENTIALS_ID = 'docker-credentials-id'
        BUILD_TAG = "${DOCKER_IMAGE}:${BUILD_NUMBER}"
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Clone the Git repository
                git branch: 'main', url: 'https://github.com/your-repository-url.git'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                // Build the Docker image with the unique build tag
                script {
                    docker.build(BUILD_TAG)
                }
            }
        }
        
        stage('Push to Docker Registry') {
            steps {
                script {
                    // Log in to Docker registry and push the image
                    docker.withRegistry("https://${DOCKER_REGISTRY}", DOCKER_CREDENTIALS_ID) {
                        docker.image(BUILD_TAG).push()
                    }
                }
            }
        }
        
        stage('Deploy Containers') {
            steps {
                script {
                    // Start Docker containers without stopping existing ones
                    sh """
                    docker-compose up -d
                    """
                }
            }
        }

        stage('Run Django Migrations') {
            steps {
                script {
                    // Run Django migrations inside the Django container
                    sh """
                    docker-compose exec django python manage.py migrate
                    """
                }
            }
        }
        
        stage('Collect Static Files') {
            steps {
                script {
                    // Collect static files inside the Django container
                    sh """
                    docker-compose exec django python manage.py collectstatic --noinput
                    """
                }
            }
        }
    }

    post {
        always {
            // Optionally clean up other resources or perform additional steps
        }
    }
}