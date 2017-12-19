def database(skew,laugh,gr):
    #Extract content from database
    templates = []
    file_name =""
    if(skew=="straight"):
        if(laugh=="laugh"):
            file_name = "LAUGH_DB.csv"
        else:
            file_name = "NORMAL_DB.csv"
    elif(skew=="left"):
        file_name="LEFT_DB.csv"
    elif(skew=="right"):
        file_name="RIGHT_DB.csv"
    # file_name = "skewskinpointsnew.csv"

    if(gr=="group"):
        with open("C:/Users/sande/Desktop/CV/sandeep/Data/database/group/"+file_name) as f:
            #Extract name and points from database
            lis=[line[:-1].split(',') for line in f]
            for i in lis:
                name=i[0]
                points=i[1:]
                points=[[int(x) for x in p.split()] for p in points]
                templates.append([name,points])
    else:
        with open("C:/Users/sande/Desktop/CV/sandeep/Data/database/"+file_name) as f:
            #Extract name and points from database
            lis=[line[:-1].split(',') for line in f]
            for i in lis:
                name=i[0]
                points=i[1:]
                points=[[int(x) for x in p.split()] for p in points]
                templates.append([name,points])
    
    return templates

