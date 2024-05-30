import requests
import logging

class BaseDataLoader:

    def __init__(self, endpoint=None, logger=None):
        self._base_url = endpoint
        if logger is None:
            logger = logging.getLogger('BASELDR')
        self._logger = logger
        self._logger.info("Створено екземпляр BaseDataLoader")

    def _get_req(self, resource, params=None):
        req_url = self._base_url + resource
        if params is not None:
            self._logger.debug(f"GET: url={req_url}, params={params}")
            response = requests.get(req_url, params=params)
        else:
            self._logger.debug(f"GET: url={req_url}")
            response = requests.get(req_url)
        self._logger.debug(f"RESPONSE: код={response.status_code}")
        if response.status_code != 200:
            msg = f"Не вдалося запросити дані з {req_url}, статус: {response.status_code}"
            if response.text:
                try:
                    json_response = response.json()
                    if 'message' in json_response:
                        msg += f", повідомлення: {json_response['message']}"
                except ValueError:
                    pass
            raise RuntimeError(msg)
        return response.text

if __name__ == "__main__":
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

  
    file_handler = logging.FileHandler('baseloader.log')
    file_handler.setFormatter(formatter)

    
    logger = logging.getLogger('BASELDR')
    logger.setLevel(logging.DEBUG)  # Спробувати різні рівні: DEBUG, INFO, WARNING, ERROR, CRITICAL
    logger.addHandler(file_handler)

    
    loader = BaseDataLoader(endpoint='https://api.example.com', logger=logger)
    
    try:
        data = loader._get_req('/resource', params={'key': 'value'})
    except RuntimeError as e:
        logger.error(e)
