echo "This is a script to install Python3.9, Python3-pip and nginx"

echo "Do you want to proceed? Yes/No"
read usr_input

usr_input=${usr_input,,}

if [ $usr_input == "yes" ]; then
    echo "Checking for updates first...."
    echo "  "
    sudo apt update
    echo "  "

    echo "Installing Python3.9...."
    echo "  "
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt install python3.9
    echo " "

    echo "Installing Python3.9-venv...."
    echo " "
    sudo apt install python3.9-venv
    echo " "

    echo "Installing Python3-pip...."
    echo "  "
    sudo apt install python3-pip
    echo " "

    echo "Installing 'nginx'...."
    echo "  "
    sudo apt install nginx
    echo " "

    echo "use the commands below to check the version of what's been installed"
    echo "For Python3.9 #python3.9 --version"
    echo "For Python-Pip3 #pip3 --version"
    echo "For nginx #nginx -v"
elif [ $usr_input == "no" ]; then
    echo "Aborting..."
else
    echo "Wrong input. Try again with yes or no."
fi
