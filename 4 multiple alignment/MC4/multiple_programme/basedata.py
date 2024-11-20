
import configparser
import warnings
import pandas as pd

warnings.filterwarnings("ignore")


# warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)


def config(file):
    l1 = []
    conf = configparser.ConfigParser()
    conf.read(file)
    for section in conf.sections():
        l2 = []
        for key, value in conf.items(section):
            if section in ["multiple_alignment", "column_name", "Interspecies comparison collinearity file",
                           "Interspecies_comparison_collinearity_file", "Double_One_collinearity"]:
                l2.append(value)
            else:
                l2.append([key, value])
        l1.append(l2)
    return l1


def section(file):
    l1 = []
    conf = configparser.ConfigParser()
    conf.read(file)
    for section in conf.sections():
        l1.append(section)
    return l1


def site(reference_sequence_site):
    return [2, 0] if reference_sequence_site == "right" else [0, 2]


def newgff(gff):
    reference_sequence = []
    with open(gff, 'r') as f:
        for ref_seq in f:
            reference_sequence.append(ref_seq.split()[1])
    reference_sequence = list(set(reference_sequence))
    reference_sequence.sort()
    return reference_sequence


def find_digits_in_string(s):
    s.lower()
    index = s.find('g')
    if index == -1:  # 'g' not found
        return None
    digit_positions = [x for x in s[:index] if x.isdigit()]
    if len(digit_positions) == 1:
        return int(digit_positions[0])
    else:
        return int(digit_positions[0] + digit_positions[1])


def read_collinearity(file, refsequence_site):
    reference_list = []
    comparison_list = []
    n_list = []
    chr1_lsit = []
    chr2_list = []
    with open(file, 'r') as fobj:
        for eachLine in fobj:
            if eachLine == "\n":
                continue
            to_list = eachLine.split(" ")
            if eachLine[0] == "#":
                chr_num = to_list[6].split("&")
                chr_num.insert(1, "&")
                n = int(to_list[5][2:])
                continue
            else:
                reference_list.append(to_list[site(refsequence_site)[0]])
                comparison_list.append(to_list[site(refsequence_site)[1]])
                chr1 = chr_num[site(refsequence_site)[0]]
                chr2 = chr_num[site(refsequence_site)[1]]
                chr1_lsit.append(chr1)
                chr2_list.append(chr2)
                n_list.append(n)

    return [reference_list, comparison_list, n_list, chr1_lsit, chr2_list]


def seven_list(file, refsequence_site):
    reference_list = []
    comparison_list = []
    n_list = []
    chr1_lsit = []
    chr2_list = []
    chr1_gene = []
    chr2_gene = []
    with open(file, 'r') as fobj:
        for eachLine in fobj:
            if eachLine == "\n":
                continue
            to_list = eachLine.split(" ")
            if eachLine[0] == "#":
                chr_num = to_list[6].split("&")
                chr_num.insert(1, "&")
                n = int(to_list[5][2:])
                continue
            else:
                reference_list.append(to_list[site(refsequence_site)[0]])
                comparison_list.append(to_list[site(refsequence_site)[1]])
                chr1 = chr_num[site(refsequence_site)[0]]
                chr2 = chr_num[site(refsequence_site)[1]]
                chr1_lsit.append(chr1)
                chr2_list.append(chr2)
                chr1_gene.append(int(to_list[site(refsequence_site)[0] + 1]))
                chr2_gene.append(int(to_list[site(refsequence_site)[1] + 1]))
                n_list.append(n)

    return [reference_list, comparison_list, n_list, chr1_lsit, chr2_list, chr1_gene, chr2_gene]


