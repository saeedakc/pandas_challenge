#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
school_data_to_load = "Desktop/School/GT-Data/Homework/04-Pandas/Instructions/PyCitySchools/Resources/schools_complete.csv"
student_data_to_load = "Desktop/School/GT-Data/Homework/04-Pandas/Instructions/PyCitySchools/Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas Data Frames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

school_df = pd.DataFrame(school_data)

total_schools = school_df["School ID"].count()
total_students = school_df["size"].sum()
total_budget= school_df["budget"].sum()

school_df.head()
print(total_schools, total_budget, total_students)


# In[ ]:


school_data = school_data.rename(columns={"name": "school name"})
student_data = student_data.rename(columns={"school": "school name"})

# Combine the data into a single dataset
school_data_complete = pd.merge(school_data, student_data, how="left", on=["school name"])
school_data_complete.head()


# In[ ]:


# total_schools = school_data_complete["School ID"].value_counts()
# total_students = school_data_complete["Student ID"].sum()
# total_budget= school_data_complete["budget"].sum()
avgmathscore = school_data_complete["math_score"].mean()
avgreadingscore = school_data_complete["reading_score"].mean()
passingmath = school_data_complete.query('math_score >70')["School ID"].count()/ total_students*100
passingreading = school_data_complete.query('reading_score >70')["School ID"].count()/ total_students*100
overallpassrate = (avgmathscore + avgreadingscore)/2
District_summary_df = pd.DataFrame({"Total Schools":[total_schools],
                                   "Total Students":[total_students],
                                   "Total Budget":[total_budget],
                                   "Average Math Score":[avgmathscore],
                                   "Average Reading Score":[avgreadingscore],
                                   "% Passing Math":[passingmath],
                                   "% Passing Reading":[passingreading],
                                   "% Overall Passing Rate":[overallpassrate]
})



District_summary_df = District_summary_df[["Total Schools",
"Total Students",
"Total Budget",
"Average Math Score",
"Average Reading Score",
"% Passing Math",
"% Passing Reading",
"% Overall Passing Rate"]]


District_summary_df

District_summary_df["Average Math Score"] = District_summary_df["Average Math Score"]
District_summary_df["Average Reading Score"] = District_summary_df["Average Reading Score"]
District_summary_df["Total Budget"] = District_summary_df["Total Budget"].map("${:,}".format)
District_summary_df["% Passing Math"] = District_summary_df["% Passing Math"]
District_summary_df["% Passing Reading"] = District_summary_df["% Passing Reading"]
District_summary_df["% Overall Passing Rate"] = District_summary_df["% Overall Passing Rate"]


District_summary_df


# In[ ]:


school_data_complete_new = school_data_complete[["School ID", "school name", "type", "size", "budget", "Student ID", "name",
                                                 "gender", "grade", "reading_score","math_score"]].copy()
school_data_complete_new.head()


# In[ ]:


school_data_complete_new["School ID"].count()


# In[ ]:


grouped_school_data = school_data_complete_new.groupby(['school name', "type"])
# grouped_school_data.drop_duplicates(subset=[budget], keep=False)


total_students_grp = grouped_school_data["Student ID"].count()
# total_budget_grp = grouped_school_data["budget"]
# total_budget_grp_var = total_budget_grp/ total_students_grp
total_budget_grp = grouped_school_data["budget"].mean()
per_stu_budget_grp =  (total_budget_grp/ total_students_grp)
avgmathscore_grp = grouped_school_data["math_score"].mean()
avgreadingscore_grp = grouped_school_data["reading_score"].mean()
passingmath_grp = school_data_complete_new.query('math_score >70')["School ID"].count()/ total_students_grp
passingreading_grp = school_data_complete_new.query('reading_score >70')["School ID"].count()/ total_students_grp 
overallpassrate_grp = ((avgmathscore_grp + avgreadingscore_grp)/2)
  
# Converting a GroupBy object into a DataFrame
grouped_school_data_df = pd.DataFrame({"Total Students":total_students_grp,
                                       "Total School Budget": total_budget_grp, 
                                       "Per Student Budget":per_stu_budget_grp,
                                       "Average Math Score": avgmathscore_grp,
                                       "Average Reading Score": avgreadingscore_grp,   
                                       "% Passing Math":passingmath_grp,
                                       "% Passing Reading":passingreading_grp,
                                        "%Overall Passing Rate":overallpassrate_grp          
                                    
                                      
})

grouped_school_data_df = grouped_school_data_df[[  "Total Students",
    "Total School Budget",
    "Per Student Budget",
    "Average Math Score",
    "Average Reading Score",
     "% Passing Math",   
     "% Passing Reading",                                             
    "%Overall Passing Rate"]]

grouped_school_data_df["Total School Budget"] = grouped_school_data_df["Total Students"].map("${:,.2f}".format)
grouped_school_data_df["Per Student Budget"] = grouped_school_data_df["Per Student Budget"].map("${:,.2f}".format)
grouped_school_data_df.head(10)


# In[ ]:


Top_schools = grouped_school_data_df.sort_values(
    ["%Overall Passing Rate"], ascending=False)
Top_schools.head()


# In[ ]:


