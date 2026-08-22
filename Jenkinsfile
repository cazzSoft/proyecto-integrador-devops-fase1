pipeline {
    agent any

    triggers {
        githubPush()
    }

    options {
        timestamps()
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '15'))
    }

    environment {
        BACKEND_REPOSITORY = 'gestion-usuarios-backend'
        FRONTEND_REPOSITORY = 'gestion-usuarios-frontend'
    }

    stages {
        stage('1. Preparacion / Checkout') {
            steps {
                script {
                    def scmVars = checkout scm
                    env.SCM_BRANCH = scmVars.GIT_BRANCH ?: 'unknown'
                    env.GIT_FULL = scmVars.GIT_COMMIT ?: sh(
                        script: 'git rev-parse HEAD',
                        returnStdout: true
                    ).trim()
                    env.GIT_SHORT = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                    env.VERSION_TAG = "fase3-${env.BUILD_NUMBER}-${env.GIT_SHORT}"
                    currentBuild.description = "${env.VERSION_TAG} | ${env.SCM_BRANCH}"

                    echo "Rama: ${env.SCM_BRANCH}"
                    echo "Commit: ${env.GIT_FULL}"
                    echo "Version: ${env.VERSION_TAG}"
                }

                sh '''
                    set -eu
                    mkdir -p reports
                    cat > reports/build-metadata.txt <<EOF
JOB_NAME=${JOB_NAME}
BUILD_NUMBER=${BUILD_NUMBER}
BUILD_URL=${BUILD_URL}
SCM_BRANCH=${SCM_BRANCH}
GIT_FULL=${GIT_FULL}
GIT_SHORT=${GIT_SHORT}
VERSION_TAG=${VERSION_TAG}
EOF
                '''
            }
        }

        stage('2. Dependencias / Build') {
            parallel {
                stage('Backend') {
                    steps {
                        dir('backend') {
                            sh 'npm ci'
                            sh 'npx prisma generate'
                            sh 'npm run build'
                        }
                    }
                }

                stage('Frontend') {
                    steps {
                        dir('frontend') {
                            sh 'npm ci'
                            sh 'npm run build'
                        }
                    }
                }
            }
        }

        stage('3. Pruebas') {
            parallel {
                stage('Backend - Pruebas') {
                    steps {
                        dir('backend') {
                            sh 'npm test'
                        }
                    }
                }

                stage('Frontend - Analisis') {
                    steps {
                        dir('frontend') {
                            sh 'npm run lint'
                        }
                    }
                }
            }
        }

        stage('4. Observabilidad / Prometheus') {
            steps {
                sh '''
                    set -eu
                    test -f observability/prometheus.yml
                    test -f observability/grafana/dashboards/observabilidad-proyecto-integrador.json

                    docker run --rm \
                        -v "$WORKSPACE/observability/prometheus.yml:/etc/prometheus/prometheus.yml:ro" \
                        --entrypoint /bin/promtool \
                        prom/prometheus:latest \
                        check config /etc/prometheus/prometheus.yml

                    echo 'Configuracion de Prometheus valida.'
                '''
            }
        }
        stage('5. Construccion') {
            steps {
                sh '''
                    set -eu
                    BACKEND_LOCAL="gestion-usuarios-backend:${VERSION_TAG}"
                    FRONTEND_LOCAL="gestion-usuarios-frontend:${VERSION_TAG}"

                    docker version
                    docker build --pull -t "$BACKEND_LOCAL" ./backend
                    docker build --pull -t "$FRONTEND_LOCAL" ./frontend

                    docker image inspect "$BACKEND_LOCAL" > reports/backend-image-inspect.json
                    docker image inspect "$FRONTEND_LOCAL" > reports/frontend-image-inspect.json
                    docker image ls --format '{{.Repository}}:{{.Tag}} {{.ID}} {{.Size}}' \
                        > reports/docker-images.txt
                '''
            }
        }

        stage('6. Publicacion') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-cazzsoft',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_TOKEN'
                )]) {
                    sh '''
                        set -eu
                        export DOCKER_CONFIG="$(mktemp -d)"
                        trap 'rm -rf "$DOCKER_CONFIG"' EXIT

                        echo "$DOCKER_TOKEN" | docker login \
                            --username "$DOCKER_USER" --password-stdin

                        BACKEND_LOCAL="gestion-usuarios-backend:${VERSION_TAG}"
                        FRONTEND_LOCAL="gestion-usuarios-frontend:${VERSION_TAG}"
                        BACKEND_REMOTE="$DOCKER_USER/$BACKEND_REPOSITORY:${VERSION_TAG}"
                        FRONTEND_REMOTE="$DOCKER_USER/$FRONTEND_REPOSITORY:${VERSION_TAG}"

                        docker tag "$BACKEND_LOCAL" "$BACKEND_REMOTE"
                        docker tag "$FRONTEND_LOCAL" "$FRONTEND_REMOTE"
                        docker push "$BACKEND_REMOTE"
                        docker push "$FRONTEND_REMOTE"

                        cat > reports/publication-metadata.txt <<EOF
BACKEND_IMAGE=${BACKEND_REMOTE}
FRONTEND_IMAGE=${FRONTEND_REMOTE}
BUILD_NUMBER=${BUILD_NUMBER}
GIT_SHORT=${GIT_SHORT}
EOF

                        docker logout >/dev/null 2>&1 || true
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline Fase 3 satisfactorio: ${env.VERSION_TAG}"
        }
        failure {
            echo 'Pipeline Fase 3 fallido: revisar la primera etapa y el primer error relevante.'
        }
        always {
            sh 'docker logout >/dev/null 2>&1 || true'
            archiveArtifacts(
                artifacts: 'reports/**, frontend/dist/**',
                allowEmptyArchive: true,
                fingerprint: true
            )
        }
    }
}