def doublingtodf(collinearity, rssite, selfgc, selfchr, index):
    # global intrachr_df
    self_chr = config(selfchr)
    five_col = read_collinearity(collinearity, rssite)
    try:
        intrachr_df = chr_judgment(self_chr[index])
    except:
        print(
            "Error:Please check whether all chromosome correspondences in the chr-chr are filled in and the corresponding format is correct")
        print("corresponding format example:1=(14,5)/(3,20)/(17)")
    df = pd.DataFrame({"reference1": five_col[0],
                       "col_name": five_col[1],
                       "N": five_col[2],
                       "chr1": five_col[3],
                       "chr2": five_col[4]})
    df.sort_values(by=["reference1", 'N'],
                   ascending=[True, False],
                   ignore_index=True,
                   inplace=True)

    df = pd.merge(df, intrachr_df, how="left")

    df.dropna(axis=0,
              how='any',
              thresh=None,
              subset=None,
              inplace=True)

    df_list = [df.loc[df["judgment"] == n + 1] for n in range(int(selfgc))]  # range needed to be changed
    for dindex in range(len(df_list)):
        df_list[dindex].drop_duplicates(subset=["reference1"],
                                        keep='first',
                                        inplace=True,
                                        ignore_index=True)
        df_list[dindex].drop(columns=["N", "chr1", "chr2", "judgment"],
                             inplace=True)

    return df_list


def double_interval(collinearity, rssite, selfgc, selfchr, index):
    self_chr = config(selfchr)
    seven_col = seven_list(collinearity, rssite)
    try:
        intrachr_df = chr_interval(self_chr[index])
    except:
        print(
            "Error:Please check whether all chromosome correspondences in the chr-chr are filled in and the corresponding format is correct")
        print("corresponding format example:1=(14,5)/(3,20)/(17)")
    df = pd.DataFrame({"reference1": seven_col[0],
                       "col_name": seven_col[1],
                       "N": seven_col[2],
                       "chr1": seven_col[3],
                       "chr2": seven_col[4],
                       "chr1_gene": seven_col[5],
                       "chr2_gene": seven_col[6]})

    df = pd.merge(df, intrachr_df, on=["chr1", "chr2"])  # how="left",

    df.dropna(axis=0,
              how='any',
              thresh=None,
              subset=None,
              inplace=True)
    # df.to_csv("test1.csv")
    filtered_df = df[(df["chr1_start"] <= df["chr1_gene"]) & (df["chr1_gene"] <= df["chr1_end"]) & (
            df["chr2_start"] <= df["chr2_gene"]) & (df["chr2_gene"] <= df["chr2_end"])]
    # filtered_df.to_csv("test2.csv")
    filtered_df.sort_values(by=["reference1", 'N'],
                            ascending=[True, False],
                            ignore_index=True,
                            inplace=True)
    # filtered_df.to_csv("test3.csv")
    df_list = [filtered_df.loc[filtered_df["judgment"] == n + 1] for n in range(int(selfgc))]  # range needed to be changed

    for dindex in range(len(df_list)):
        df_list[dindex].drop_duplicates(subset=["reference1"],
                                        keep='first',
                                        inplace=True,
                                        ignore_index=True)
        df_list[dindex].drop(
            columns=["N", "chr1", "chr2", "judgment", "chr1_gene", "chr2_gene", "chr1_start", "chr1_end", "chr2_start",
                     "chr2_end"],
            inplace=True)

    return df_list


def reference_double(collinearity, rssite, selfgc, SelfChr):
    self_chr = config(SelfChr)
    five_col = read_collinearity(collinearity, rssite)
    intrachr_df = chr_judgment(self_chr[0])
    df = pd.DataFrame({"reference1": five_col[0],
                       "reference2": five_col[1],
                       "N": five_col[2],
                       "chr1": five_col[3],
                       "chr2": five_col[4]})
    df.sort_values(by=["reference1", 'N'],
                   ascending=[True, False],
                   ignore_index=True,
                   inplace=True)

    df = pd.merge(df, intrachr_df, how="left")

    df.dropna(axis=0,
              how='any',
              thresh=None,
              subset=None,
              inplace=True)

    dfl = [df.loc[df["judgment"] == n + 1] for n in range(int(selfgc))]  # selfgc needed to be changed

    for dindex in range(len(dfl)):
        num = str(dindex + 2)
        dfl[dindex].drop_duplicates(subset=["reference1"],
                                    keep='first',
                                    inplace=True,
                                    ignore_index=True)
        dfl[dindex].drop(columns=["N", "chr1", "chr2", "judgment"],
                         inplace=True)
        dfl[dindex].columns = ["reference1", "reference" + num]

    return dfl


