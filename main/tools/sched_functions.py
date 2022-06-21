from datetime import datetime as dt

# Test scheduled app
# Prints the current date and time to your console
def sched_test():

    import pandas as pd
    from sqlalchemy import create_engine

    #### Establishes connection to Postgres
    #POSTGRES_ADDRESS = '___the name of your VM - ex lin2dv2nba68_____'
    POSTGRES_ADDRESS = 'lin2dv2nba75'
    POSTGRES_PORT = 1550
    POSTGRES_USERNAME = 'postgres'
    POSTGRES_PASSWORD = 'postgres'
    POSTGRES_DBNAME = 'postgres'
    postgres_str = 'postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'.format(username=POSTGRES_USERNAME, password= POSTGRES_PASSWORD, ipaddress=POSTGRES_ADDRESS, port=POSTGRES_PORT, dbname=POSTGRES_DBNAME)
    connection = create_engine(postgres_str)

    x = dt.now()
    y=(' {}'.format(x))
    z=pd.DataFrame({'Message':'Hello, the app is running and the time is:' + y},index=['1'])
    z.to_sql('schedule_test', connection, index=False, if_exists='append')
    return

# Secondary test scheduled app
# Prints the current date/time along with a message
def sched_test_cron():
    import pandas as pd
    from sqlalchemy import create_engine

    #### Establishes connection to Postgres
    #POSTGRES_ADDRESS = '___the name of your VM - ex lin2dv2nba68_____'
    POSTGRES_ADDRESS = 'lin2dv2nba75'
    POSTGRES_PORT = 1550
    POSTGRES_USERNAME = 'postgres'
    POSTGRES_PASSWORD = 'postgres'
    POSTGRES_DBNAME = 'postgres'
    postgres_str = 'postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}'.format(username=POSTGRES_USERNAME, password= POSTGRES_PASSWORD, ipaddress=POSTGRES_ADDRESS, port=POSTGRES_PORT, dbname=POSTGRES_DBNAME)
    connection = create_engine(postgres_str)

    x = dt.now()
    y=(' {}'.format(x))
    z=pd.DataFrame({'Message':'Help, there is no end in sight...the time is:' + y},index=['1'])
    z.to_sql('schedule_test', connection, index=False, if_exists='append')
    return