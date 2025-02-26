# AIAnalysisApp
Python app that can be monitored with Dynatrace and brings potential issues further analysed with AI

# git clone https://github.com/ManojKamatam/AIAnalysisApp.git

# On EC2

# Install dependencies
sudo apt-get update
sudo apt-get install python3-pip redis-server

# Clone your repository
git clone <your-repo-url>
cd sample-app

# Install Python dependencies
pip3 install -r requirements.txt

# Initialize the database
python3 init_db.py

# Start the application
python3 run.py

# Github token PAT
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

# Install packages and make zip file
mkdir lambda_package
cd lambda_package 
python -m pip install PyGithub -t . --no-user
Create lambda_function.py as well
powershell Compress-Archive -Path * -DestinationPath ..\lambda_function.zip -Force

This will create a ZIP file outside lambda_package in the main folder.
