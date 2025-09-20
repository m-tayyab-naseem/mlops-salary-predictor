pipeline {
    agent any
    
    environment {
        // Docker Hub credentials - configure these in Jenkins credentials store
        DOCKER_HUB_CREDENTIALS = credentials('docker-hub-credentials')
        DOCKER_IMAGE_NAME = 'taayabbb/salary-prediction-app'
        DOCKER_IMAGE_TAG = "${env.BUILD_NUMBER}"
        DOCKER_REGISTRY = 'docker.io'
        
        // Email configuration - configure these in Jenkins system configuration
        EMAIL_RECIPIENTS = 'your-email@example.com'
        EMAIL_SUBJECT = 'MLOps Salary Prediction App - Build Success'
    }
    
    triggers {
        // Trigger on push to master branch
        githubPush()
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from repository...'
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    // Build the Docker image
                    def image = docker.build("${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}")
                    
                    // Also tag as latest
                    sh "docker tag ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} ${DOCKER_IMAGE_NAME}:latest"
                    
                    // Store image reference for later use
                    env.DOCKER_IMAGE_ID = image.id
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing Docker image to Docker Hub...'
                script {
                    // Login to Docker Hub
                    sh "echo ${DOCKER_HUB_CREDENTIALS_PSW} | docker login ${DOCKER_REGISTRY} -u ${DOCKER_HUB_CREDENTIALS_USR} --password-stdin"
                    
                    // Push both tagged versions
                    sh "docker push ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
                    sh "docker push ${DOCKER_IMAGE_NAME}:latest"
                    
                    echo "Successfully pushed ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} and ${DOCKER_IMAGE_NAME}:latest to Docker Hub"
                }
            }
        }
        
        stage('Cleanup') {
            steps {
                echo 'Cleaning up local Docker images...'
                script {
                    // Remove local images to save space
                    sh "docker rmi ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} || true"
                    sh "docker rmi ${DOCKER_IMAGE_NAME}:latest || true"
                }
            }
        }
    }
    
    post {
        success {
            echo 'Build completed successfully!'
            script {
                // Send success notification email
                emailext (
                    subject: "${EMAIL_SUBJECT} - Build #${env.BUILD_NUMBER}",
                    body: """
                    <h2>Build Success Notification</h2>
                    <p><strong>Project:</strong> MLOps Salary Prediction App</p>
                    <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                    <p><strong>Branch:</strong> ${env.BRANCH_NAME}</p>
                    <p><strong>Commit:</strong> ${env.GIT_COMMIT}</p>
                    <p><strong>Docker Image:</strong> ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}</p>
                    <p><strong>Build URL:</strong> ${env.BUILD_URL}</p>
                    <p><strong>Status:</strong> <span style="color: green;">SUCCESS</span></p>
                    <br>
                    <p>The Docker image has been successfully built and pushed to Docker Hub.</p>
                    <p>You can pull the image using:</p>
                    <code>docker pull ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}</code>
                    """,
                    to: "${EMAIL_RECIPIENTS}",
                    mimeType: 'text/html'
                )
            }
        }
        
        failure {
            echo 'Build failed!'
            script {
                // Send failure notification email
                emailext (
                    subject: "MLOps Salary Prediction App - Build Failed - Build #${env.BUILD_NUMBER}",
                    body: """
                    <h2>Build Failure Notification</h2>
                    <p><strong>Project:</strong> MLOps Salary Prediction App</p>
                    <p><strong>Build Number:</strong> ${env.BUILD_NUMBER}</p>
                    <p><strong>Branch:</strong> ${env.BRANCH_NAME}</p>
                    <p><strong>Commit:</strong> ${env.GIT_COMMIT}</p>
                    <p><strong>Build URL:</strong> ${env.BUILD_URL}</p>
                    <p><strong>Status:</strong> <span style="color: red;">FAILED</span></p>
                    <br>
                    <p>Please check the build logs for more details.</p>
                    """,
                    to: "${EMAIL_RECIPIENTS}",
                    mimeType: 'text/html'
                )
            }
        }
        
        always {
            echo 'Build process completed.'
            // Clean up workspace if needed
            cleanWs()
        }
    }
}
