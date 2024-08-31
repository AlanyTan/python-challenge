"""The configuration module, set system wide configure centrally here

Using pydantic to pull EnVar values into the BaseSettings object.

Usage:
    from config import config
    setting_needed = config.USER_SUBMISSION_DIR
"""
from pydantic import ValidationError, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    >>> os.environ['USER_SUBMISSION_DIR'] = 'tmp1'
    >>> os.environ['CHALLENGE_DIR'] = 'tmp2'
    >>> config = Settings()
    >>> config.USER_SUBMISSION_DIR
    'tmp1'
    >>> config.CHALLENGE_DIR
    'tmp2'
    
    >>> os.environ['USER_SUBMISSION_DIR'] = 'Invalid Dir Name!'
    >>> os.environ['CHALLENGE_DIR'] = 'Invalid Dir Name!'
    >>> Settings()
    Traceback (most recent call last):
    ...
    pydantic_core._pydantic_core.ValidationError: 2 validation errors for Settings
    USER_SUBMISSION_DIR
      Value error, USER_SUBMISSION_DIR must contain only alphanumeric characters and underscores [type=value_error, input_value='Invalid Dir Name!', input_type=str]
        For further information visit https://errors.pydantic.dev/2.8/v/value_error
    CHALLENGE_DIR
      Value error, CHALLENGE_DIR must contain only alphanumeric characters and underscores [type=value_error, input_value='Invalid Dir Name!', input_type=str]
        For further information visit https://errors.pydantic.dev/2.8/v/value_error
    >>> del os.environ['USER_SUBMISSION_DIR']
    >>> del os.environ['CHALLENGE_DIR']
    >>> config = Settings()
    >>> config.USER_SUBMISSION_DIR
    'user_submissions'
    >>> config.CHALLENGE_DIR
    'challenges'
    """
    USER_SUBMISSION_DIR: str = "user_submissions"
    CHALLENGE_DIR: str = "challenges"
    TEST_FILENAME: str = "test_solution.py"
    PROBLEM_FILENAME: str = "problem.json"
    PORT: int = 3000
    HOST: str = "0.0.0.0"

    @field_validator('USER_SUBMISSION_DIR',
                     'CHALLENGE_DIR')
    def validate_alphanumeric_and_underscore(cls, v, field):
        """validate the fields have only A-Za-z0-9 and _"""
        if not all(char.isalnum() or char in '_-' for char in v):
            raise ValueError(f'{field.field_name} must contain only alphanumeric characters and underscores')
        return v
    

#config: Settings
try:
    config = Settings()
except ValidationError as e:
    print(f'Environment variable validation error: {e}')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
