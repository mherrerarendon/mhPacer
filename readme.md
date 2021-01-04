# Welcome to mhPacer!
<img alt="GitHub branch checks state" src="https://img.shields.io/github/checks-status/mherrerarendon/mhpacer/master?label=tests"><br/>
<img src="https://img.shields.io/codecov/c/github/mherrerarendon/mhpacer"><br/>
This is a Flask sample project that demonstrates how to implement speed language parsing (e.g. "10 miles per hour" or "10mph", etc) using regexes, as well as speed math (e.g. How much time would it take to travel 100 meters going at a speed of 7 miles per hour?).

## Virtual environment setup
```
# Run the following commands in the repository directory

# Create virtual environment
python3 -m venv venv

# Activate virtual environment (win)
venv\Scripts\activate.bat

# Activate virtual environment (mac)
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```
## Give it a try!
In a terminal with the virtual environment activated, cd to root directory of this repository and enter `python start_server.py`. Using a browser, navigate to the link specified in the terminal output, and test out different speed and distance combinations!

## Run unit tests
In a terminal with the virtual environment activated, cd to root directory of the repository, and enter `pytest`