Bottom_schools = grouped_school_data_df.sort_values(
    ["%Overall Passing Rate"], ascending=True)
Bottom_schools.head()


# In[ ]:


nineth_graders = school_data_complete[(school_data_complete["grade"] == "9th")]
tenth_graders = school_data_complete[(school_data_complete["grade"] == "10th")]
eleventh_graders = school_data_complete[(school_data_complete["grade"] == "11th")]
twelfth_graders = school_data_complete[(school_data_complete["grade"] == "12th")]

nineth_graders_scores = nineth_graders.groupby(["school name"]).mean()["math_score"]
tenth_graders_scores = tenth_graders.groupby(["school name"]).mean()["math_score"]
eleventh_graders_scores = eleventh_graders.groupby(["school name"]).mean()["math_score"]
twelfth_graders_scores = twelfth_graders.groupby(["school name"]).mean()["math_score"]


scores_by_grade_df = pd.DataFrame({"9th": nineth_graders_scores,
                                "10th":tenth_graders_scores,
                                "11th":eleventh_graders_scores,
                                "12th":twelfth_graders_scores
})

scores_by_grade_df.index.name = None

scores_by_grade_df = scores_by_grade_df [["9th", "10th", "11th", "12th"]]
scores_by_grade_df


# In[ ]:


nineth_graders = school_data_complete[(school_data_complete["grade"] == "9th")]
tenth_graders = school_data_complete[(school_data_complete["grade"] == "10th")]
eleventh_graders = school_data_complete[(school_data_complete["grade"] == "11th")]
twelfth_graders = school_data_complete[(school_data_complete["grade"] == "12th")]

nineth_graders_scores = nineth_graders.groupby(["school name"]).mean()["reading_score"]
tenth_graders_scores = tenth_graders.groupby(["school name"]).mean()["reading_score"]
eleventh_graders_scores = eleventh_graders.groupby(["school name"]).mean()["reading_score"]
twelfth_graders_scores = twelfth_graders.groupby(["school name"]).mean()["reading_score"]


scores_by_grade_df = pd.DataFrame({"9th": nineth_graders_scores,
                                "10th":tenth_graders_scores,
                                "11th":eleventh_graders_scores,
                                "12th":twelfth_graders_scores    
})

scores_by_grade_df.index.name = None

scores_by_grade_df = scores_by_grade_df [["9th", "10th", "11th", "12th"]]
scores_by_grade_df


# In[ ]:


grouped_school_data_dfbn = grouped_school_data_df.copy()
#grouped_school_data_dfbn.head()


# In[ ]:


grouped_school_data_df3 = grouped_school_data_dfbn[["Per Student Budget","Average Math Score","Average Reading Score","% Passing Math","% Passing Reading",
                                     "%Overall Passing Rate"]]
grouped_school_data_df3.head()


# In[ ]:


bins=[0,585,615,645,675]
bin_names = ["< $585", "$585-615","$615-645","$645-675"]
grouped_school_data_df3["Spending ranges (Per Student)"] = pd.cut(per_stu_budget_grp, bins, labels=bin_names)

sch_spn_math_scores = grouped_school_data_df3.groupby(["Spending ranges (Per Student)"]).mean()["Average Math Score"]
sch_spn_reading_scores = grouped_school_data_df3.groupby(["Spending ranges (Per Student)"]).mean()["Average Reading Score"]
sch_spn_passing_math = grouped_school_data_df3.groupby(["Spending ranges (Per Student)"]).mean()["% Passing Math"]
sch_spn_passing_reading = grouped_school_data_df3.groupby(["Spending ranges (Per Student)"]).mean()["% Passing Reading"]
sch_spn_overall_passing_rate = (sch_spn_math_scores + sch_spn_reading_scores)/2

score_by_school_spn_df = pd.DataFrame({"Average Math Score":sch_spn_math_scores,
                                    "Average Reading Score":sch_spn_reading_scores,
                                    "% Passing Math":sch_spn_passing_math,
                                    "% Passing Reading":sch_spn_passing_reading,
                                    "% Overall Passing Rate": sch_spn_overall_passing_rate})

score_by_school_spn_df


# In[ ]:


grouped_school_data_df3["Scores by School Size"] = pd.cut(total_students_grp, bins, labels=size_names)

sch_spn_math_scores = grouped_school_data_df3.groupby(["Scores by School Size"]).mean()["Average Math Score"]
sch_spn_reading_scores = grouped_school_data_df3.groupby(["Scores by School Size"]).mean()["Average Reading Score"]
sch_spn_passing_math = grouped_school_data_df3.groupby(["Scores by School Size"]).mean()["% Passing Math"]
sch_spn_passing_reading = grouped_school_data_df3.groupby(["Scores by School Size"]).mean()["% Passing Reading"]
sch_spn_overall_passing_rate = (sch_spn_math_scores + sch_spn_reading_scores)/2

score_by_school_size_df = pd.DataFrame({"Average Math Score":sch_spn_math_scores,
                                    "Average Reading Score":sch_spn_reading_scores,
                                    "% Passing Math":sch_spn_passing_math,
                                    "% Passing Reading":sch_spn_passing_reading,
                                    "% Overall Passing Rate": sch_spn_overall_passing_rate})

score_by_school_size_df

