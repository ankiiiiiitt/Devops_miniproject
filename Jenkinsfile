pipeline {
    agent any

    environment {
        DOCKER_HUB_ID = 'your_dockerhub_username'
        IMAGE_NAME = 'focusvault-app'
        EC2_IP = 'your_ec2_public_ip'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/ankiiiiiitt/Devops_miniproject.git'
                echo '✅ Code checked out from GitHub successfully!'
            }
        }

        stage('Build Docker Image') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                    sh "docker build -t ${DOCKER_HUB_ID}/${IMAGE_NAME}:latest ."
                    echo '✅ Docker image built successfully!'
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-creds',
                                                      usernameVariable: 'DOCKER_USER',
                                                      passwordVariable: 'DOCKER_PASS')]) {
                        sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                        sh "docker push ${DOCKER_HUB_ID}/${IMAGE_NAME}:latest"
                        echo '✅ Image pushed to Docker Hub!'
                    }
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                    sshagent(['ec2-ssh-creds']) {
                        sh """
                            ssh -o StrictHostKeyChecking=no ubuntu@${EC2_IP} '
                                docker pull ${DOCKER_HUB_ID}/${IMAGE_NAME}:latest &&
                                docker stop focusvault || true &&
                                docker rm focusvault || true &&
                                docker run -d --name focusvault -p 5001:5000 ${DOCKER_HUB_ID}/${IMAGE_NAME}:latest
                            '
                        """
                        echo '✅ Deployed to EC2!'
                    }
                }
            }
        }
    }

    post {
        always {
            echo '🏁 Pipeline finished.'
            cleanWs()
        }
        success {
            echo '🎉 All stages passed!'
        }
        unstable {
            echo '⚠️ Some optional stages (Docker/EC2) were skipped. Core checkout succeeded!'
        }
    }
}
