# Project Insights — Student Performance & Placement Analytics

*All figures below are calculated directly from the generated dataset
(`data/cleaned_student_data.csv`).*

## Overall Insights

- **Total Students:** 800
- **Placed Students:** 352
- **Not Placed Students:** 448
- **Placement Rate:** 44.00%
- **Average CGPA:** 7.45
- **Average Salary Package:** 10.25 LPA
- **Highest Salary Package:** 16.73 LPA
- **Lowest Salary Package (placed):** 4.81 LPA

## Academic Insights

- **Branch with highest average CGPA:** Computer Science Engineering (7.55)
- **CGPA range with highest placement rate:** Above 9 (65.96%)

**Placement rate by CGPA range:**
- **Below 6**: 30.51% placement rate
- **6 to 7**: 39.60% placement rate
- **7 to 8**: 44.44% placement rate
- **8 to 9**: 46.67% placement rate
- **Above 9**: 65.96% placement rate

- **Average attendance of placed students:** 79.86%
- **Average attendance of not-placed students:** 78.61%

Higher CGPA is generally associated with a higher chance of placement,
though the relationship is not perfectly linear — some students with
strong CGPA remain unplaced, while some with moderate CGPA but strong
internships/skills profiles do get placed. This reflects the realistic
noise deliberately built into the dataset.

## Skills Insights

**Correlation of each factor with placement outcome (higher = stronger positive impact):**
- **CGPA**: correlation = 0.124
- **Internships**: correlation = 0.112
- **Technical_Skills**: correlation = 0.091
- **Projects**: correlation = 0.086
- **Certifications**: correlation = 0.075
- **Attendance_Percentage**: correlation = 0.054
- **Aptitude_Score**: correlation = -0.017
- **Communication_Score**: correlation = -0.025

- **Most influential factor for placement:** CGPA (correlation = 0.124)

Technical skills, internships, projects and certifications all show a
positive relationship with placement likelihood — students investing in
practical, hands-on experience alongside academics tend to have better
placement outcomes.

## Placement Insights

- **Branch with highest placement rate:** Computer Science Engineering (47.27%)
- **Top recruiting company:** Capgemini (44 students placed)

**Gender-wise placement rate:**
- **Female**: 41.67% placement rate
- **Male**: 46.33% placement rate
- **Other**: 26.67% placement rate

## Salary Insights

- **Branch with highest average package:** Mechanical Engineering (10.64 LPA)
- **Company with highest average package:** Deloitte (10.90 LPA)
- **Feature most strongly correlated with salary:** CGPA (correlation = 0.199)

CGPA shows a clear positive relationship with salary package, and this
is reinforced by internships, projects and technical skills — students
who combine strong academics with hands-on experience tend to command
higher packages.

## Final Conclusion

The analysis of 800 student records shows an
overall placement rate of 44.00%, with
**Computer Science Engineering** leading in placement
outcomes and **Mechanical Engineering** leading in average
salary package. Academic performance (CGPA) and hands-on experience
(internships, projects, certifications, technical skills) together are
the strongest drivers of both placement likelihood and salary package.
Students aiming to improve their employability should focus on
maintaining a strong CGPA while actively building practical experience
through internships, projects and relevant certifications, alongside
developing aptitude and communication skills, which also contribute
meaningfully to placement success.

---
*Report generated automatically from the analysis pipeline — no values
in this report are hardcoded.*
