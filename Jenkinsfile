pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'Job Portal'
        BUILD_TAG = "${DOCKER_IMAGE}:${BUILD_NUMBER}"
    }

    stage('Clone Repository') {
        steps {
            script {
                withCredentials([usernamePassword(credentialsId: 'your-credentials-id', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                    git branch: 'restapi', 
                        url: "https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/living-ghost/Job_Portal.git"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build(BUILD_TAG)
                }
            }
        }
        
        stage('Push to Docker Registry') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials-id', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    script {
                        docker.withRegistry('https://hub.docker.com/repository/docker/living9host', 'dockerhub-credentials-id') {
                            docker.image(BUILD_TAG).push()
                        }
                    }
                }
            }
        }

        stage('Deploy Containers') {
            steps {
                script {
                    sh """
                    docker-compose up -d
                    """
                }
            }
        }

        stage('Run Django Migrations') {
            steps {
                script {
                    sh """
                    docker-compose exec django python manage.py migrate
                    """
                }
            }
        }

        stage('Collect Static Files') {
            steps {
                script {
                    sh """
                    docker-compose exec django python manage.py collectstatic --noinput
                    """
                }
            }
        }
    }
}