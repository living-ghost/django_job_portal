pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS_ID = 'jenkins-docker-integration'
        DOCKER_IMAGE = 'living9host/job_portal'
        BUILD_TAG = "${DOCKER_IMAGE}:${BUILD_NUMBER}"
    }

    stages {
        stage('Clone Repository') {
            steps {
                script {
                    withCredentials([ 
                        usernamePassword( 
                            credentialsId: 'github-jenkins-integrations', 
                            usernameVariable: 'GIT_USERNAME', 
                            passwordVariable: 'GIT_PASSWORD' 
                        )
                    ]) {
                        git branch: 'master', 
                            url: "https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/living-ghost/django-job-portal.git"
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    withCredentials([ 
                        string(credentialsId: 'SECRET_KEY', variable: 'SECRET_KEY'), 
                        string(credentialsId: 'DB_NAME', variable: 'DB_NAME'), 
                        string(credentialsId: 'DB_USER', variable: 'DB_USER'), 
                        string(credentialsId: 'DB_PASSWORD', variable: 'DB_PASSWORD'), 
                        string(credentialsId: 'DB_HOST', variable: 'DB_HOST'), 
                        string(credentialsId: 'DB_PORT', variable: 'DB_PORT'), 
                        string(credentialsId: 'PGADMIN_DEFAULT_EMAIL', variable: 'PGADMIN_DEFAULT_EMAIL'), 
                        string(credentialsId: 'PGADMIN_DEFAULT_PASSWORD', variable: 'PGADMIN_DEFAULT_PASSWORD'),
                    ]) {
                        if (isUnix()) {
                            // If it's a Unix-like system (Linux/Mac), use 'sh' instead of 'bat'
                            sh """
                            docker build \\
                                --build-arg SECRET_KEY=\$SECRET_KEY \\
                                --build-arg DB_NAME=\$DB_NAME \\
                                --build-arg DB_USER=\$DB_USER \\
                                --build-arg DB_PASSWORD=\$DB_PASSWORD \\
                                --build-arg DB_HOST=\$DB_HOST \\
                                --build-arg DB_PORT=\$DB_PORT \\
                                --build-arg PGADMIN_DEFAULT_EMAIL=\$PGADMIN_DEFAULT_EMAIL \\
                                --build-arg PGADMIN_DEFAULT_PASSWORD=\$PGADMIN_DEFAULT_PASSWORD \\
                                -t \$BUILD_TAG .
                            """
                        } else {
                            // If it's a Windows system, use 'bat' commands
                            bat """
                            docker build ^
                                --build-arg SECRET_KEY=%SECRET_KEY% ^
                                --build-arg DB_NAME=%DB_NAME% ^
                                --build-arg DB_USER=%DB_USER% ^
                                --build-arg DB_PASSWORD=%DB_PASSWORD% ^
                                --build-arg DB_HOST=%DB_HOST% ^
                                --build-arg DB_PORT=%DB_PORT% ^
                                --build-arg PGADMIN_DEFAULT_EMAIL=%PGADMIN_DEFAULT_EMAIL% ^
                                --build-arg PGADMIN_DEFAULT_PASSWORD=%PGADMIN_DEFAULT_PASSWORD% ^
                                -t %BUILD_TAG% .
                            """
                        }
                    }
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', DOCKER_CREDENTIALS_ID) {
                        if (isUnix()) {
                            // On Unix systems, use 'sh' to push the image
                            sh "docker push \$BUILD_TAG"
                        } else {
                            // On Windows systems, use 'bat' to push the image
                            bat "docker push %BUILD_TAG%"
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
