pipeline {
    agent any
    
    parameters {
        string(name: 'DOCKER_TAG', defaultValue: 'latest', description: 'Deployment tag specification')
        booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Perform health-check validations')
    }

    environment {
        REGISTRY_URI = 'your-dockerhub-username' // Change to your actual Docker Hub profile username
        APP_NAME     = 'smart-agri-portal'
        CRED_ID      = 'docker-hub-credentials'
    }

    stages {
        stage('Initialize & Pull') {
            steps {
                echo "Fetching repository head pointers..."
                cleanWs()
                checkout scm
            }
        }

        stage('Parallel Build & Test Matrix') {
            parallel {
                stage('Docker Compile') {
                    steps {
                        sh "docker build -t ${REGISTRY_URI}/${APP_NAME}:${params.DOCKER_TAG} ."
                    }
                }
                stage('Static Code Verification') {
                    when { expression { return params.RUN_TESTS } }
                    steps {
                        echo "Running HTML structural evaluations..."
                        sh "sleep 2" // Mocking testing frame runtime
                    }
                }
            }
        }

        stage('Registry Ship') {
            steps {
                withCredentials([usernamePassword(credentialsId: env.CRED_ID, usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh "echo '${PASS}' | docker login -u '${USER}' --password-stdin"
                    sh "docker push ${REGISTRY_URI}/${APP_NAME}:${params.DOCKER_TAG}"
                }
            }
        }

        stage('Kubernetes Orchestrated Delivery') {
            steps {
                // Relies on configured 'kubernetes-config' credentials inside Jenkins environment
                withKubeConfig([credentialsId: 'kubernetes-config']) {
                    sh "kubectl apply -f deployment.yaml"
                    sh "kubectl set image deployment/smart-agri-deployment smart-agri-container=${REGISTRY_URI}/${APP_NAME}:${params.DOCKER_TAG}"
                    sh "kubectl rollout status deployment/smart-agri-deployment"
                }
            }
        }
    }

    post {
        always {
            echo "Archiving operational assets..."
            archiveArtifacts artifacts: 'index.html', allowEmptyArchive: false
        }
    }
}
