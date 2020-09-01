import os

class BaseConfig:
  """Base configuration"""
  TESTING = False
  SECRET_KEY = os.environ.get('SECRET_KEY')

class DevelopmentConfig(BaseConfig):
  """Development configuration"""
  DEBUG_TB_ENABLED = True

class TestConfig(BaseConfig):
  """Testing configuration"""
  TESTING = True
  PRESERVE_CONTEXT_ON_EXCEPTION = False

class ProductionConfig(BaseConfig):
  """Production configuration"""  

class StageConfig(BaseConfig):
  """Development configuration"""
