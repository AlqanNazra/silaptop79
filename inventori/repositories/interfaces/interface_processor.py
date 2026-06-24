from abc import ABC, abstractmethod

class IProcessorRepository(ABC):
    
    @abstractmethod
    def tambah_processor(self, data):
        pass
        
    @abstractmethod
    def ambil_processor(self):
        pass
        
    @abstractmethod
    def ambil_processor_by_id(self,id_processor):
        pass
    
    @abstractmethod
    def update_processor(self, data):
        pass
    
    @abstractmethod
    def hapus_processor(self, id_processor):
        pass
    @abstractmethod
    def ambil_processor_dropdown(self):
        pass