def inter_df_list(collinearity, rssite, interchr):
    # global interchr_df
    l = []
    chr_chr = config(interchr)
    for k in range(len(collinearity)):
        five_col = read_collinearity(collinearity[k], rssite)
        try:
            interchr_df = chr_judgment(chr_chr[k])
        except:
            print(
                "Error:Please check whether all chromosome correspondences in the chr-chr are filled in and the corresponding format is correct")
            print("corresponding format example:1=(14,5)/(3,20)/(17)")

        df = pd.DataFrame({"reference1": five_col[0],
                           "col_name": five_col[1],
                           "N": five_col[2],
                           "chr1": five_col[3],
                           "chr2": five_col[4]})

        dfr = pd.merge(df, interchr_df, how="left")

        dfr.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)

        dfr.sort_values(by=["reference1", 'N'],
                        ascending=[True, False],
                        ignore_index=True,
                        inplace=True)
        dfr.drop_duplicates(subset=["reference1"], keep='first', inplace=True,
                            ignore_index=True)

        dfr.drop(columns=["N", "chr1", "chr2", "judgment"], inplace=True)
        l.append(dfr)
    return l


def inter_interval(collinearity, rssite, interchr):
    # global interchr_df
    l = []
    chr_chr = config(interchr)
    for k in range(len(collinearity)):
        seven_col = seven_list(collinearity[k], rssite)
        try:
            interchr_df = chr_interval(chr_chr[k])
        except:
            print(
                "Error:Please check whether all chromosome correspondences in the chr-chr are filled in and the corresponding format is correct")
            print("corresponding format example:1=(14,5)/(3,20)/(17)")

        df = pd.DataFrame({"reference1": seven_col[0],
                           "col_name": seven_col[1],
                           "N": seven_col[2],
                           "chr1": seven_col[3],
                           "chr2": seven_col[4],
                           "chr1_gene": seven_col[5],
                           "chr2_gene": seven_col[6]})

        dfr = pd.merge(df, interchr_df, on=["chr1", "chr2"])
        dfr.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
        dfr.sort_values(by=["reference1", 'N'],
                        ascending=[True, False],
                        ignore_index=True,
                        inplace=True)

        filtered_df = dfr[(dfr["chr1_start"] <= dfr["chr1_gene"]) & (dfr["chr1_gene"] <= dfr["chr1_end"]) & (
                dfr["chr2_start"] <= dfr["chr2_gene"]) & (dfr["chr2_gene"] <= dfr["chr2_end"])]


        filtered_df.drop_duplicates(subset=["reference1"], keep='first', inplace=True,
                                    ignore_index=True)

        filtered_df.drop(
            columns=["N", "chr1", "chr2", "judgment", "chr1_gene", "chr2_gene", "chr1_start", "chr1_end", "chr2_start",
                     "chr2_end"], inplace=True)
        l.append(filtered_df)
    return l


def deal_inter_double(interdf, double_list):
    multi = list(
        map(lambda x: pd.merge(x, interdf, left_on=x.columns[1], right_on="reference1", how='left'), double_list))
    list(map(lambda x: x.drop(columns=[x.columns[2]], inplace=True), multi))
    return multi


def chr_judgment(data):
    chr_dict = {}
    for i in data:
        key = i[0]
        if '/' in i[1] or '(' in i[1]:
            values = i[1].split('/')
        else:
            values = i[1].split(',')
        chr_dict[key] = values
    chr_list = []
    for key, values in chr_dict.items():
        group = 0
        for v in values:
            group += 1
            if v == '':
                continue
            if "(" in v:
                value = [x.strip() for x in v.replace("(", "").replace(")", "").split(",")]
                for vs in value:
                    chr_list.append([str(key), str(vs), group])
            else:
                group = 1
                chr_list.append([str(key), str(v), group])

    chr_df = pd.DataFrame(chr_list, columns=['chr1', 'chr2', 'judgment'])

    return chr_df


