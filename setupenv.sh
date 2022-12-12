# install python3 and pip3
sudo apt update
sudo apt upgrade
sudo apt install python3
sudo apt install python3-pip

# install virtualenv
pip3 install virtualenv

# install and create a virtual environment in your target folder
python3 -m venv myenv

# now activate your venv and install pycryptodome
source myenv/bin/activate

# install dependencies
pip3 install -r server/requirements.txt
pip3 install -r client/requirements.txt

# create dirs
mkdir datasets