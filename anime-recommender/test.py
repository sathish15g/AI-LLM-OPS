from  utils.custom_exception import CustomException

try:
    x= 1/0

except Exception as e:
    raise CustomException("An error occurred", e)