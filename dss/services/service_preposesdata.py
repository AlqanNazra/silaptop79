from dss.repositories.repositori_laptop_pengadaan import LaptopPengadaanRepository
from dss.repositories.dto.dto_laptop_pengadaan import FilterPengadaanDTO
from dss.repositories.dto.dto_laptop_pengadaan import LaptopPengadaanDTO

from inventori.repositories.dto.dto_laptop_inventori import LaptopInventoriDetailDTO
from inventori.repositories.dto.dto_laptop_inventori import FilterInventoriDTO
from inventori.repositories.repositori_laptop_inventori import LaptopInventoriRepository

from collections import defaultdict
from typing import Union, Optional
import re

class Servicepreposesdata:
    
    def __init__(self, conn):
        self.conn = conn
        self.repoLP = LaptopPengadaanRepository(conn)
        self.repoLI = LaptopInventoriRepository(conn) 
    def ekstrak_processor(self, text):
            if not text:
                return None, None, None

            text_lower = text.lower()

            special_series = [
                "core ultra",
                "ryzen ai",
                "celeron",
                "snapdragon",
            ]

            for s in special_series:
                if s in text_lower:
                    tier_match = re.search(rf'{s}\s*(\d+)', text_lower)
                    tier = tier_match.group(1) if tier_match else None

                    series = f"{s} {tier}" if tier else s

                    model_match = re.search(r'(\d{3,5})', text)
                    model = int(model_match.group(1)) if model_match else None

                    gen = int(str(model)[0]) if model else None

                    return series, model, gen
            apple_match = re.search(r'\bM(\d)\b', text)
            if apple_match:
                gen = int(apple_match.group(1))
                return f"M{gen}", None, gen
            amd_match = re.search(r'ryzen\s*(\d)\s*(\d{4,5})', text_lower)
            if amd_match:
                series = int(amd_match.group(1))
                model = int(amd_match.group(2))
                gen = int(str(model)[0])
                return series, model, gen
            intel_match = re.search(r'i(\d)[-\s]*(\d{4,5})', text_lower)
            if intel_match:
                series = int(intel_match.group(1))
                model = int(intel_match.group(2))

                gen = int(str(model)[:2]) if len(str(model)) >= 4 else int(str(model)[0])
                return series, model, gen
            model_match = re.search(r'(\d{3,5})', text)
            if model_match:
                model = int(model_match.group(1))
                gen = int(str(model)[0])
                return None, model, gen

            return None, None, None

    def mapping_processor(self, series, gen):
        if not series:
            return 3 

        series_lower = str(series).lower()
        tier_weight = 2
        tier = None
        bonus = 0
        special_series = ["core ultra", "ryzen ai", "celeron", "snapdragon"]

        for s in special_series:
            if s in series_lower:
                tier_match = re.search(rf'{s}\s*(\d+)', series_lower)
                tier = int(tier_match.group(1)) if tier_match else 1

                match s:
                    case "core ultra":
                        bonus = 1.0
                    case "ryzen ai":
                        bonus = 1.0
                    case "celeron":
                        return 2
                    case "snapdragon":
                           return 3

                break
        apple_match = re.search(r'\bm(\d)\b', series_lower)
        if apple_match:
            gen_apple = int(apple_match.group(1))
            return 8 + gen_apple
        if tier is None:
            tier_match = re.search(r'(\d)', series_lower)
            tier = int(tier_match.group(1)) if tier_match else 3

        gen = gen if gen else 1

        score = (tier * tier_weight) + gen + bonus
        return score
    
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
            series, model, gen = self.ekstrak_processor(
                item.get("nama_processor") or item.get("processor")
            )
            skor_processor = self.mapping_processor(series, gen)

            hasil.append({
                "id": item.get("id_laptop_inventori") or item.get("id_laptop_pengadaan"),

                "processor": skor_processor,

                "ram": item.get("ram_kapasitas") or item.get("ram") or 0,

                "storage": item.get("storage_kapasitas") or item.get("storage") or 0,

                "berat": item.get("berat", 0),

                "layar": item.get("ukuran_layar", 0),

                "baterai": item.get("baterai", 0)
            })

        return hasil