  class Config:
SECRET_KEY = os.environ.get('SECRET_KEY')  # Remove fallback value
# ...