import configparser
import pandas as pd
import basedata
import warnings
from functools import reduce
from abstract_multiple import AbstractMultiple

warnings.filterwarnings("ignore")


class MC(AbstractMultiple):
    def __init__(self, AllConf):
        super(MC, self).__init__(AllConf)

    def get_name(self):
        return None

    def doubling_one(self):
        # A double species sequence is merged with a reference species sequence
        section_list = basedata.section(self.DoubleChr)
        section_alter = list(map(lambda x: "../data/" + x, section_list))
        double_df_list = []
        if self.DivideInterval == "flase":
            for collinearity_index in range(len(section_alter)):
                df_list = basedata.doublingtodf(section_alter[collinearity_index],
                                                self.ReferenceSequenceSite,
                                                self.DoubleColumn,
                                                self.DoubleChr,
                                                collinearity_index)

                df_list.insert(0, self.gfftodf())
                dbone_df = reduce(lambda x, y: pd.merge(x, y, on="reference1", how="left"), df_list)
                double_df_list.append(dbone_df)
        else:
            for collinearity_index in range(len(section_alter)):
                df_list = basedata.double_interval(section_alter[collinearity_index],
                                                   self.ReferenceSequenceSite,
                                                   self.DoubleColumn,
                                                   self.DoubleChr,
                                                   collinearity_index)

                df_list.insert(0, self.gfftodf())
                dbone_df = reduce(lambda x, y: pd.merge(x, y, on="reference1", how="left"), df_list)
                double_df_list.append(dbone_df)
        double_df = reduce(lambda x, y: pd.merge(x, y, on="reference1", how="left"), double_df_list)

        return double_df

    def interdf_list(self):
        section_list = basedata.section(self.InterChr)
        section_alter = list(map(lambda x: "../data/" + x, section_list))
        if self.DivideInterval == "false":
            inter_df_list = basedata.inter_df_list(section_alter,
                                                   self.ReferenceSequenceSite,
                                                   self.InterChr)
        else:
            inter_df_list = basedata.inter_interval(section_alter,
                                                    self.ReferenceSequenceSite,
                                                    self.InterChr)
        return inter_df_list

    def main(self):
        if self.InterChr != "none" and self.DoubleChr == "none":
            inter_df_list = self.interdf_list()
            inter_df_list.insert(0, self.gfftodf())
            mc_df = reduce(lambda x, y:pd.merge(x, y, on="reference1", how="left"),inter_df_list)


        if self.InterChr == "none" and self.DoubleChr != "none":
            mc_df = self.doubling_one()


        if self.InterChr != "none" and self.DoubleChr != "none":
            inter_df_list = self.interdf_list()
            inter_df_list.insert(0, self.doubling_one())
            mc_df = reduce(lambda x, y:
                                     pd.merge(x, y, on="reference1", how="left"),
                                     inter_df_list)
        mc_df.to_csv(self.SaveFile,index=False)

        return "finished"


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('../conf/mc.conf')
    mc = MC(config)
    # print(mc.get_name())
    # print(mc.doubling_one())
    # print(mc.interdf_list())
    print(mc.main())
