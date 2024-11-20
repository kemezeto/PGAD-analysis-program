import abc
import pandas as pd
import basedata
from abc import ABC, abstractmethod

'''
Abstract classes do not need to be instantiated
'''


class AbstractMultiple(ABC):
    def __init__(self, allconf):
        self.ReferenceSequenceSite = allconf["mc"]["reference_sequence_site"]
        self.Gff = allconf["mc"]["reference_gff"]
        self.InterChr = allconf["mc"]["inter_chr"]
        self.DoubleChr = allconf["mc"]["double_chr"]
        self.DoubleColumn=allconf["mc"]["double_column"]
        self.DivideInterval=allconf["mc"]["divide_interval"]
        self.SaveFile = allconf["mc"]["savefile"]

    def get_name(self):
        return self.ReferenceSequenceSite, self.Gff, self.InterChr

    def get_df(self):
        return self.main()

    def gfftodf(self):
        new_gff = basedata.newgff(self.Gff)
        df0 = pd.DataFrame({"reference1": new_gff})
        return df0

    @abstractmethod
    def main(self):
        print('Need to rewrite')
