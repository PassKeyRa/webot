from app.imports import *


def loadEnv():
    try:
        load_dotenv()
        aws_access_key_id = getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = getenv('AWS_SECRET_ACCESS_KEY')
        region_name = getenv('REGION_NAME')
        queue_name_in = getenv('QUEUE_NAME_IN')
        queue_name_out = getenv('QUEUE_NAME_OUT')
        return aws_access_key_id, aws_secret_access_key, region_name, queue_name_in, queue_name_out
    except Exception as e:
        logger.exception("Some error occured: {}".format(e))