def chr_interval(data):
    chr_dict = {}
    for i in data:
        key = i[0]
        if '/' in i[1] or '(' in i[1]:
            values = i[1].split('/')
        else:
            values = i[1].split(',')
        chr_dict[key] = values
    chr_list = []
    for key, values in chr_dict.items():
        group = 0
        if '-' in key:
            start_index = key.find('[')
            middle_index = key.find('-')
            end_index = key.find(']')
            start_key = int(key[start_index + 1:middle_index])
            end_key = int(key[middle_index + 1:end_index])
            for v in values:
                group += 1
                if v == '':
                    continue
                if "(" in v:
                    value = [x.strip() for x in v.replace("(", "").replace(")", "").split(",")]
                    for vs in value:
                        if '-' in vs:
                            start_vs = vs.find('[')
                            middle_vs = vs.find('-')
                            end_vs = vs.find(']')
                            start_chr = int(vs[start_vs + 1:middle_vs])
                            end_chr = int(vs[middle_vs + 1:end_vs])
                            chr_list.append(
                                [str(key[0:start_index]), start_key, end_key, str(vs[0:start_vs]), start_chr, end_chr,
                                 group])
                        else:
                            chr_list.append([str(key[0:start_index]), 0, 1000000, str(vs), 0, 1000000, group])
                else:
                    group = 1
                    if '-' in v:
                        start_v = v.find('[')
                        middle_v = v.find('-')
                        end_v = v.find(']')
                        start_chr = int(v[start_v + 1:middle_v])
                        end_chr = int(v[middle_v + 1:end_v])
                        chr_list.append(
                            [str(key[0:start_index]), start_key, end_key, str(v[0:start_v]), start_chr, end_chr, group])
                    else:
                        chr_list.append([str(key[0:start_index]), 0, 1000000, str(v), 0, 1000000, group])
        else:
            for v in values:
                group += 1
                if v == '':
                    continue
                if "(" in v:
                    value = [x.strip() for x in v.replace("(", "").replace(")", "").split(",")]
                    for vs in value:
                        if '-' in vs:
                            start_vs = vs.find('[')
                            middle_vs = vs.find('-')
                            end_vs = vs.find(']')
                            start_chr = int(vs[start_vs + 1:middle_vs])
                            end_chr = int(vs[middle_vs + 1:end_vs])
                            chr_list.append(
                                [str(key), 0, 1000000, str(vs[0:start_vs]), start_chr, end_chr,
                                 group])
                        else:
                            chr_list.append([str(key), 0, 1000000, str(vs), 0, 1000000, group])
                else:
                    group = 1
                    if '-' in v:
                        start_v = v.find('[')
                        middle_v = v.find('-')
                        end_v = v.find(']')
                        start_chr = int(v[start_v + 1:middle_v])
                        end_chr = int(v[middle_v + 1:end_v])
                        chr_list.append(
                            [str(key), 0, 1000000, str(v[0:start_v]), start_chr, end_chr, group])
                    else:
                        chr_list.append([str(key), 0, 1000000, str(v), 0, 1000000, group])

    chr_df = pd.DataFrame(chr_list,
                          columns=["chr1", "chr1_start", "chr1_end", "chr2", "chr2_start", "chr2_end", "judgment"])

    return chr_df


def quadratic_matching(ma_file, self_file):
    mf_df = pd.read_csv(ma_file)
    sf_df = pd.read_csv(self_file)
    sm_df = pd.merge(sf_df, mf_df, left_on=sf_df.columns[1], right_on=mf_df.columns[0], how="left")
    msm_df = pd.merge(mf_df, sm_df, left_on=mf_df.columns[0], right_on=sm_df.columns[0], how="left")
    msm_df.to_csv("test2.csv")


if __name__ == '__main__':
    # quadratic_matching("../data/all.csv","../data/self.csv")
    # print(config("../conf/test.txt"))
    print(chr_interval(config("../conf/test.txt")[0]))
    print("0")
