# Data Cleaning

import xml.etree.ElementTree as ET
import csv

###################################
### THINGS THAT YOU SHOULD CHANGE #
###################################

# Start

file_name = 'final_2014.xml'
consult_filename = 'consult.csv'
img_filename = 'img_14.csv'
# lib_path = '/'
final_filename = 'final.csv'

# End


#################################
### Get Variable list from .xml #
#################################

xmlTree = ET.parse(file_name)
elemList = []

# This part is for you to check all
# the elements in this file.

# Start
for elem in xmlTree.iter():
  elemList.append(elem.tag)

# remove duplicities
elemList = list(set(elemList))
print(elemList)

# End

#################################
####  Extract Data From .xml ####
#################################

# extract consulting information

tree = ET.parse(file_name)
root = tree.getroot()


def search_insert(name, records, info_list):
    """
    Usage: search one 'name' in a centain part
           of the .xml records.
           Add the corresponding attributes into
           the info_list.
    """
    current = records.find(name)
    if current == None:
        info_list.append('')
    else:
        temp = records.find(name).text
        if temp == None:
            temp = ''
        info_list.append(temp)


# edit namelist to meet your requirement
namelist = ['noDr', 'ma', 'cw', 'hma', 'he', 'vb', 'irmaWithin8a',
            'irmaGreaterThan8a', 'heWithin1DD', 'heGreaterThan2DD', 'heWithin2DD',
            'hmaGreaterThan2a', 'hmaWithin2a', 'irma', 'nvfp',
            'prhvh', 'prp', 'fp']

# these are some other information that we are interested
otherlist = ['cataract', 'glaucoma', 'maculopathy', 'occlusion', 'otherReferrable']

# Title list would be used as the first line when writing the .csv
Title = ['id', 'right_noDr', 'right_ma', 'right_cw', 'right_hma', 'right_he', 'right_vb',
         'right_irmaWithin8a', 'right_irmaGreaterThan8a',
         'right_heWithin1DD', 'right_heGreaterThan2DD', 'right_heWithin2DD',
         'right_hmaGreaterThan2a', 'right_hmaWithin2a', 'right_irma', 'right_nvfp',
         'right_prhvh', 'right_prp', 'right_fp', 'left_noDr', 'left_ma', 'left_cw',
         'left_hma', 'left_he', 'left_vb', 'left_irmaWithin8a', 'left_irmaGreaterThan8a',
         'left_heWithin1DD', 'left_heGreaterThan2DD',
         'left_heWithin2DD', 'left_hmaGreaterThan2a', 'left_hmaWithin2a', 'left_irma', 'left_nvfp',
         'left_prhvh', 'left_prp', 'left_fp', 'imageQualityFactor', 'imageQuality',
         'cataract', 'glaucoma', 'maculopathy', 'occlusion', 'otherReferrable']

# first .csv for the 'consulting' message in the .xml
with open(consult_filename, 'w', newline='') as r:
    writer = csv.writer(r)
    writer.writerow(Title)

    for case in tree.iter(tag='case'):
        info_list = []
        # use id as an unique key
        id = case.attrib.get('id')
        info_list.append(id)
        for records in case.iter(tag='right'):
            for name in namelist:
                search_insert(name, records, info_list)
        for records in case.iter(tag='left'):
            for name in namelist:
                search_insert(name, records, info_list)

        # Note: ElementTree uses 'ambiguous' matching methods
        # Therefore longer name should be put before the shorter ones,
        # if they share the same beginning

        for imageQF in case.iter(tag='imageQualityFactor'):
            imageQF_temp = imageQF.text
            info_list.append(imageQF_temp)
        for imageQ in case.iter(tag='imageQuality'):
            imageQ_temp = imageQ.text
            info_list.append(imageQ_temp)
        for others in case.iter(tag='otherConditions'):
            for name in otherlist:
                search_insert(name, others, info_list)
        writer.writerow(info_list)


#  Format:
#  id path1 type1 path2 type2 ...

###################################
### THINGS THAT YOU SHOULD CHANGE #
###################################

# Start

# 1. Set title of the img file
# MUST BE SET !
# 2. Open the file, double click on random cell
# and save the it again before running the following script.

