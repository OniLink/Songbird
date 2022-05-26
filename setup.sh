if [ -d "./venv" ]
then
    echo "virtual environment exists";
    source ./venv/bin/activate;
    echo "checking that dependencies are present";
    pip install -r requirements.txt;
else
    echo "virtual environment does not exist...running initial setup";
    python3 -m venv ./venv;
    source ./venv/bin/activate;
    pip install -r requirements.txt;
fi

echo
echo "Can now run gui.py with the command \"python gui.py\"";
