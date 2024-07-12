from abc import ABC, abstractmethod
import vt


class API(ABC):
    @property
    @abstractmethod
    def client_api(self):
        pass
    
    
class VTapi(API):
    def __init__(self,api_key):
        self._api_key = api_key
        self._client_api =  vt.Client(api_key) 

    @property
    def client_api(self):
        return self._client_api
    
    def get_file(self, hash)->vt.Object:
        '''
        Possible issue being the limitations of number of requests
        '''
        try:
            file = self.client_api.get_object("/files/"+hash)
            print(file)
        except Exception:
           return None
        return file

    def close_connection(self):
        self._client_api.close()

    def open_connection(self, api_key = None):
        if api_key:
            self._client_api =  vt.Client(api_key) 
        else:
            self._client_api = vt.Client(self._api_key)
        
        
   
    
    