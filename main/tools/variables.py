import pandas as pd

# STYLE DICTIONARIES FOR INPUTS
# Hidden will keep an element from showing up
hidden = {'display':'none'}
# Visible will make it show up - effectively overrides the display and sets a small margin around the item
standard = {'margin':5}
# Used for Divs - will center content in the middle of the page
divstyle = {
    'display':'flex'
    ,'justify-content':'center'
    ,'margin':5
}



sampledata = pd.DataFrame({
    'Request':[1,2,3,4]
    ,'Date':['8/1/2021','8/1/2021','8/1/2021','8/1/2021']
    ,'C-Code':['C1','C2','C3','C4']
})