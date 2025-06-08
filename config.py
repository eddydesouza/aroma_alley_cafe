class Config:
    SECRET_KEY = 'your-secret-key'  # Needs to be replaced with a secure key
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost/aroma_alley_cafe'
    SQLALCHEMY_TRACK_MODIFICATIONS = False