# C5 DEPLOYMENT WORKLOAD 3


---



## Deployment of a WebApp - using a CI/CD Pipeline & with monitoring.


## <ins> OBJECTIVE</ins>
In this assignment, entirely in AWS, a WebApp is deployed - with all source files 
built in GitHub, tested on a Jenkins server using the multi-branch CI/CD pipeline.

In this workload we focus on how to execute unit testing, how to execute a CI/CD pipeline with added stages; OWASP (a security feature), a Clean (to clean out any running services)
 in Workload #1, we had to manually upload a zipped file - as downloaded from GitHub repo, in this assignment we use the AWS' EC2 the command line interface of AWS to launch the app. This brings about more effeciency and automation capabilities, reduction in human errors. With that said, this might also make it a bid harder to troubleshoot in case of a error.

## <ins> SYSTEM DIAGRAM</ins>
<div align="center">

</div>


## <ins>PROCESS</ins>

1. Application source files was cloned into my GitHub (with a specified repo name - )
2. An AWS t3.micro EC2 for Jenkins was created and the above mentioned repo cloned to the EC2. (_[Jenkins installation file found here](add-link-here)_)  with the following security configurations via port configurations; 22 for SSH, 8080 for Jenkins.
3. CI/CD Pipeline configuration was then done within the Jenkins file as follows (reference it here to follow along):
    
  a). Build Stage: were all of the commands required to prepare the environment for the application.
  	- The command 'export FLASK_APP=microblog.py' was to assign the environment variable FLASK_APP to be the 'microblog.py' python file. This is to.......
   	- Not mentioned here is that upon installation of nginx, nginx configuration file located at "/etc/nginx/sites-enabled/default" had to be edited (with the code below) so as to direct how to; handle web requests,
    	  route web traffic etc. for the default site on the server.

            ```
                location / {
                proxy_pass http://127.0.0.1:5000;
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                }
            ```

**<ins>WHY?</ins>**

NGINX was setup as a proxy server that passes web requests to the gunicorn server running at http://127.0.0.1:5000 - the same location hosting the the microblog:app. The response to the request is then sent back to nginx and then to the client by nynix proxy. Hence being able to view the webapp on the public ip address of the computer - instead of the local host's IP address; 127.0.0.1

   	- The command 'gunicorn -b :5000 -w 4 microblog:app' was to launch gunicorn app, a web server graphics interface used to run web apps, while assigning the use of port number 5000, hosting and/or serving the app; microblog (a flask app).


b). Test Stage: This is the environment/stage where unit testing of the application is done by running the test file; test_app.py.

c). OWASP FS SCAN: This is the environment/stage where the app is checked and scanned against standard security protocols. To be specific, this stage is responsible for
    - Ensuring security integration within the pipeline.
    - Catching any security risks that may arise from the bins and libraries.
    - Ensuring the web application meets the proper security standard protocols set.
Additionally, while in the Jenkins GUI via the web browser, OWASP Dependency-Check plugin, used a security feature to scan applications dependencies within the CI/CD pipeline by ensuring that a project is free from known vulnerabilities, was added. This is critical as it reduces chances of chances of security breaches and meeting compliance requirements. The plug-in can be either triggered as a stage in the pipeline or even auto-triggered during the build stage.


    <ADD DEPENDENCY CHECK IMAGE HERE>


d). Clean Stage: This is the environment/stage where termination of the running gunicorn app is done, and therefore free up the 5000 port that is to be then re-initiated, in the deploy stage.

e). Deploy stage: Here the commands required to deploy the application so that it is available to the internet.


**<ins>Note:</ins>**



2. Jenkins was installed installed on the EC2 using the script named "_install_jenkins.sh_"


## Instructions

1. Clone this repo to your GitHub account. IMPORTANT: Make sure that the repository name is "microblog_EC2_deployment"

2. Create an Ubuntu EC2 instance (t3.micro) named "Jenkins" and install Jenkins onto it (are you still doing this manually?).  Be sure to configure the security group to allow for SSH and HTTP traffic in addition to the ports required for Jenkins and any other services needed (Security Groups can always be modified afterward)

