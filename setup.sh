RED="\033[0;31m"
GREEN="\033[0;32m"
ENDCOLOR="\033[0m"


echo -e "\n${RED}Deleting old environment${ENDCOLOR}\n"
deactivate
rm -rf venv

echo -e "\n${RED}Creating new virtual environment${ENDCOLOR}\n"
python3 -m pip install virtualenv
python3 -m venv .venv

echo -e "\n${RED}Activating environment and upgrading pip${ENDCOLOR}\n"
source .venv/bin/activate
pip install --upgrade pip

echo -e "\n${RED}Installing packages${ENDCOLOR}\n"
pip install -r requirements.txt

echo -e "\n${GREEN}Installed${ENDCOLOR}\n"