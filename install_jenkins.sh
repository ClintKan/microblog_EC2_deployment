sudo apt update -y
sudo apt upgrade -y
sudo apt install fontconfig openjdk-17-jre software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt install python3.7 python3.7-venv -y
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]" https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/nul 
sudo apt update -y
sudo apt upgrade -y
sudo apt install jenkins -y
sudo systemctl start jenkins
sudo systemctl status jenkins