3. Configure the server by installing 'python3.9',  'python3.9-venv', 'python3-pip', and 'nginx'. (Hint: There are several ways to install a previous python version. One method was used in Workloads 1 and 2)

4. Clone your GH repository to the server, cd into the directory, create and activate a python virtual environment with: 

```
$python3.9 -m venv venv
$source venv/bin/activate
```

5. While in the python virtual environment, install the application dependencies and other packages by running:

```
$pip install -r requirements.txt
$pip install gunicorn pymysql cryptography
```

6. Set the ENVIRONMENTAL Variable:

```
FLASK_APP=microblog.py
```
Question: What is this command doing?

7. Run the following commands: 

```
$flask translate compile
$flask db upgrade
```

8. Edit the NginX configuration file at "/etc/nginx/sites-enabled/default" so that "location" reads as below.

Question: What is this config file/NginX responsible for?

9. Run the following command and then put the servers public IP address into the browser address bar

```
gunicorn -b :5000 -w 4 microblog:app
```
Question: What is this command doing? You should be able to see the application running in the browser but what is happening "behind the scenes" when the IP address is put into the browser address bar?

10. If all of the above works, stop the application by pressing ctrl+c.  Now it's time to automate the pipeline.  Modify the Jenkinsfile and fill in the commands for the build and deploy stages.

  a. The build stage should include all of the commands required to prepare the environment for the application.  This includes creating the virtual environment and installing all the dependencies, setting variables, and setting up the databases.

  b. The test stage will run pytest.  Create a python script called test_app.py to run a unit test of the application source code. IMPORTANT: Put the script in a directory called "tests/unit/" of the GitHub repository. Note: The complexity of the script is up to you.  Work within your limits.  (Hint: If you don't know where to start, try testing the homepage or log in page.  Want to challenge yourself with something more complicated? Sky's the limit!)

  c. The deploy stage will run the commands required to deploy the application so that it is available to the internet. 

  d. There is also a 'clean' and an 'WASP FS SCAN' stage.  What are these for?
  
11. In Jenkins, install the "OWASP Dependency-Check" plug-in

    a. Navigate to "Manage Jenkins" > "Plugins" > "Available plugins" > Search and install

 	b. Then configure it by navigating to "Manage Jenkins" > "Tools" > "Add Dependency-Check > Name: "DP-Check" > check "install automatically" > Add Installer: "Install from github.com"

Question: What is this plugin for?  What is it doing?  When does it do it?  Why is it important?

12. Create a MultiBranch Pipeline and run the build.  IMPORTANT: Make sure the name of the pipeline is: "workload_3".

    Note: Did the pipeline complete? Is the application running?

    Hint: if the pipeline stage is unable to complete because the process is running, perhaps the process should be run in the BACKGROUND (daemon).
    
    Hint pt 2: NOW does the pipeline complete? Is the application running?  If not: What happened to that RUNNING PROCESS after the deploy STAGE COMPLETES? (stayAlive)

14. After the application has successfully deployed, create another EC2 (t3.micro) called "Monitoring".  Install Prometheus and Grafana and configure it to monitor the activity on the server running the application. 

15. Document! All projects have documentation so that others can read and understand what was done and how it was done. Create a README.md file in your repository that describes:

	  a. The "PURPOSE" of the Workload,

  	b. The "STEPS" taken (and why each was necessary/important),
      Question: Were steps 4-9 absolutely necessary for the CICD pipeline? Why or why not?
    
  	c. A "SYSTEM DESIGN DIAGRAM" that is created in draw.io (IMPORTANT: Save the diagram as "Diagram.jpg" and upload it to the root directory of the GitHub repo.),

	  d. "ISSUES/TROUBLESHOOTING" that may have occured,

  	e. An "OPTIMIZATION" section for that answers the question: What are the advantages of provisioning ones own resources over using a managed service like Elastic Beanstalk?  Could the infrastructure created in this workload be considered that of a "good system"?  Why or why not?  How would you optimize this infrastructure to address these issues?

    f. A "CONCLUSION" statement as well as any other sections you feel like you want to include.
