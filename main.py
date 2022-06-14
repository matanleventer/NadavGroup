import requests
from bs4 import BeautifulSoup
import wget
import zipfile
import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

def web_crawler():
  url = "https://www.cdc.gov/nchs/data_access/vitalstatsonline.htm"
  f = requests.get(url)
  soup = BeautifulSoup(f.content,'lxml')
  list_path=[]
  path = soup.find('table', {'class': 'table'}).find_all('a')
  # Get url from web
  for link in path:
    try:
      list_path.append(link['href'])
    except:continue
  list_nes_path=[list_path[48],list_path[49],list_path[50],list_path[51],list_path[52]]
  # Downloads files
  for ur in list_nes_path:
    wget.download(ur)
  # Extract Files
  for num in range(2016,2021):
    with zipfile.ZipFile(f"C:/Users/matan/PycharmProjects/pythonProject6/Nat{num}us.zip", "r") as zip_ref:
      zip_ref.extractall("files")

def extract_load():
  filePath = 'C:/Users/matan/PycharmProjects/pythonProject6/files/'
  filePath_1 = 'C:/Users/matan/PycharmProjects/pythonProject6/files'
  dir_list = os.listdir(filePath)
  num=0
  for name in dir_list:
    #Create data set
    s=extractLines(filePath,name,num)
    num+=1
    with open(filePath_1 + "out.csv", 'a') as fd:
      fd.write(s)
      fd.close()

def Analysis(data):
  df_values_unique={}
  # View the Data
  print(data.head(5))
  #Describe the Data
  print((data.describe().T.iloc[:,:5]))
  print((data.describe().T.iloc[:,5:]))
  for col in data.columns:
     df_values_unique[col]=len(data[col].unique())
  #Unique each columns
  print(pd.Series(df_values_unique))
  # Dtypes each columns
  print(data.dtypes)
  number_of_Features = len(data.columns)
  print(f"There is number_of_Features : {number_of_Features}")


def plot_data_numeric(data):
  data_1=data.iloc[:,1:11]
  data_2=data.iloc[:,12:]
  list_data = [data_1,data_2]
  for dat in list_data:
    dat.hist(figsize=(20,15))
  plt.show()

def plot_data_categorial(data):
  data_dtypes = data.dtypes
  data_1=data.iloc[:,28:35]
  for col in data_1.columns:
    if data_dtypes[col] == 'string':
      count = Counter(data_1[col].to_dict().values())
      new_count = Counter({'Yes': count['Y'], 'No': count['N']})
      keys = new_count.keys()
      values = new_count.values()
      plt.bar(keys, values, color='black', width=0.4)
      plt.title(f'{col}')
      plt.show()

def extractLines(filePath, url, num):
  f = open(filePath + url, "r")
  if num == 0:
    # create columns names
    res = "id,birth_year,birth_month,birth_time,birth_place,mother_age,marital_status,mother_education,"
    res += "father_age,father_education,interval_llb,cigarettes,mother_height,mother_bmi,"
    res += "pre_preg_weight,delivery_weight,pre_preg_diabetes,gest_diabetes,pre_preg_hypertension,gest_hypertension,"
    res += "prev_preterm_birth,infertility_treatment,prev_cesarian,gonorrhea,syphilis,chlamydia,hepatitis_b,hepatitis_c,"
    res += "labor_induction,labor_augmentation,steroids,antibiotics,chorioamnionitis,anesthesia,"
    res += "apgar5,apgar10,plurality,gender,infant_weight\n"
  else:
    res = ""
  count = 1
  i = 0
  for s in f:
    if i % 20 == 0:
      res += str(count) + ","
      res += s[8:12] + ","
      res += s[12:14] + ","
      timeOfBirth = s[18:22]
      if timeOfBirth == "9999":
        timeOfBirth = ""
      res += timeOfBirth + ","

      birthPlace = s[31]
      if birthPlace == "9":
        birthPlace = ""
      res += birthPlace + ","

      res += s[74:76] + ","
      res += s[119] + ","

      motherEducation = s[123]
      if motherEducation == "9":
        motherEducation = ""
      res += motherEducation + ","

      fatherAge = s[146:148]
      if fatherAge == "99":
        fatherAge = ""
      res += fatherAge + ","

      fatherEducation = s[162]
      if fatherEducation == "9":
        fatherEducation = ""
      res += fatherEducation + ","

      intervalLLB = s[197:200]
      if intervalLLB == "999":
        intervalLLB = ""
      res += intervalLLB + ","

      cigarettes = s[252:254]
      if cigarettes == "99":
        cigarettes = ""
      res += cigarettes + ","

      motherHeight = s[279:281]
      if motherHeight == "99":
        motherHeight = ""
      res += motherHeight + ","

      bmi = s[282:286]
      if bmi == "99.9":
        bmi = ""
      res += bmi + ","

      prePregnancyWeight = s[291:294]
      if prePregnancyWeight == "999":
        prePregnancyWeight = ""
      res += prePregnancyWeight + ","

      deliveryWeight = s[298:301]
      if deliveryWeight == "999":
        deliveryWeight = ""
      res += deliveryWeight + ","

      diabetes = s[312]
      if diabetes == "U":
        diabetes = ""
      res += diabetes + ","

      gestationalDiabetes = s[313]
      if gestationalDiabetes == "U":
        gestationalDiabetes = ""
      res += gestationalDiabetes + ","

      hypertension = s[314]
      if hypertension == "U":
        hypertension = ""
      res += hypertension + ","

      gestationalHypertension = s[315]
      if gestationalHypertension == "U":
        gestationalHypertension = ""
      res += gestationalHypertension + ","

      pretermBirths = s[317]
      if pretermBirths == "U":
        pretermBirths = ""
      res += pretermBirths + ","

      infertilityTreatment = s[324]
      if infertilityTreatment == "U":
        infertilityTreatment = ""
      res += infertilityTreatment + ","

      ceserian = s[331:332]
      if ceserian == "U":
        ceserian = ""
      res += ceserian + ","

      for disease in range(342, 347):
        if s[disease] == "U":
          res += ""
        else:
          res += s[disease]
        res += ","

      for labor in range(382, 388):
        if s[labor] == "U":
          res += ""
        else:
          res += s[labor]
        res += ","

      apgar5 = s[443:445]
      if apgar5 == "99":
        apgar5 = ""
      res += apgar5 + ","

      apgar10 = s[447:449]
      if apgar10 == "99":
        apgar10 = ""
      res += apgar10 + ","

      res += s[453] + ","
      res += s[474] + ","
      res += s[503:507] + "\n"

      count += 1

    i += 1

  f.close()
  return res


web_crawler()
extract_load()
df = pd.read_csv("filesout.csv",low_memory=False)
data =df.convert_dtypes()
data = data.dropna()
Analysis(data)
plot_data_numeric(data)
plot_data_categorial(data)