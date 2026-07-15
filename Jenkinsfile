pipeline {
    agent any
    
    environment {
        AWS_ACCOUNT_ID     = '5685-2925-2779' 
        AWS_DEFAULT_REGION = 'eu-north-1'
        CLUSTER_NAME       = 'flask-eks-cluster'
        
        IMAGE_REPO_NAME    = 'flask-app-repo'
        AWS_CRED_ID        = 'aws-credentials-id' 
        
        IMAGE_TAG          = "${BUILD_NUMBER}"
        REPOSITORY_URI     = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${IMAGE_REPO_NAME}" 
    }
    
    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Flask App Docker image..."
                    // Fixing potential typo string replacement inline during build if needed, 
                    // but best to fix the double underscores directly in your app.py file!
                    sh "docker build -t ${REPOSITORY_URI}:${IMAGE_TAG} ."
                    sh "docker tag ${REPOSITORY_URI}:${IMAGE_TAG} ${REPOSITORY_URI}:latest"
                }
            }
        }
        
        stage('Push to Amazon ECR') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${AWS_CRED_ID}", usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    script {
                        echo "Logging into Amazon ECR..."
                        sh "aws ecr get-login-password --region ${AWS_DEFAULT_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com"
                        
                        echo "Pushing image..."
                        sh "docker push ${REPOSITORY_URI}:${IMAGE_TAG}"
                        sh "docker push ${REPOSITORY_URI}:latest"
                    }
                }
            }
        }
        
        stage('Deploy to EKS') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${AWS_CRED_ID}", usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    script {
                        echo "Connecting to EKS Cluster..."
                        sh "aws eks update-kubeconfig --region ${AWS_DEFAULT_REGION} --name ${CLUSTER_NAME}"
                        
                        echo "Applying/Updating Kubernetes manifest..."
                        // Dynamically update the placeholder image in the manifest file before applying it
                        sh "sed -i 's|REPLACE_WITH_YOUR_ECR_URI|${REPOSITORY_URI}|g' k8s-deployment.yaml"
                        sh "kubectl apply -f k8s-deployment.yaml"
                        
                        echo "Force updating the container to the new build tag..."
                        sh "kubectl set image deployment/flask-app-deployment flask-app-container=${REPOSITORY_URI}:${IMAGE_TAG}"
                        
                        echo "Verifying deployment status..."
                        sh "kubectl rollout status deployment/flask-app-deployment"
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo "Cleaning up local images..."
            sh "docker rmi ${REPOSITORY_URI}:${IMAGE_TAG} ${REPOSITORY_URI}:latest || true"
        }
    }
}
