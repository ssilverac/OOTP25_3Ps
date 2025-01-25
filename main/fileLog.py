import logging

#Logging config

def config_log(filePath):
    logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=filePath,
    filemode='w' #this will overwrite log file
    )
