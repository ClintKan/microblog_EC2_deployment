**<ins>Note:</ins>**


# <ins>C5 DEPLOYMENT WORKLOAD 3</ins>

   #### _Deployment of a WebApp - using a CI/CD Pipeline & with monitoring_

## <ins> OBJECTIVE</ins>
In this assignment, a WebApp is deployed entirely in AWS- with all source files built in GitHub, tested on a Jenkins server using the multi-branch CI/CD pipeline.
There is a focus on how to execute unit testing, how to execute a CI/CD pipeline with added stages; **_OWASP (a security feature)_**, a **_Clean (to clean out any running services)_** and then 
eventually the deploy stage.


## <ins> SYSTEM DIAGRAM</ins>
<div align="center">
	<img width="752" alt="image" src="https://github.com/user-attachments/assets/83d2e7b9-bda6-41ed-9315-ae42a6302e64">
</div>


## <ins>PROCESS</ins>

1. Application source files was cloned into my GitHub (with a specified repo name - )
2. An AWS t3.micro EC2 for Jenkins was created and the above mentioned repo cloned to the EC2. (_[Jenkins installation file found here](add-link-here)_)  with the following security configurations via port configurations; 22 for SSH, 8080 for Jenkins.
3. CI/CD Pipeline configuration was then done within the Jenkins file as follows (reference it here to follow along):

   **a. Build Stage:**

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
	NGINX was setup as a proxy server that passes web requests to the gunicorn server running at http://127.0.0.1:5000 - the same location hosting the the microblog:app. The response to the request is then sent back to nginx and then to the
	client by nynix proxy. Hence being able to view the webapp on the public ip address of the computer - instead of the local host's IP address; 127.0.0.1



   **b. Test Stage:**

	
   This is the environment/stage where unit testing of the application is done by running the test file; test_app.py.
   

   **c. OWASP FS SCAN Stage:**

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
    <ADD DEPENDENCY CHECK IMAGE HERE>
</div>



   **d. Clean Stage:**

   This is the environment/stage where termination of the running gunicorn app is done, and therefore free up the 5000 port that is to be then re-initiated, in the deploy stage.


   **d. Deploy Stage:**

   In this stage was the commands required to deploy the application so that it is available to the internet.

   


