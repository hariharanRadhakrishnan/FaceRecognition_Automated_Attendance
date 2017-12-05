def database():
    #Extract content from database
    templates = []
    with open("C:/Users/sande/Desktop/CV/sandeep/Data/database/skewskinpointsnew.csv") as f:
        #Extract name and points from database
        lis=[line[:-1].split(',') for line in f]        
        for i in lis:
            name=i[0]
            points=i[1:]
            points=[[int(x) for x in p.split()] for p in points]
            templates.append([name,points])
    return templates

def train_database():
	pass