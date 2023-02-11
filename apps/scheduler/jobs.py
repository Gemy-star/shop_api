import logging


class Jobs:
    @staticmethod
    def job_temp_task():
        logger = logging.getLogger(__name__)
        logger.info("Start job Uploading CDR File to ovp")
