pipeline {
    agent any
//     agent {
//         docker {
//             image 'python:3.9'
//             args '-v $HOME:/home/jenkins'
//         }
//     }
    stages {
        stage('build') {
            steps {
                sh 'git checkout dev'
                sh 'git pull'
                sh 'docker build . -t kirrog76/infr_big_data'
//                 sh 'docker login -u $docker_hub_us -p $docker_hub_pw'
//                 sh 'docker push kirrog76/infr_big_data'
//                 withEnv(["HOME=${env.WORKSPACE}"]) {
//                     sh "python -m pip install virtualenv"
//                     sh "python -m virtualenv venv"
//                     sh "python -m pip install -r requirements.txt "
//                 }
            }
        }
        stage('push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker_hub', passwordVariable: 'docker_hub_pw', usernameVariable: 'docker_hub_us')]) {
                    sh "docker login -u ${env.docker_hub_us} -p ${env.docker_hub_pw}"
                    sh 'docker push kirrog76/infr_big_data:v1'
                }
//                 sh 'docker login -u $docker_hub_us -p $docker_hub_pw'
//                 sh 'docker push kirrog76/infr_big_data'
//                 withEnv(["HOME=${env.WORKSPACE}"]) {
//                     sh "python -m pip install virtualenv"
//                     sh "python -m virtualenv venv"
//                     sh "python -m pip install -r requirements.txt "
//                 }
            }
        }
        stage('test') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker_hub', passwordVariable: 'docker_hub_pw', usernameVariable: 'docker_hub_us')]) {
                    sh "docker login -u ${env.docker_hub_us} -p ${env.docker_hub_pw}"
                    sh 'docker pull kirrog76/infr_big_data:v1'
                }
                sh 'docker compose up -d -f docker-compose_jenkins.yml'
                sleep time: 240, unit: 'SECONDS'
                sh 'docker compose exec web-app bash -c "python -m unittest tests.tests"'
//                 sh 'docker login -u $docker_hub_us -p $docker_hub_pw'
//                 sh 'docker pull kirrog76/infr_big_data'
//                 sh 'docker run kirrog76/infr_big_data sh -c "python -m main; python -m unittest tests.tests"'
//                 withEnv(["HOME=${env.WORKSPACE}"]) {
// //                     sh 'python -m main'
//                     sh 'python -m unittest tests.tests'
//                 }
            }
        }
    }
}