"""
Written by:
    Aviv Shisman
"""

# import
import mysql.connector
import datetime

# logging to db
data_base = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="ecologi"
)

# global
office_ids = []

def activate():

  # get newest data
  cursor = data_base.cursor()
  cursor.execute("SELECT * FROM occupancystatistic")
  occupancy_table_full = cursor.fetchall()

  # filter the data and adapt it to our format
  data = []
  for elm in occupancy_table_full:
    update_office_Ids(elm[6],0)           # update office list if we don't have this office
    time,iso_date = extract_time(elm[7])
    data.append((elm[6],time,iso_date,elm[1]))   # we only want the zone/office, time,date,userId

  # get occupancy from data
  data = list(dict.fromkeys(data)) # remove duplicates (same hour couple of times)
  occupancy = get_occupancy(data)


  # write to file...
  update_office_Ids(0,1)
  update_data_table(occupancy)

  return


'''
update data table
'''
def update_data_table(data):
  occ_file = open("data.csv", 'w')
  occ_file.write(",".join(("office id", "week", "day", "hour", "workers","year" + "\n")))

  for office in data:
    for ent in office:
      id = ent[0]
      time = ent[1]
      year = ent[2][0]
      week = ent[2][1]
      day = ent[2][2]
      count = office[ent]
      occ_file.write(",".join((str(id), str(week), str(day), str(time), str(count),str(year) + "\n")))

  occ_file.close()

  return

'''
update office ids each run to newest
'''
def update_office_Ids(new_id,flag):
  if flag ==0 and new_id not in office_ids:
    office_ids.append(new_id)

  if flag == 1:
    office_ids_file = open("offices.txt", 'w')
    for id in office_ids:
      office_ids_file.write(str(id)+'\n')
    office_ids_file.close()

'''
extract our time measurements
'''
def extract_time(elm):
  date, time_now = elm.strftime("%d/%m/%Y %H:%M:%S").split(' ')
  temp = date.split('/')
  time_now = int(time_now.split(':')[0])
  iso_date = datetime.date(int(temp[2]), int(temp[1]), int(temp[0])).isocalendar()

  return time_now,iso_date

'''
get occupancy from data
'''
def get_occupancy(data):

  # arrange data to offices
  offices_data =[]
  for i,id in enumerate(office_ids):
    temp = []
    for elm in data:
      if elm[0] == id:
        temp.append(elm)
    offices_data.append(temp)

  # get occupancy from data
  occupancy =[]
  for office in offices_data:
    office_occupancy={}
    for entry in office:
      curr = (entry[0],entry[1],entry[2])
      if not curr in office_occupancy:
        office_occupancy[curr] = 1
      else:
        office_occupancy[curr] +=1

    occupancy.append(office_occupancy)


  return occupancy

