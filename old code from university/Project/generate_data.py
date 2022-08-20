"""
 Workers:
 - 15 workers
 Patterns:
 - 5 workers do'nt come on 3rd day ever
 - all workers (15) are not in the office at 18 at monday
 - 10 workers do'nt come on 5th day on 10hour
 - the office close on saturday
 """

def activate():
    details = open("data.csv", "w")

    # get offices.txt id's
    office_ids = []
    office_ids_file = open("offices.txt", 'r')
    for line in office_ids_file.readlines():
        office_ids.append(line.rstrip('\n'))
    office_ids_file.close()

    week = [i for i in range(1, 53)]
    days = [1, 2, 3, 4, 5, 6, 7]
    hours = [i for i in range(8,21)]
    years =  [2018,2019]

    details.write(",".join(("office id","week", "day", "hour", "workers","year"+ "\n")))

    for i in office_ids:
        for y in years:
            for w in week:
                for d in days:
                    for h in hours:
                            workers = 15
                            if d == 3:
                                workers = 10
                            elif d == 2 and h == 18:
                                workers = 0
                            elif d == 5 and h == 10:
                                workers = 5
                            elif d == 7:
                                workers = 0

                            #workers += i

                            details.write(",".join((str(i),str(w), str(d), str(h), str(workers),str(y)+"\n")))
    details.close()
