import  urllib2
import pandas as pd
import os, datetime, glob, re

def reIndex(path):
    indexMap = {'25':'2', '05':'3', '24':'1', '23':'6', '26':'7', '06':'4', '27':'5', '07':'8', '11':'9', '17':'14', '02':'24', '04':'25', '09':'20', '10':'21', '14':'11', '13':'10', '16':'13', '15':'12', '18':'15', '01':'22', '21':'17', '19':'16', '08':'19', '22':'18', '03':'23'}
    files = glob.glob("*.csv")
    for filename in files:
        id = filename[7:9]
        try:
            os.rename(filename, "_"+filename[0:7]+indexMap[id]+filename[9:])
        except KeyError:
            pass
    for filename in files:
        try:
            os.remove(filename)
        except OSError:
            pass

#index is string key value in frames dict

def weekInYearMaxVHI(frames, index, year):
    df = frames[index]
    dfYear = df.loc[df['year']==year]
    print "Week with max VHI for index #"+str(index)
    print dfYear.loc[dfYear['VHI'].idxmax()]

def weekInYearMinVHI(frames, index, year):
    df = frames[index]
    dfYear = df.loc[df['year']==year]
    print "Week with min VHI for index #"+str(index)
    print dfYear.loc[dfYear['VHI'].idxmin()]

def getYearsWithExtraDryAreaMoreThan(frames, index, criticalArea):
    resultYears = []
    for year in range(1981, 2017):
        areaYearList = listParameterForYear(frames, index, year, 'Area_VHI_LESS_15')
        for area in areaYearList:
            if float(area)>criticalArea:
                print area
                resultYears.append(year)
                break;
    return resultYears

def getYearsWithDryAreaMoreThan(frames, index, criticalArea):
    resultYears = []
    for year in range(1981, 2017):
        areaYearList = listParameterForYear(frames, index, year, 'Area_VHI_LESS_35')
        for area in areaYearList:
            if float(area)>criticalArea:
                print area
                resultYears.append(year)
                break;
    return resultYears

#parameter is column name string
def listParameterForYear(frames, index, year, parameter):
    df = frames[index]
    dfYear = df.loc[df['year']==year]
    return dfYear[parameter].map(lambda x: '%2.2f' % x).tolist()

def listParameterForAllYears(frames, index, parameter):
    parameterList = []
    for year in range(1981, 2017):
        parameterList.extend(listParameterForYear(frames, index, year, parameter))
    return parameterList

def listVHIForAllYears(frames, index):
    VHIList = []
    for year in range(1981, 2017):
        VHIList.extend(listParameterForYear(frames, index, year, 'VHI'))
    print VHIList

def getDataByIndex(index):
    strIndex = str(index)
    if index<10:
        strIndex = "0"+strIndex
    url="http://www.star.nesdis.noaa.gov/smcd/emb/vci/gvix/G04/ts_L1/ByProvince/Mean/L1_Mean_UKR.R"+strIndex+".txt"
    vhi_url = urllib2.urlopen(url)
    time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    out = open('vhi_id_'+strIndex+'_'+time[:19]+'.csv','wb')
    out.write(vhi_url.read())
    out.close()
    print "VHI "+str(index)+" is downloaded..."

def getAll():
    for i in range(27):
        getDataByIndex(i+1)
        print "Done.\n"

def readCSVtoFrames(path):
    os.chdir(path)
    files = glob.glob("*.csv")
    if len(files)==0:
        return;
    frames = {}
    for file in files:
        df = pd.read_csv(path+file,index_col=False, header=1)
        new_columns = df.columns.values
        for i in range(0, len(df.columns.values)):
            new_columns[i] = re.sub('[^A-Za-z0-9_]+', '', new_columns[i])
        df.columns = new_columns
        index = file[8:10]
        if index[1]=='_':
            index = index[:-1]
        frames[index] = df
    return frames

try:
    menuChoice=int(raw_input('1. Download data by index\n2. Get all \n3. Read to frame\n'))
except ValueError:
    print "Not a number"

if menuChoice==1:
    try:
        index=int(raw_input('Enter area index: '))
        getDataByIndex(index)
    except ValueError:
        print "Not a number"
elif menuChoice==2:
    getAll()
    reIndex("./")
else:
    path=raw_input('Enter path to CSV files: ')
    frames = readCSVtoFrames(path)
    for i in range(len(frames)):
        weekInYearMaxVHI(frames, str(i+1), 1990)
        weekInYearMinVHI(frames, str(i+1), 1990)
        print getYearsWithExtraDryAreaMoreThan(frames, str(25) , 55)
        #listVHIForAllYears(frames, str(i+1))
        #print
        print "\n"

raw_input()

