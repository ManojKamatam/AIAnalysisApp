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