Title = ['id', 'type1', 'path1', 'type2', 'path2',
         'type3', 'path3', 'type4', 'path4',
         'type5', 'path5', 'type6', 'path6',
         'type7', 'path7', 'type8', 'path8', 'omit']

# dimension: set as the same as the maximum
# number of images in one patient's profile

dimension = 8

# End

with open(img_filename, 'w', newline='') as r:
    writer = csv.writer(r)
    writer.writerow(Title)

    for case in tree.iter(tag='case'):
        info_list = []
        id = case.attrib.get('id')
        info_list.append(id)
        for image in case.iter(tag='image'):
            type_temp = image.attrib.get('type')
            info_list.append(type_temp)
            for path in image.iter(tag='path'):
                path_temp = path.text
                info_list.append(path_temp)

        writer.writerow(info_list)

# Extracting other information

"""
namelist = ["age", "ethnicity", "gender"]
Title = ["id", "age", "ethnicity", "gender"]


def search_insert(name, records, info_list):
    current = records.find(name)
    if current == None:
        info_list.append('')
    else:
        temp = records.find(name).text
        if temp == None:
            temp = ''
        info_list.append(temp)

with open('2014_patient.csv', 'w', newline='') as r:
    writer = csv.writer(r)
    writer.writerow(Title)
    for case in tree.iter(tag='case'):
        info_list = []
        id = case.attrib.get('id')
        info_list.append(id)
        for patient in case.iter(tag='patient'):
            for name in namelist:
                search_insert(name, patient, info_list)
        writer.writerow(info_list)

    import xml.etree.ElementTree as ET
    import csv

    tree = ET.parse('final_2014.xml')
    root = tree.getroot()


    def search_insert(name, records, info_list):
        current = records.find(name)
        if current == None:
            info_list.append('')
            return

        temp = records.find(name).text
        if temp == None:
            temp = ''
        info_list.append(temp)


    namelist = ['siteIdentifier', 'encounterDate', 'pupilDilation', 'yearsWithDiabetes',
                'insulinDependent', 'insulinDependDuration', 'lastEyeExam', 'recentBloodTest',
                'medications', 'hemoglobinA1c', 'cholesterol', 'triglycerides', 'hypertension',
                'historyGlaucoma', 'subjectiveDiabeticControl', 'visualAcuityRight',
                'visualAcuityLeft', 'iopRight', 'iopLeft']

    Title = ['id', 'siteIdentifier', 'encounterDate', 'pupilDilation', 'yearsWithDiabetes',
             'insulinDependent', 'insulinDependDuration', 'lastEyeExam', 'recentBloodTest',
             'medications', 'hemoglobinA1c', 'cholesterol', 'triglycerides', 'hypertension',
             'historyGlaucoma', 'subjectiveDiabeticControl', 'visualAcuityRight',
             'visualAcuityLeft', 'iopRight', 'iopLeft']

    with open('2014_cldtl.csv', 'w', newline='') as r:
        writer = csv.writer(r)
        writer.writerow(Title)

        for case in tree.iter(tag='case'):
            info_list = []
            id = case.attrib.get('id')
            info_list.append(id)
            for records in case.iter(tag='clinicalDetails'):
                for name in namelist:
                    search_insert(name, records, info_list)
            writer.writerow(info_list)
"""

#################################
####     Combine  Data     ######
#################################

import pandas as pd


"""
Pandas can only read in regular rectangular shape dataset, 
please check the .csv file to add 'headers'.
In this case, that is 'typek' or 'pathk'
"""


##############################
##### check image.csv file ###
##############################

# Check if the 'img_filename' file can be read in

# read in
image14 = pd.read_csv(img_filename)

"""
You should also check how many columns do we need. 
For data14, we need 16(8 paths, 8 types) + 1 (id) + 1 (pandas id)
"""

image14 = image14.iloc[:, 0:17]
consult14 = pd.read_csv(consult_filename)
df2014 = pd.merge(consult14, image14, how='left', on='id')

#################################
####     Wide to Long     #######
#################################


