def branchreporting (file):

    import pandas as pd
    import pymssql
    import os
    
    server,user,password='BranchReporting','CHR\STAAJAM','#Itspoolworld22'

    with open(file+".sql","r") as f:
        query=f.read()    
    with pymssql.connect(server, user, password) as conn:
        result=pd.read_sql(query, conn)
    f.close()
    
    return result;


branchreporting('testsql.sql')