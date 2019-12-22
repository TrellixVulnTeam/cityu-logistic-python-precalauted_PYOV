import multiprocessing

from services.CPDService import cPDService

if __name__ == '__main__':
    multiprocessing.freeze_support()
    cPDService.initCPDTable()
    
