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
        TODO check what happens when there is no hash found?
        '''
        try:
            file = self.client_api.get_object("/files/"+hash)
            print(file)
        except Exception:
            return None
        return file
        
   
    
    