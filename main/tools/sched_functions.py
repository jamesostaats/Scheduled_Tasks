from datetime import datetime as dt
from datetime import timezone
from datetime import timedelta

# Test scheduled app
# Prints the current date and time to your console
def sched_marketo_loop():

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
    z=pd.DataFrame({'Message':'Hello, the schedule tracker app is running and the time is:' + y},index=['1'])
    z.to_sql('schedule_test', connection, index=False, if_exists='append')

    minutes_ago=dt.now(tz=timezone.utc) +timedelta(minutes=-9)
    marketo_run=pd.read_sql('''SELECT * FROM match_account_marketo_last_run''',connection)

    df=pd.read_sql('''SELECT * FROM schedule_task_status''',connection)
    df_marketo=df.loc[df['Task']=='Marketo Contact Match Loop']

    if (marketo_run['Last_Run'][0]<minutes_ago)&(df_marketo['Status'][0]!='Failed_Notified'):
        df.loc[df['Task']=='Marketo Contact Match Loop','Status']='Failed'
    
    if (marketo_run['Last_Run'][0]>minutes_ago):
        df.loc[df['Task']=='Marketo Contact Match Loop','Status']='Active'

    df_marketo=df.loc[df['Task']=='Marketo Contact Match Loop']
    if df_marketo['Status'][0]=='Failed':
        from email.mime.multipart import MIMEMultipart
        from email.mime.application import MIMEApplication
        from email.mime.text import MIMEText
        import smtplib

        #EMAIL
        def email_send(address):
            msg=MIMEMultipart()
            body_part=MIMEText(
            'Hello,\
            \n\
            \nThe Marketo Contact Match Loop has failed.\
            \n\
            \nCheck the status using this application:\
            \nhttp://lin2dv2nba75:3519/\
            \n\
            \nBest,\
            \nJames Staats\
            \nBusiness & Data Analyst\
            \nO:952.683.3149 | M:952.297.7889', 'plain')
            msg['Subject']='Dash Notification Email'
            msg['From']='James.Staats@chrobinson.com'
            #msg['To']='<James.Staats@chrobinson.com>'
            msg['To']='<'+address+'>'
            msg.attach(body_part)

            smtp_obj=smtplib.SMTP('mail.chrobinson.com',25)
            smtp_obj.sendmail(msg['From'],msg['To'],msg.as_string())
            smtp_obj.quit()
            return 
        
        email_send('william.fleurant@chrobinson.com')
        email_send('james.staats@chrobinson.com')
        email_send('Michael.Younghans@chrobinson.com')
        email_send('Amber.Hillman@chrobinson.com')
        email_send('Lynn.Wood@chrobinson.com')

        df.loc[df['Task']=='Marketo Contact Match Loop','Status']='Failed_Notified'
    
    df.to_sql('schedule_task_status', connection, index=False, if_exists='replace')

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