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
                py.test ./tests/unit/test_app.py --verbose --junit-xml test-reports/results.xml
                '''
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
    //   stage ('OWASP FS SCAN') {
    //         steps {
    //             dependencyCheck additionalArguments: '--scan ./ --disableYarnAudit --disableNodeAudit --nvdApiKey 5a3a753b-8edc-43f5-a07f-14f53235a3e9', odcInstallation: 'DP-Check'
    //             dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
    //         }
    //     }
      stage ('Clean') {
            steps {
                sh '''#!/bin/bash
                pid=$(pgrep -f "gunicorn")

                # Check if PID is found and is valid (non-empty)
                if [[ -n "$pid" && "$pid" -gt 0 ]]; then
                    echo "$pid" > pid.txt
                    kill "$pid"
                    echo "Killed gunicorn process with PID $pid"
                else
                    echo "No gunicorn process found to kill"
                fi
                '''
            }
        }
      stage ('Deploy') {
            steps {
                sh '''#!/bin/bash
                # Start Flask application
                source venv/bin/activate

                # Restart the microblog service
                sudo /bin/systemctl restart microblog 

                # Check the status of the service
                if bin/systemctl is-active --quiet microblog; then // sudo /bin/
                    echo "microblog restarted successfully"
                else
                    echo "Failed to restart microblog"
                    # Print logs for debugging
                    /bin/journalctl -u microblog // sudo
                    exit 1
                fi
                '''
            }
        }
    }
}