def return_sub(path, type):
    # combine consult data and image data together
    # for path(k) type(k)
    var_list = [path, type, 'id', 'right_noDr', 'right_ma',
                'right_cw', 'right_hma', 'right_he', 'right_vb',
                'right_irmaWithin8a', 'right_heWithin1DD', 'right_irmaGreaterThan8a',
                'right_heGreaterThan2DD', 'right_heWithin2DD', 'right_hmaGreaterThan2a',
                'right_hmaWithin2a', 'right_irma', 'right_nvfp', 'right_prhvh',
                'right_prp', 'right_fp', 'left_noDr', 'left_ma', 'left_cw', 'left_hma',
                'left_he', 'left_vb', 'left_irmaWithin8a', 'left_heWithin1DD',
                'left_heGreaterThan2DD', 'left_heWithin2DD', 'left_hmaGreaterThan2a',
                'left_hmaWithin2a', 'left_irma', 'left_nvfp', 'left_prhvh', 'left_prp',
                'left_fp', 'imageQualityFactor', 'imageQuality', 'cataract', 'glaucoma',
                'maculopathy', 'occlusion', 'otherReferrable', 'left_irmaGreaterThan8a']

    df_temp = df2014.loc[(df2014[type] == 'Right Field 1') | (df2014[type] == 'Right Field 2') |
                         (df2014[type] == 'Right Field 3') | (df2014[type] == 'Right External') |
                         (df2014[type] == 'Left Field 1') | (df2014[type] == 'Left Field 2') |
                         (df2014[type] == 'Left Field 3') | (df2014[type] == 'Left External'), var_list]
    df_temp = df_temp.rename(index=str, columns={path: 'path', type: 'type'})
    return df_temp

# combine id, path, type and other variables together
df = return_sub('path1', 'type1')
for i in range(2, dimension+1):
    path_temp = 'path' + str(i)
    type_temp = 'type' + str(i)
    temp = return_sub(path_temp, type_temp)
    df = pd.concat([df, temp])


################################
####   Add  Dr_Grade     #######
################################

# refer confluence for the rules

n, m = df.shape

right_grade = [None] * n
left_grade = [None] * n

for i in range(n):
    print("proceed: " + str(i))
    if df.right_nvfp[i] == 'yes' or df.right_prhvh[i] == 'yes':
        right_grade[i] = 4
        continue

    if df.right_hmaGreaterThan2a[i] == 'yes' or \
                df.right_vb[i] == 'yes':
        right_grade[i] = 3
        continue

    if df.right_cw[i] == 'yes' or df.right_hmaWithin2a[i] == 'yes' or df.right_irma[i] == 'yes' or \
                    df.right_irmaWithin8a[i] == 'yes' or df.right_heWithin1DD[i] == 'yes' or \
                    df.right_heWithin2DD[i] == 'yes' or \
                    df.right_heGreaterThan2DD[i] == 'yes':
        right_grade[i] = 2

    if df.right_ma[i] == 'yes':
        right_grade[i] = 1
        continue

    if df.right_noDr[i] == 'yes':
        right_grade[i] = 0
        continue

    if df.right_irmaGreaterThan8a[i] == 'yes':
        right_grade[i] = 3
        continue

for i in range(n):
    print("proceed: " + str(i))
    if df.left_nvfp[i] == 'yes' or df.left_prhvh[i] == 'yes':
        left_grade[i] = 4
        continue

    if df.left_hmaGreaterThan2a[i] == 'yes' or \
                    df.left_vb[i] == 'yes':
        left_grade[i] = 3
        continue

    if df.left_cw[i] == 'yes' or df.left_hmaWithin2a[i] == 'yes' or df.left_irma[i] == 'yes' or \
                        df.left_irmaWithin8a[i] == 'yes' or df.left_heWithin1DD[i] == 'yes' or \
                        df.left_heWithin2DD[i] == 'yes' or \
                        df.left_heGreaterThan2DD[i] == 'yes':
        left_grade[i] = 2

    if df.left_ma[i] == 'yes':
        left_grade[i] = 1
        continue

    if df.left_noDr[i] == 'yes':
        left_grade[i] = 0
        continue

    if df.left_irmaGreaterThan8a[i] == 'yes':
        left_grade[i] = 3
        continue

df['right_grade'] = right_grade
df['left_grade'] = left_grade

# df.to_csv(lib_path+'df.csv')
# (recommended)


