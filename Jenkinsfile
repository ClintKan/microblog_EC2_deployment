pipeline {
  agent any
    stages {
        stage ('Build') {
            steps {
                sh '''#!/bin/bash
                pwd
                sudo apt install python3.9 -y # this would be uncommented if not done initially
                sudo apt install python3.9-venv -y # this would be uncommented if not done initially
                sudo apt install python3-pip -y # this would be uncommented if not done initially
                # sudo apt install nginx -y
                echo "Starting virtual environment...."
                ls -al
                // python3.9 -m venv venv
                // source venv/bin/activate
                // echo "Installing requirements..."
                // pip install -r requirements.txt
                // pip install flask
                // sudo apt-get install python3-flask -y
                // pip install gunicorn pymysql cryptography
                // echo 'export FLASK_APP=microblog.py' >> ~/.bashrc
                // flask translate compile
                // flask db upgrade
                '''
            }
        }
        // stage ('Test') {
        //     steps {
        //         sh '''#!/bin/bash
        //         gunicorn -b :5000 -w 4 microblog:app
        //         py.test ./tests/unit/test_app.py --verbose --junit-xml test-reports/results.xml
        //         '''
        //     }
        //     post {
        //         always {
        //             junit 'test-reports/results.xml'
        //         }
        //     }
        // }
        stage('Testing Status Code') {
            steps {
                echo "Testing Status Code"
                script {     
                    echo "Test Application Status Code == 200"       
                    statuscode = sh (script: "curl -s -o /dev/null -w \"%{http_code}\" 'http://3.20.235.84:8080'",returnStdout: true)
                    echo "${statuscode}"
                    if ( "${statuscode}" == "200" ){
                    echo "Application is Live!!!"
                    } else {
                    error("Application is Down")
                    }
                }
            }
        }
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
 
