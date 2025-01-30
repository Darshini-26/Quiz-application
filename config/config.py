from config.aws_ssm import quiz_application

def database_url():
    try:
        parameter_value=quiz_application('/quiz_application/serveroverride')

        for line in parameter_value.splitlines():
            if line.startswith('DATABASE_URL='):
                database_url=line.split('=',1)[1].strip()
                return database_url

        raise RuntimeError("DATABASE_URL not found in the parameter value.")
    except Exception as e:
        raise RuntimeError(f"Error retrieving database URL: {e}")