################################
####   Combine irma/he/hma   ###
################################

# irma/he/hma are categorical variables
# create new variables to represent each level

# df = pd.read_csv("df2013.csv")

n, m = df.shape
irmar = [None] * n
irmaf = [None] * n
her = [None] * n
hef = [None] * n
hmar = [None] * n
hmaf = [None] * n

for i in range(n):
    if df.right_irmaGreaterThan8a[i] == 'yes':
        irmar[i] = 2
    elif df.right_irmaWithin8a[i] == 'yes':
        irmar[i] = 1
    elif df.right_irma[i] != 'cannot grade':
        irmar[i] = 0
    else:
        irmar[i] = -1

    if df.left_irmaGreaterThan8a[i] == 'yes':
        irmaf[i] = 2
    elif df.left_irmaWithin8a[i] == 'yes':
        irmaf[i] = 1
    elif df.left_irma[i] != 'cannot grade':
        irmaf[i] = 0
    else:
        irmaf[i] = -1

    if df.right_heGreaterThan2DD[i] == 'yes':
        her[i] = 3
    elif df.right_heWithin2DD[i] == 'yes':
        her[i] = 2
    elif df.right_heWithin1DD[i] == 'yes':
        her[i] = 1
    elif df.right_he[i] != 'cannot grade':
        her[i] = 0
    else:
        her[i] = -1

    if df.left_heGreaterThan2DD[i] == 'yes':
        hef[i] = 3
    elif df.left_heWithin2DD[i] == 'yes':
        hef[i] = 2
    elif df.left_heWithin1DD[i] == 'yes':
        hef[i] = 1
    elif df.left_he[i] != 'cannot grade':
        hef[i] = 0
    else:
        hef[i] = -1

    if df.right_hmaGreaterThan2a[i] == 'yes':
        hmar[i] = 2
    elif df.right_hmaWithin2a[i] == 'yes':
        hmar[i] = 1
    elif df.right_hma[i] != 'cannot grade':
        hmar[i] = 0
    else:
        hmar[i] = -1

    if df.left_hmaGreaterThan2a[i] == 'yes':
        hmaf[i] = 2
    elif df.left_hmaWithin2a[i] == 'yes':
        hmaf[i] = 1
    elif df.left_hma[i] != 'cannot grade':
        hmaf[i] = 0
    else:
        hmaf[i] = -1


df['right_irma_final'] = irmar
df['left_irma_final'] = irmaf
df['right_he_final'] = her
df['left_he_final'] = hef
df['right_hma_final'] = hmar
df['left_hma_final'] = hmaf

# if -1 -- delete the line
df = df.loc[(df.right_irma_final != -1) & (df.left_irma_final != -1) &
            (df.right_he_final != -1) & (df.left_he_final != -1) &
            (df.right_hma_final != -1) & (df.right_hma_final != -1)]

# if "cannot grade" -- delete the line
df = df.loc[(-df['right_noDr'].isin(["cannot grade"])) & (-df['left_noDr'].isin(["cannot grade"])) &
        (-df['right_ma'].isin(["cannot grade"])) & (-df['left_ma'].isin(["cannot grade"])) &
        (-df['right_cw'].isin(["cannot grade"])) & (-df['left_cw'].isin(["cannot grade"])) &
        (-df['right_vb'].isin(["cannot grade"])) & (-df['left_vb'].isin(["cannot grade"])) &
        (-df['right_nvfp'].isin(["cannot grade"])) & (-df['left_nvfp'].isin(["cannot grade"])) &
        (-df['right_prhvh'].isin(["cannot grade"])) & (-df['left_prhvh'].isin(["cannot grade"])) &
        (-df['right_prp'].isin(["cannot grade"])) & (-df['left_prp'].isin(["cannot grade"])) &
        (-df['right_fp'].isin(["cannot grade"])) & (-df['left_fp'].isin(["cannot grade"]))]


################################
####   Seperate Right/Left   ###
################################

# 'Right Field #' data are supposed not to have 'left' features
# Delete left features contained by right data and vice versa.

