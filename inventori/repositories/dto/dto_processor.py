class ProcessorDTO:
    def __init__(self, id_processor=None, nama_processor=None, manufactur=None,
                 model=None, cores=None, threads=None,
                 base_clock=None, max_clock=None,
                 arsitektur=None, keterangan=None,
                 processor_score=None,):
        self.id_processor = id_processor
        self.nama_processor = nama_processor
        self.manufactur = manufactur
        self.model = model
        self.cores = cores
        self.threads = threads
        self.base_clock = base_clock
        self.max_clock = max_clock
        self.arsitektur = arsitektur
        self.keterangan = keterangan
        self.processor_score = processor_score