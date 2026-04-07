pipeline {
    agent any

    environment {
        DOCKER_HUB_ID = 'your_dockerhub_username'
        IMAGE_NAME = 'focusvault-app'
        REGISTRY_USER_CREDENTIALS_ID = 'docker-hub-creds'
        SSH_CREDENTIALS_ID = 'ec2-ssh-creds'
        EC2_IP = 'your_ec2_public_ip'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/yourusername/Devops_Project.git'
            }
        }

        stage('Build Image') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_HUB_ID}/${IMAGE_NAME}:${env.BUILD_ID}")
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('', REGISTRY_USER_CREDENTIALS_ID) {
                        dockerImage.push("${env.BUILD_ID}")
                        dockerImage.push("latest")
                    }
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent([SSH_CREDENTIALS_ID]) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ubuntu@${EC2_IP} '
                            docker pull ${DOCKER_HUB_ID}/${IMAGE_NAME}:latest
                            docker stop focusvault-web || true
                            docker rm focusvault-web || true
                            docker run -d --name focusvault-web -p 5001:5000 \
                                -e MONGO_URI=mongodb://mongodb:27017/ai_sem_project \
                                ${DOCKER_HUB_ID}/${IMAGE_NAME}:latest
                        '
                    """
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