var_listR = ['path', 'type', 'id', 'right_noDr', 'right_ma',
             'right_cw', 'right_vb', 'right_nvfp', 'right_prhvh',
             'right_prp', 'right_fp', 'imageQualityFactor', 'imageQuality',
             'cataract', 'glaucoma', 'maculopathy', 'occlusion',
             'otherReferrable', 'right_irma_final', 'right_he_final', 'right_hma_final',
             'right_grade']

var_listL = ['path', 'type', 'id', 'left_noDr', 'left_ma',
             'left_cw', 'left_vb', 'left_nvfp', 'left_prhvh',
             'left_prp', 'left_fp', 'imageQualityFactor', 'imageQuality',
             'cataract', 'glaucoma', 'maculopathy', 'occlusion',
             'otherReferrable', 'left_irma_final', 'left_he_final', 'left_hma_final',
             'left_grade']

dataR = df.loc[(df.side == 'Right'), var_listR]
dataL = df.loc[(df.side == 'Left'), var_listL]

# change labels before combining R and F
dfR = dataR.rename(index=str, columns={'right_noDr': 'noDr', 'right_ma':'ma',
                   'right_cw':'cw', 'right_vb':'vb', 'right_nvfp':'nvfp', 'right_prhvh':'prhvh',
                   'right_prp':'prp', 'right_fp':'fp','right_irma_final':'irma_final',
                   'right_he_final':'he_final', 'right_hma_final':'hma_final',
                   'right_grade':'grade'})

dfL = dataL.rename(index=str, columns={'left_noDr': 'noDr', 'left_ma': 'ma',
                   'left_cw':'cw', 'left_vb': 'vb', 'left_nvfp': 'nvfp', 'left_prhvh': 'prhvh',
                   'left_prp':'prp', 'left_fp': 'fp','left_irma_final':'irma_final',
                   'left_he_final':'he_final', 'left_hma_final': 'hma_final',
                   'left_grade':'grade'})

data = pd.concat([dfR, dfL])

# select records based on the img quality
# data = data.loc[(df.imageQuality == 'Good') | (df.imageQuality == 'Adequate')
#                 | (df.imageQuality == 'Excellent'))

# replacement: " " -> None in str variables; "yes" -> 1; "no/None" ->0
# data = pd.read_csv("df13.csv")

data['ma'] = data['ma'].replace(['no', None], '0')
data['ma'] = data['ma'].replace(['yes'], '1')

data['cw'] = data['cw'].replace(['no', None], '0')
data['cw'] = data['cw'].replace(['yes'], '1')
data['vb'] = data['vb'].replace(['no', None], '0')
data['vb'] = data['vb'].replace(['yes'], '1')
data['nvfp'] = data['nvfp'].replace(['no', None], '0')
data['nvfp'] = data['nvfp'].replace(['yes'], '1')
data['prhvh'] = data['prhvh'].replace(['no', None], '0')
data['prhvh'] = data['prhvh'].replace(['yes'], '1')
data['prp'] = data['prp'].replace(['no', None], '0')
data['prp'] = data['prp'].replace(['yes'], '1')
data['fp'] = data['fp'].replace(['no', None], '0')
data['fp'] = data['fp'].replace(['yes'], '1')

data['imageQualityFactor'] = data['imageQualityFactor'].replace([None], 'None')

data['cataract'] = data['cataract'].replace([None], '0')
data['cataract'] = data['cataract'].replace(['yes'], '1')
data['glaucoma'] = data['glaucoma'].replace(['no', None], '0')
data['glaucoma'] = data['glaucoma'].replace(['yes'], '1')
data['maculopathy'] = data['maculopathy'].replace(['no', None], '0')
data['maculopathy'] = data['maculopathy'].replace(['yes'], '1')
data['occlusion'] = data['occlusion'].replace(['no', None], '0')
data['occlusion'] = data['occlusion'].replace(['yes'], '1')
data['otherReferrable'] = data['otherReferrable'].replace(['no', None], '0')
data['otherReferrable'] = data['otherReferrable'].replace(['yes'], '1')

df = df.loc[(df.right_irma_final != -1) & (df.left_irma_final != -1) &
            (df.right_he_final != -1) & (df.left_he_final != -1) &
            (df.right_hma_final != -1) & (df.right_hma_final != -1)]

data.to_csv(final_filename)

