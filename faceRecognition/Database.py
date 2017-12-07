def database(skew,laugh):
    #Extract content from database
    templates = []
    file_name =""
    if(skew=="straight"):
        if(laugh=="laugh"):
            file_name = "laughdb.csv"
        else:
            file_name = "normaldb.csv"
    elif(skew=="left"):
        file_name="leftdb.csv"
    elif(skew=="right"):
        file_name="rightdb.csv"

    with open("C:/Users/sande/Desktop/CV/sandeep/Data/database/"+file_name) as f:
        #Extract name and points from database
        lis=[line[:-1].split(',') for line in f]        
        for i in lis:
            name=i[0]
            points=i[1:]
            points=[[int(x) for x in p.split()] for p in points]
            templates.append([name,points])
    return templates

