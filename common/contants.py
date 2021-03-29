import os
base_dir = os.path.dirname(os.path.dirname(__file__))

utils_dir = os.path.join(base_dir,'data/utils.yaml')
env_dir = os.path.join(base_dir,'data/env.yaml')



# 健康申報api
questionnaire_dir = os.path.join(base_dir,'data/questionnaire/questionnaire.yaml')

# 健康申報cases
test_questionnaire_dir = os.path.join(base_dir,'data/cases/test_questionnaire/test_questionnaire.yaml')

# 問卷api
quarter_dir = os.path.join(base_dir,'data/quarter/quarter.yaml')
# 問卷cases
test_quarter_dir = os.path.join(base_dir,'data/cases/test_quarter/test_quarter.yaml')

test_uat_fir_dir = os.path.join(base_dir,'data/cases/test_quarter/test_uat_fir.yaml')

test_prod_dir = os.path.join(base_dir,'data/cases/test_quarter/test_prod.yaml')

# 日程api
schedule_dir = os.path.join(base_dir,'data/schedule/schedule.yaml')

# 日程cases
test_schedule_dir = os.path.join(base_dir,'data/cases/test_schedule/test_schedule.yaml')

# 問卷api
class_timetable_dir = os.path.join(base_dir,'data/class_timetable/class_timetable.yaml')
# 問卷cases
test_class_timetable_dir = os.path.join(base_dir,'data/cases/test_class_timetable/test_class_timetable.yaml')








