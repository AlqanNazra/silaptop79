from dss.repositories.repositori_laptop_pengadaan import LaptopPengadaanRepository
from dss.repositories.dto.dto_laptop_pengadaan import FilterPengadaanDTO
from dss.repositories.dto.dto_laptop_pengadaan import LaptopPengadaanDTO

from inventori.repositories.dto.dto_laptop_inventori import LaptopInventoriDetailDTO
from inventori.repositories.dto.dto_laptop_inventori import FilterInventoriDTO
from inventori.repositories.repositori_laptop_inventori import LaptopInventoriRepository

from collections import defaultdict
from typing import Union, Optional
import re

class PreprocessingService:
    
    def __init__(self, conn):
        self.conn = conn
        self.repoLP = LaptopPengadaanRepository(conn)
        self.repoLI = LaptopInventoriRepository(conn) 
    
    def filtering_data(
        self, 
        sumber_data: str, 
        data: Union[FilterPengadaanDTO, FilterInventoriDTO]
    ) -> dict:
        try:
            with self.conn:
                if sumber_data == "pengadaan":
                    if not isinstance(data, FilterPengadaanDTO):
                        return {
                            "status": "error",
                            "message": "Untuk pengadaan, gunakan FilterPengadaanDTO"
                        }
                    filtered_data = self.repoLP.filter_pengadaan(data)
                    result = filtered_data
                    processed = self.preprocessing_processor(result)
                    
                    return {
                        "status": "success",
                        "sumber": "pengadaan",
                        "data_raw": result,
                        "data_processed": processed,
                        "total": len(result),
                        "message": f"Berhasil mengambil {len(result)} data pengadaan"
                    }
                elif sumber_data == "inventori":
                    if not isinstance(data, FilterInventoriDTO):
                        return {
                            "status": "error",
                            "message": "Untuk inventori, gunakan FilterInventoriDTO"
                        }
                    filtered_data = self.repoLI.filter_inventori(data)
                    result = filtered_data
                    processed = self.preprocessing_processor(result)
                    
                    return {
                        "status": "success",
                        "sumber": "inventori",
                        "data_raw": result,
                        "data_processed": processed,
                        "total": len(result),
                        "message": f"Berhasil mengambil {len(result)} data inventori"
                    }
                else:
                    return {
                        "status": "error",
                        "message": f"Sumber data '{sumber_data}' tidak valid. Gunakan 'pengadaan' atau 'inventori'"
                    }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Gagal filter data: {str(e)}"
            }

    def preprocessing_processor(self, data_list):
        hasil = []
        
        for item in data_list:
            processor_text = item.get("processor")
            series,model,gen = self.ekstrak_processor(processor_text)
            skor_processor = self.mapping_processor(series,gen)
            hasil.append({
                "id": item.get("id") or item.get("id_laptop_pengadaan") or item.get("id_laptop_inventori"),
                "processor": skor_processor
            })

        return hasil

    def preprocessing(self, data_list):
        hasil = []

        for item in data_list:

            hasil.append({
                "id": item.get("id_laptop_inventori") or item.get("id_laptop_pengadaan"),

                "ram": item.get("ram_kapasitas") or item.get("ram") or 0,

                "storage": item.get("storage_kapasitas") or item.get("storage") or 0,

                "berat": item.get("berat", 0),

                "layar": item.get("ukuran_layar", 0),

                "baterai": item.get("baterai", 0)
            })

        return hasil

    def split_role_requirement(self,data_list,role_requirement):
        role_match = []
        min_ram = role_requirement["min_ram"]
        min_storage = role_requirement["min_storage"]
        min_processor_score = role_requirement["min_processor_score"]
        for item in data_list:
            ram = item.get("ram_kapasitas", 0)
            storage = item.get("storage_kapasitas", 0)
            processor_score = (
                item.get("benchmark_score")
                or 0
            )
            if (
                ram >= min_ram
                and storage >= min_storage
                and processor_score >= min_processor_score
            ):
                role_match.append(item)
        return {
            "role_match": role_match,
            "fallback": data_list
        }