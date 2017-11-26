def database():
	#Extract content from database
	database = []
    with open("../Data/database/points yes-skin no-skew.csv") as f:
        #Extract name and points from database
        lis=[line[:-1].split(',') for line in f]        
        for i in lis:
            name=i[0]
            points=i[1:]
            points=[[int(x) for x in p.split()] for p in points]
            database.append([name,points])
    return database

def train_database():
	pass