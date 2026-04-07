pipeline {
    agent any

    environment {
        DOCKER_HUB_ID = 'ankiiiiitt'
        IMAGE_NAME = 'focusvault-app'
        EC2_IP = 'your_ec2_public_ip'
        PATH = "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/ankiiiiiitt/Devops_miniproject.git'
                echo '✅ Code checked out from GitHub!'
            }
        }

        stage('Build Docker Image') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                    sh '/usr/local/bin/docker build -t ${DOCKER_HUB_ID}/${IMAGE_NAME}:latest .'
                    echo '✅ Docker image built!'
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-creds',
                                                      usernameVariable: 'DOCKER_USER',
                                                      passwordVariable: 'DOCKER_PASS')]) {
                        sh '/usr/local/bin/docker login -u $DOCKER_USER -p $DOCKER_PASS'
                        sh '/usr/local/bin/docker push ${DOCKER_HUB_ID}/${IMAGE_NAME}:latest'
                        echo '✅ Pushed to Docker Hub!'
                    }
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                    echo '⚠️ EC2 deploy skipped - configure ec2-ssh-creds to enable.'
                }
            }
        }
    }

    post {
        always {
            echo '🏁 Pipeline finished.'
            cleanWs()
        }
    }
}
