# <ins>C5 DEPLOYMENT WORKLOAD 3</ins>


## <ins> OBJECTIVE</ins>

   #### _Deployment of a WebApp - using a CI/CD Pipeline & with monitoring_
   
In this assignment, a WebApp is deployed entirely in AWS - with all source files built in GitHub, tested on a Jenkins server using the multi-branch CI/CD pipeline.
There is a focus on how to execute unit testing, how to execute a CI/CD pipeline with added stages; **_OWASP (a security feature)_**, a **_Clean (to clean out any running services)_** and then 
eventually the deploy stage.


## <ins> SYSTEM DIAGRAM</ins>

<div align="center">
	<img width="965" alt="Workload 3 Sys Diag" src="https://github.com/user-attachments/assets/5eed5497-8cb9-45c3-8115-cd950c6227b6">
</div>

## <ins>PROCESS</ins>


_**Key Pre-requisites to running the pipeline:**_
- A system process file for the app; microblog, has to be created prior to running the pipeline. This is to easily manage the app, like keeping it running when needed (in the Deploy stage) or killing it when needed (in the (Clean stage) by calling upon the process ID (PID).
This is done by executing the command; sudo nano /etc/systemd/system/microblog.service and the below added in the opened file.

		```
		Unit]
		Description=Gunicorn instance to serve microblog
		After=network.target
		
		[Service]
		User=jenkins
		Group=jenkins
		WorkingDirectory=/var/lib/jenkins/workspace/workload_3_main
		Environment="/var/lib/jenkins/workspace/workload_3_main/venv/bin"
		ExecStart=/var/lib/jenkins/workspace/workload_3_main/venv/bin/gunicorn -b :5000 -w 4 microblog:app
		
		[Install]
		WantedBy=multi-user.target
  
		```


- In case of running into an error at the Deploy stage where the error is about the user not having permissions or needed to provide the password of the user to execute, then do the following;
Excecute the command: ```sudo visudo ```. Then append the following in the file

```
jenkins ALL=(ALL) NOPASSWD: /bin/systemctl restart microblog, /bin/systemctl status microblog, /bin/systemctl is-active microblog

```

This will give the Jenkins user permission to restart, check the status, and check the active state of the microblog service using systemctl, without "requiring a password each time" that would 
be needed during the pipeline. This is often done for automation purposes in CI/CD pipelines so Jenkins can manage services without manual intervention.

1. Application source files was cloned into my GitHub (with a specified repo name - without the quotes - "**_microblog_EC2_deployment_**")
2. An AWS t3.medium EC2 for Jenkins was created and the above mentioned repo cloned to the EC2 (_[Jenkins installation file found here](https://github.com/ClintKan/microblog_EC2_deployment/blob/main/Jenkinsfile)_) with the following security configurations via port configurations; 22 for SSH, 8080 for Jenkins.
3. CI/CD Pipeline configuration was then done within the Jenkins file as follows (reference it here to follow along):

   **(a.) Build Stage:**

	While most were to prepare the environment in which the app was to be run, the commands below are the ones that I am highlighting for the reasons to be shared respecitvely;

 	- The command ```export FLASK_APP=microblog.py``` was to assign the environment variable FLASK_APP to be the 'microblog.py' python file. This is to point the flask app to look for the app in micrroblog.py
	Similarly, the above command can instead be entered in the ~/.bashrc file as shown in the image below.



	<div align="center">
		<img width="965" alt="Pasted Graphic 33" src="https://github.com/user-attachments/assets/dcca2b18-c7d0-482d-9ccf-22b1ff6c276b">
	</div>



	- The command ```gunicorn -b :5000 -w 4 microblog:app``` was to launch gunicorn app, a web server graphics interface used to run web apps, while assigning the use of port number 5000, hosting and/or serving
	the app; microblog (a flask app). When running, it appears, in the browser, as the image below.



	<div align="center">
		<img width="1446" alt="Pasted Graphic 35" src="https://github.com/user-attachments/assets/a334f050-8923-4f5c-8c11-14d9dacb83e7">
 	</div>



	- Not shown in this stage is that upon installation of nginx, nginx configuration file located at "**_/etc/nginx/sites-enabled/default_**" had to be edited (with the code below) so as to direct how to; handle web 	requests, route web traffic etc. for the default site on the server.

            ```
                location / {
                proxy_pass http://127.0.0.1:5000;
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                }
            ```

	**_Why update the file as noted above?_**

	NGINX was setup as a proxy server that passes web requests to the gunicorn server running at http://127.0.0.1:5000 - the same location hosting the the microblog:app. The response to the request is then sent back to
	nginx and then to the
	client by nynix proxy. Hence being able to view the webapp on the public ip address of the computer - instead of the local host's IP address; 127.0.0.1



   **(b.) Test Stage:**

	
   This is the environment/stage where unit testing of the application is done by running the test file; test_app.py.
   

   **(c.) OWASP FS SCAN Stage:**

   Using the National Vulnerability Database (NVD) API key, in this stage the app is checked and scanned against standard security protocols. To be specific, this stage is responsible for;

   - Ensuring security integration within the pipeline.
     
   - Catching any security risks that may arise from the bins and libraries.
     
   - Ensuring the web application meets the proper security standard protocols set.
  
            ```
                dependencyCheck additionalArguments: '--scan ./ --disableYarnAudit --disableNodeAudit --nvdApiKey <enter-your-NVDAPI-key>', odcInstallation: 'DP-Check'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'

            ```
     

Additionally, while in the Jenkins GUI via the web browser, OWASP Dependency-Check plugin, used a security feature to scan applications dependencies within the CI/CD pipeline by ensuring that a project is free
from known vulnerabilities, was added. This is critical as it reduces chances of chances of security breaches and meeting compliance requirements. The plug-in can be either triggered as a stage in the pipeline or
even auto-triggered during the build stage.


<div align="center">
    <img width="1461" alt="Pasted Graphic" src="https://github.com/user-attachments/assets/0e166b92-300c-47d2-a7ce-3ebbaa9f0593">

</div>



   **(d.) Clean Stage:**

   This is the environment/stage where termination of the running gunicorn app is done, and therefore free up the 5000 port that is to be then re-initiated, in the deploy stage.


   **(e.) Deploy Stage:**

   In this stage was the commands required to deploy the application so that it is available to the internet.

A successful deployment would look as the image below;

<div align="center">
    <img width="1689" alt="image" src="https://github.com/user-attachments/assets/258f10c5-1abd-4b90-a88e-0c6d25bbebfa">

</div>

4. Monitoring. This was done in a separately created t3.micro EC2, with ports (for); 22 (SSH), 9090 (Prometheus), and 3000 (Grafana) opened within the AWS security group configuration.
5. On the Monitoring EC2, prometheus, grafana were installed using _[this](https://github.com/ClintKan/microblog_EC2_deployment/blob/main/install_prom_graf_node.sh script)_.
6. The prometheus yml file [found here; ``` sudo nano /opt/prometheus/prometheus.yml ```] was updated as follows - so as to scrape the metrics broadcasted by the Jenkins server
replacing the ``` jenkins-ip-address ``` with the real IP address of the Jenkins EC2
	```
 	scrape_configs:
	  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
	  - job_name: "prometheus"
	    static_configs:
	      - targets: ["<jenkins-ip-address>:9090"]
	  - job_name: "node_exporter"
	    static_configs:
	      - targets: ["jenkins-ip-address:9100"]
	  - job_name: "microblog app"
	    static_configs:
	      - targets: ["jenkins-ip-address:4000"]

	```

   
7. Finally, Grafana - accessible at the http://ip-address-of-monitoriing-ec2:3000 in the browser - was configured to have dashboards showing the details of the EC2 being monitored.
In my case, I scraped the CPU usage (the blue line), memory usage (green line), and storage usage (yellow line).  FYI: The blue and yellow line were intertwined as per the image shown.

<div align="center">
	<img width="1138" alt="Pasted Graphic 4" src="https://github.com/user-attachments/assets/e354f721-c232-4c43-a2b1-f7724bafa3f5">
</div>


<div align="center">
	<img width="1004" alt="image" src="https://github.com/user-attachments/assets/ddbe374b-4093-4cf7-b827-c5830dab501a">
</div>




