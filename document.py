import pandas as pd


class TxtFile:
    @staticmethod
    def parse(file):
        pass


class XlsxFile:
    @staticmethod
    def parse(file):
        df = pd.read_excel(file)
        
