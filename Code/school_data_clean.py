import pandas as pd
from created_functions import *
import sys

report_df = pd.read_csv("2010_school_report_card.csv")


col_names = ["dbn", "district","school","principal","progress_report_type","school_level","peer_index","overall_grade",
             "overall_score","environment_score","environment_grade","performance_score","performance_grade",
             "progress_score","progress_grade","additional_credit","report_grade"]
report_df.columns = col_names
report_df["school_level"] = report_df["school_level"].replace(["High School Transfer"],["High School"])
report_df = report_df[report_df["school_level"].isin(["Elementary","K-8", "High School", "Middle"])]
sat_df = pd.read_csv("2010_SAT.csv")
sat_col_names = ["dbn","school_name","num_test_takers","sat_critical_reading_mean",
                 "sat_mathematics_mean","sat_writing_mean"]
sat_df.columns = sat_col_names

sat_df = sat_df.drop(columns=["school_name"])

class_df = pd.read_csv("2010_class_size.csv")

class_col_names = ["CSD","SCHOOL CODE","TOTAL REGISTER", "SCHOOLWIDE PUPIL-TEACHER RATIO"]
class_df = class_df[class_col_names]
class_df.columns = ["csd","school_code","class_size", "schoolwide_pupil_teacher_ratio"]
class_df["dbn"] =  class_df.apply(lambda i: str(i["csd"]).zfill(2) + str(i["school_code"]), axis=1)
class_df = class_df.drop(columns=["csd","school_code"])
class_gb_df = class_df.groupby(["dbn"]).agg({"class_size":"sum","schoolwide_pupil_teacher_ratio":"mean"}).reset_index()

regent_df = pd.read_csv("2010_math_regents.csv")
print_df(regent_df,rows=5)
sys.exit()


#class_gb_df = class_df.groupby(["dbn","grade","program_type"]).agg({"class_size":"mean"}).reset_index()
sys.exit()

ap_df = pd.read_csv("2010_AP_scores.csv")
ap_cols_list = ["dbn","school","ap_test_takers","total_exams_taken","num_exams_with_3_4_5_ap_scores"]
ap_df.columns = ap_cols_list
ap_df["num_exams_with_3_4_5_ap_scores"] = ap_df["num_exams_with_3_4_5_ap_scores"].fillna(0)
ap_df = ap_df[["dbn", "num_exams_with_3_4_5_ap_scores"]]

df = report_df.merge(sat_df, on="dbn")
df = df.drop_duplicates(subset=list(df.columns))
df = df[df["school_level"].isin(["High School", "High School Transfer"])]
# df = df.merge(ap_df, on="dbn")
# df = df.drop_duplicates(subset=list(df.columns))

df = df[["dbn","school_level","district","peer_index","overall_score","environment_score","performance_score",
         "progress_score","additional_credit","num_test_takers","sat_critical_reading_mean",
         "sat_mathematics_mean","sat_writing_mean"]]
df["sat_flag"] = 1
df = df[df["peer_index"].notnull()]
df = df[df["sat_critical_reading_mean"].notnull()]
df = df.reset_index(drop=True)
df["sat_flag"] = 1

non_df = report_df[~report_df["dbn"].isin(df["dbn"])]
non_df = non_df[["dbn","school_level","district","peer_index","overall_score","environment_score","performance_score",
         "progress_score","additional_credit"]]
non_df["sat_flag"] = 0
new_df = pd.concat([df,non_df])
for n in ["peer_index","overall_score"]:
    new_df = new_df[new_df[n].notnull()]

new_df = new_df.drop(columns=["dbn"])
new_df = new_df.drop_duplicates(subset=list(new_df.columns))
print(new_df.shape)
new_df.to_csv("2010_all_school_scores.csv",index=False)