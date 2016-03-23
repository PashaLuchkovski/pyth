import urllib2
import os
import pandas as pd
import re

#GetDataByIndex
def reIndex(index):
    IndexDictionary = {1:24, 2:25, 3:5, 4:6, 5:27, 6:23, 7:26, 8:7, 9:11, 10:13, 11:14, 12:15, 13:16, 14:17, 15:18, 16:19, 17:21, 18:22, 19:8, 20:9, 21:10, 22:1, 23:3, 24:2, 25:4}
    return IndexDictionary[index]


def getDataByIndex(index):
    index = reIndex(index)
    strIndex = str(index)
    if index<10:
        strIndex = "0"+strIndex
    url="http://www.star.nesdis.noaa.gov/smcd/emb/vci/gvix/G04/ts_L1/ByProvince/Mean/L1_Mean_UKR.R"+strIndex+".txt"
    vhi_url = urllib2.urlopen(url)
    out = open('/Users/pashaluchkovski/Documents/Study/Coding/Python/pyth/f.csv', 'wb')
    out.write(vhi_url.read())
    out.close()

    print "VHI " + strIndex + " is downloaded..."

def readDataToFrame(path):
    os.chdir(path)
    df = pd.read_csv('f.csv', header = 1)
    #print list(df.columns.values)
    #print df[:3]
    frame_columns = df.columns.values
    for i in range(0, len(df.columns.values)):
        frame_columns[i] = re.sub('[^A-Za-z0-9]+', '', frame_columns[i])
    df.columns = frame_columns
    df = df.loc[(df['SMN'] != -1)]
    return df

def getYearVHI(year, df, district):
    #yearVHI = df[df['year'] == year]
    yearVHI = df.loc[(df['year']==year)]
    maxYearVHI = max(yearVHI['VHI'])
    minYearVHI = min(yearVHI['VHI'])
    print "Maximum year VHI in " + str(district) + " district in " + str(year) + ": " + str(maxYearVHI)
    print "Minimum year VHI in " + str(district) + " district in " + str(year) + ": " + str(minYearVHI)

def extraDryYears(df, areaPercent):
    extraDrySeasons = df.loc[df['AreaVHILESS15'] > areaPercent]
    #print list(extraDrySeasons['year'])
    extraDryYears_mass = []
    for year in extraDrySeasons['year']:
        #print str(year) + ", "
        if year not in extraDryYears_mass:
            extraDryYears_mass.append(year)
    return extraDryYears_mass

def DryYears(df, areaPercent):
    DrySeasons = df.loc[df['AreaVHILESS35'] > areaPercent]
    #print list(extraDrySeasons['year'])
    DryYears_mass = []
    for year in DrySeasons['year']:
        #print str(year) + ", "
        if year not in DryYears_mass:
            DryYears_mass.append(year)
    return DryYears_mass


def getMeanVHIyears(df):
    tmp = df.loc[(df['week'] >= 17)]
    tmp = df.loc[(df['week'] <= 28)]
    arr = df['VHI'].mean()
    dd = tmp.loc[(tmp['VHI'] <= arr)]
    Years_mass = []
    for year in dd['year']:
        #print str(year) + ", "
        if year not in Years_mass:
            Years_mass.append(year)
    print "Years with less VHI than mean"
    print list(Years_mass)

##################################_______________######################################

def main_func():
    print '\n\n\n'
    district = int(raw_input('Enter district ID: ' ))
    path = "/Users/pashaluchkovski/Documents/Study/Coding/Python/pyth/"
    getDataByIndex(district)
    DataFrame = readDataToFrame(path)
    year = 2012
    AreaPercent = 23
    
    yearVHI = getYearVHI(year, DataFrame, district)
    print "######################################################"
    print "Extra dry years, " + str(AreaPercent) + "% of area in " + str(district) + " district: ", list(extraDryYears(DataFrame, AreaPercent))
    print "######################################################"
    print "Dry years, " + str(AreaPercent) + "% of area in " + str(district) + " district: " , list(DryYears(DataFrame, AreaPercent))
    print "######################################################"
    getMeanVHIyears(DataFrame)
    #print list(DataFrame.columns.values)
    #print DataFrame[:100]

main_func()

