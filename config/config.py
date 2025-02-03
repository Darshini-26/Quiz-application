from config.aws_ssm import quiz_application1

def database_url():
    try:
        parameter_value = quiz_application1('/quiz_application1/serveroverride')

        for line in parameter_value.splitlines():
            if line.startswith('DATABASE_URL='):
                database_url = line.split('=', 1)[1].strip()  # Strip spaces after the '=' sign
                return database_url

        raise RuntimeError("DATABASE_URL not found in the parameter value.")
    except Exception as e:
        raise RuntimeError(f"Error retrieving database URL: {e}")

