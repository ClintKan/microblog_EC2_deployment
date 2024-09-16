pipeline {
  agent any
    stages {
        stage ('Build') {
            steps {
                sh '''#!/bin/bash
                python3.9 -m venv venv
                source venv/bin/activate
                echo "Installing requirements..."
                pip install -r requirements.txt
                pip install gunicorn pymysql cryptography
                export FLASK_APP=microblog.py
                flask translate compile
                flask db upgrade
                '''
            }
        }
        stage ('Test') {
            steps {
                sh '''#!/bin/bash
                source venv/bin/activate
                pytest --junit-xml test-reports/results.xml ./tests/unit/ // --verbose
                '''
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
        // stage('Testing Status Code') {
        //     steps {
        //         echo "Testing Status Code"
        //         script {     
        //             echo "Test Application Status Code == 200"       
        //             statuscode = sh (script: "curl -LI 'http://18.188.200.134' -o /dev/null -w '%{http_code}' -s",returnStdout: true)
        //             echo "${statuscode}"
        //             if ( "${statuscode}" == "200" ){
        //             echo "Application is live!!!"
        //             } else {
        //             error("Application is Down")
        //             }
        //         }
        //     }
        // }
      stage ('OWASP FS SCAN') {
            steps {
                dependencyCheck additionalArguments: '--scan ./ --disableYarnAudit --disableNodeAudit', odcInstallation: 'DP-Check'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }
      stage ('Clean') {
            steps {
                sh '''#!/bin/bash
                if [[ $(ps aux | grep -i "gunicorn" | tr -s " " | head -n 1 | cut -d " " -f 2) != 0 ]]
                then
                ps aux | grep -i "gunicorn" | tr -s " " | head -n 1 | cut -d " " -f 2 > pid.txt
                kill $(cat pid.txt)
                exit 0
                fi
                deactivate
                '''
            }
        }
      stage ('Deploy') {
            steps {
                sh '''#!/bin/bash
                source venv/bin/activate
                gunicorn -b :5000 -w 4 microblog:app
                '''
            }
        }
    }
}
 
