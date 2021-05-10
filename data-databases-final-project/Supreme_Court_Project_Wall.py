#!/usr/bin/env python
# coding: utf-8

# ## Supreme Court Project Guide
# 
# The ultimate goal of this project is to build a database of Supreme Court cases for 2019 (or a different range of years) that includes the dialogue from the oral arguments of each case. As we have seen in class the arguments were scraped from this page: https://www.supremecourt.gov/oral_arguments/argument_transcript.aspx 
# 
# I have already downloaded and transformed the PDFs of the transcripts into text documents which you can download from courseworks: supreme_court_pdfs_txt.zip
# 
# There are three primary programmatic steps that you need to complete:
# 
# **Please note:** Step 3 is the most challenging--if you want to spend some time coding, you can skip Steps 1 and 2 and get to work on Step 3
# 
# **STEP 1:** scrape all of the case information available on this page: https://www.supremecourt.gov/oral_arguments/argument_transcript/2019
# 
# This should include case name, docket number, etc--and most importantly the name of the PDF file. All of the text files share the exact same name as the PDF files they came from. This file name will allow you to connect your transcription data with your case data. 
# 
# It is up to you what kind data structure you want to build. But it likely to be a list of lists, or list of dictionaries--for each case you will have a list or dictionary of the information you scrape from the webpage.
# 
# **STEP 2:** find secondary source(s) to scrape/integrate with your case data. The information on the Supreme Court page is very limited. You need to find a source or group of sources that ad information. The most important information would likely be: the decision, who voted for and against, and the district court origin of the case (for geocoding). You might think of other great things to put in there too! This information needs to be merged with the data you have from STEP 2.
# 
# **STEP 3:** use regular expressions to clean up and parse the text files so that you have a searchable data structure containing the dialog from the transcripts. 
# 
# **Data Architecture** 
# You will need to think about how you will set up, separate, and join different tables that you create. The initial scraping will give you very simple dataframe: the columns will be dockett, case name, date argued, and PDF name. The regex work on the PDFs should result in a very simple table (or just a list of tuples) of speaker name and dialogue. 
# 
# `[('MR. BERGERON'," Yes. That's essentially the same thing"),('JUSTICE SOTOMAYOR',' So how do you deal with Chambers?')]`
# 
# But make sure you attach the docket number or pdf filename to each set of arguments transform using regex. Your secondary sources and information should be linked by docket number, but the question is how to set up those data frames, join them, aggregate them, and narrow them to the fields necessary for presentation.
# 
# Go step-by-step through this, and DM me on Slack whenever you get stuck, and I will help. If you complete all the steps before Thursday, Slack me if you want to go further.
# 
# **Interpretive Architecture**
# Also consider what kind of interpretive categories you can add through your reading and research. At the very least, it is recommended that you come up with categories for the kinds of cases that are before the court: human clustering for meaning is always more effective than computational clustering. Try to come up with perhaps 8 to 10 domains that groups of cases might belong to. But also think of other ways of categorizing these cases or these decisions--by politics, by consequences on citizens (you could make a scale from 1 to 10), even an aggregated index of consequences/effects on different types of communities, sectors, regions, etc. 
# 
# You are the researcher, these categories or ways of expressing your point-of-view.
# 
# 

# ### STEP 1
# Scrape all of the necessary information from:
# 
# https://www.supremecourt.gov/oral_arguments/argument_transcript.aspx 
# 
# You should result and a list of dictionaries for each case.

# In[1]:


###Import your scraping libraries

import requests
from bs4 import BeautifulSoup


# In[2]:


scotus = "https://www.supremecourt.gov/oral_arguments/argument_transcript/2019"
raw_html = requests.get(scotus).content
doc = BeautifulSoup(raw_html, "html.parser")
# print(doc.prettify())



# In[3]:


cases_2019 = doc.find_all('tr')[2:]


# In[4]:


all_2019 = []
for case in cases_2019:
    cases_dict = {}
    try:
        #print("-----------")
        elements = case.find_all('td')
        elementA = elements[0].find('a')     
        cases_dict['docket'] = elementA.text
        cases_dict['name'] = elements[0].find_all('span')[1].text
        cases_dict['date'] = elements[1].text
        cases_dict['pdf'] = elementA['href']
    except:
        pass
    #print(cases_dict)
    all_2019.append(cases_dict)

# all_2019


# In[5]:


docks = []
for num in all_2019:
    try:
        docks.append(num['docket'])
    except:
        pass
print(len(docks))


# In[6]:


import pandas as pd


# In[7]:


df = pd.DataFrame(all_2019)
df.head()


# ### STEP 2 
# Scrape the additional source(s)
# 
# For this you need to do research and try to find sources that will give you useful information that you can add to the table/dictionary you created in Step 1.
# 
# Here are some recommended sources that you can scrape and add to your data. You do not need to scrape all of these, and you may want to look for other sources that are useful.
# 
# Geographical locations:
# https://system.uslegal.com/us-courts-of-appeals/
# 
# Transcripts by year
# https://www.supremecourt.gov/oral_arguments/argument_transcript/2017
# 
# Dockets buy circuit court (I recommend at least this one):
# https://www.supremecourt.gov/orders/ordersbycircuit/ordercasebycircuit/061118OrderCasesByCircuit
# 
# Dockett information by case:
# https://www.supremecourt.gov/search.aspx?filename=/docket/docketfiles/html/public/17-7919.html
# 
# Opinions (as seen in Homework 3):
# https://www.supremecourt.gov/opinions/slipopinion/17

# In[8]:


#Code away!
lower_courts = "https://www.supremecourt.gov/search.aspx?filename=/docket/docketfiles/html/public/19-177.html"
raw_html = requests.get(lower_courts).content
doc2 = BeautifulSoup(raw_html, "html.parser")
# print(doc2.prettify())


# In[9]:


items = doc2.find_all('table')
circuits = items[2].find_all('span')
print(circuits[9].text.strip())


# In[10]:


docks = []
for court in all_2019:
    try:
        docks.append(court['docket'])
    except:
        pass
print(len(docks))


# In[11]:


other_source = []
for dock in docks:
    try:
        more_courts = {}
        lowers =f'https://www.supremecourt.gov/search.aspx?filename=/docket/docketfiles/html/public/{dock}.html'
        raw_html = requests.get(lowers).content
        doc1 = BeautifulSoup(raw_html, "html.parser")
        items = doc1.find_all('table')
        circuits = items[2].find_all('span')
        more_courts['docket'] = dock
        more_courts['lower_court'] = circuits[9].text.strip()
    except:
        pass
    
    #print(more_courts)
    other_source.append(more_courts)

# print(other_source)


# In[12]:


df2 = pd.DataFrame(other_source)
df2.head()


# In[13]:


merged = df.merge(df2, how = 'outer', left_on = 'docket', right_on = 'docket')
# merged.head(58)
merged = merged.dropna()


# # Step 1 & 2 data frame

# In[14]:


len(merged.docket)
merged.head()


# In[15]:


merged.to_csv("merged.csv", index=False, header=True)


# ### STEP 3
# Here we go: the text files that were extracted from the PDFs are quite messy, you do not need to get them perfect, but you need to clean them up enough so that you can zone in on the arguments themselves. Below I take you step-by-step through what you need to do. In the end you want to have a separate list for each case that contains the speaker and the dialogue attached to that speaker.

# **Step 1:** Download the text files from courseworks.
# 
# Make sure they are locally on your computer. 
# 
# Open up the text files in a text editor like sublime, and carefully look at the problems with the files. How will you clean this up?

# **Step 2:** Eventually you will want to loop through all of the text files and run the cleanup on all of them. But first just select one text file to open up and begin cleaning up.

# In[16]:


#Import the regular expression library
import re


# In[17]:


#Open a text file from your computer

f = open('/Users/sheridanwall/Documents/Data/2019pdfs_official/17-834_5h25.txt', 'r')

#f = open('/Users/YOU/Documents/columbia_syllabus/pdf/15-777_1b82.txt', 'r')
sample_transcript = f.read()


# In[18]:


#Take a look at the text file
sample_transcript


# **How in the world are you going to clean this up?**
# Take a close look and think about first what needs to be removed, and then needs to be isolated. You'll probably need the combination of regular expression (especially using subs() -- which is a regex replace), and simple splits -- where you split the text that point, and just keep the part of the text that you want. If you want to figure this on your own don't read any further--if you're starting to get stuck go a few cells down, and follow my hints.
# 
# Also take a look at the hint below--it might come in very handy...
# 

# In[19]:


#A note on regex splits:
# look at the difference between regex1 regex2
#A split using groups keeps the groups!!!!

string = "Tomorrow and tomorrow and tomorrow"
regex1 = r"and" #not grouped
regex2 = r"(and)" #grouped
re.split(regex2,string)


# ### Cleaning comes first
# 
# A step-by-step way of Cleaning up this mess.
# 
# Step 1. You might notice that every page has:
# 
# `Heritage Reporting Corporation
# 
# Official 2 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25`
# 
# (Note in earlier years it was:
# `Alderson Reporting Company
# 
# Official - Subject to Final Review`
#  If you choose to transform arguments from earlier years, please Slack me and I will send you the instructions for earlier versions of these PDFs.
#  )
# You want to get rid of that. I would use a regex sub() 
# 
# Step 2 and 3. **chop off the beginning/ chop off the end**: now it would be very helpful to get rid of all of the text that comes before the arguments begin, and all the text that comes after the argument (each page has a really annoying index at the end that you don't want to be searching through). Look for words or phrases that uniquely repeat at the beginning and at the end of the arguments. The easiest way to isolate this, to do a simple split() on one of those phrases, and keep the half of The split you want. (Am I being too cryptic here?--a good split should give you list with two elements when you want to keep one of them) Think about it and email me.
# 
# Try to get these 3 cleaning actions to work step-by-step in the 4 cells below. As you go, I would assign each cleaner version of the text to a new variable. 

# In[20]:


#1. Heritage company stuff, and numbers
heritage = r"HERITAGE REPORTING CORPORATION"
re.findall(heritage, sample_transcript)
clean1 = re.sub(heritage,"",sample_transcript)

heritage2 = r"Heritage Reporting Corporation[\s\n\d-]+Official"
re.findall(heritage2, clean1)
clean2 = re.sub(heritage2,"",clean1)
#clean2


# In[21]:


#2. Chop off the beginning before the dialogue begins

clean3 = re.split(r"(\nCHIEF JUSTICE ROBERTS:)", clean2,1)
cleanA = clean3[1]+clean3[2]


# In[22]:


#3. Chop off the end after the dialogue ends

clean4 = re.split("(The case is submitted.)",cleanA,1)
cleanB = clean4[0] + clean4[1]


# In[23]:


#Check your new variable to make sure it is clean

# cleanB


# ### Get your dialogue list
# Now this transcription should be clean enough to get a list with every speaker, and what the speaker said. The pattern for the speakers is fairly obvious--my recommendation is to do a split using groups (like the example I show above with "tomorrow and tomorrow").
# 
# If you write your regular expression correctly: you should get a single list in which each element is either a speaker, or what was said.

# In[24]:


#get a list of speaker and speech

speakers = r"\n[A-Z\s\n]+:"
re.findall(speakers,cleanB)


# In[25]:


regex1 = r"(\n[A-Z\s\n]+:)"
dialogue = re.split(regex1,cleanB)
# print(dialogue)


# ### Make it a list of pairs
# If you got your list the way I recommended to, it is just single list with elements after element--you need to figure out how to change it so you pair the speaker with what is said. Give it some thought, there are a few ways to try to do this. If you made it this far, you're doing great!

# In[26]:


#make it a list of pairs of speaker and speech

joined_dialogue = [[dialogue[x],dialogue[x+1]] for x in range(1,len(dialogue),2)]
# print(joined_dialogue)


# ### Loop through all texts
# If you made it this far--congratulations! 
# The only thing left is to set up a loop that looks through all the texts and runs the cleanup and parsing when each one. You will need to have completed Step 1 in order to be able to do this loop because you will need the names to PDFs to do it. (Also each final list should also contain the PDF name, so you can reference it from your case database.)

# In[27]:


# you could try here--Or email me with questions...


# In[28]:


all_cases = []
for file in all_2019:
    try:
        name_pdf = file['pdf'].split('/')[-1]
        name_txt = name_pdf.split('.')[0] + ".txt"
        #print(name_txt)
        f = open('/Users/sheridanwall/Documents/Data/2019pdfs_official/'+name_txt, 'r')
        each_transcript = f.read()
        find_her = r"Heritage Reporting Corporation[\s\n\d-]+Official"
        clean_transcript = re.sub(find_her,"",each_transcript)
        clean_transcripts1=re.split(r"(\nCHIEF JUSTICE ROBERTS:)",clean_transcript,1)
        split_transcripts = clean_transcripts1[1]+clean_transcripts1[2]
        split_transcript1 = re.split(r"(The case is submitted.)", split_transcripts,1)
        split_transcripts2 = split_transcript1[0]+split_transcript1[1]
        find_speakers = r"(\n[A-Z\s\n]+:)"
        speaker_transcripts = re.split(find_speakers,split_transcripts2)
        joined_dialogue1 = [[speaker_transcripts[x],speaker_transcripts[x+1],file['docket']] for x in range(1,len(speaker_transcripts),2)]
        all_cases+=joined_dialogue1
    except:
        pass

print(all_cases[1])


# In[29]:


import pandas as pd
col_names = ['speaker','words', 'docket']
dialogue = pd.DataFrame(all_cases, columns=col_names)


# In[30]:


dialogue.head()


# # Final dialogue data frame

# In[31]:



dialogue['speaker'] = dialogue.speaker.str.replace(r'\n','',regex=True)
dialogue['words'] = dialogue.words.str.replace(r'\n','',regex=True)
dialogue.head()


# # Analysis of speakers

# Most common speaker per case: 

# In[324]:


most_common_speaker = dialogue.groupby(['docket']).speaker.value_counts().nlargest(58)
most_common_speaker


# Most common speaker total

# In[33]:


most_common_speaker_total = dialogue.speaker.value_counts()
most_common_speaker_total.head().plot(kind = 'barh')


# In[34]:


from collections import Counter
import re


# In[35]:


justice_speakers = dialogue[dialogue.speaker.str.contains('JUSTICE')]
justice_speakers


# In[36]:


speaker_wordcount = justice_speakers.groupby(['speaker']).sum().applymap(lambda words: Counter(re.findall(r"\b\w{10,}\b",words.lower())).most_common())


# In[334]:


speaker_wordcount.head()


# In[332]:


def apply_to_words(word):
    return word[:5]


# In[333]:


justice_common_words = speaker_wordcount.words.apply(apply_to_words).reset_index()


# At this point, I would have liked to have done an aggregation of the five most common words used by each justice. I attempted to do that by grouping by speaker, and then re-formatting the tuples (seen below), but because the words are in this format, that kind of analysis isn't possible through the methods I attempted.

# In[ ]:





# In[325]:





# In[ ]:





# # Looking at Justice Ginsburg

# In[41]:


rbg = dialogue[dialogue.speaker == 'JUSTICE GINSBURG:']
rbg_num_quotes = rbg.docket.value_counts().reset_index()


# In[42]:


rbg_num_quotes = rbg.docket.value_counts().reset_index()
rbg_num_quotes.columns = ['docket','speech_count']
rbg_num_quotes.head()


# In[43]:


rbg_wordcount = rbg.groupby(['docket']).sum().applymap(lambda words: Counter(re.findall(r"\b\w{7,}\b",words.lower())).most_common())


# In[44]:


rbg_wordcount


# In[45]:


def apply_to_row(row):
    return row[:5]


# In[47]:


rbg_words = rbg_wordcount.words.apply(apply_to_row).reset_index()


# In[48]:


rbg_speech = rbg_words.merge(rbg_num_quotes, how='outer', left_on = 'docket', right_on = 'docket')


# In[49]:


rbg_speech.head()


# # Ginsburg Table

# In[50]:


ginsburg = rbg_speech.merge(merged, how = 'outer', left_on = 'docket', right_on='docket')
ginsburg.columns = ['docket', 'most_used_words', 'speech_count', 'case_name', 'date', 'transcript_pdf', 'lower_court']
ginsburg.head()


# In[51]:


ginsburg.to_csv('ginsburg.csv', index=False, header=True)


# # Cleaning Ginsburg Table

# In[197]:


import numpy as np


# In[198]:


ginsburg['lower_court'] = ginsburg_readable.lower_court.replace("", np.nan)


# In[199]:


ginsburg = ginsburg.dropna()


# In[207]:


# Making top 5 words readable
def transl(topwords):
    word_string = "The top 5 words are: "
    elements = topwords.split('||')
    for element in elements:
        words = element[1:-1].split(',')
        if len(words) == 2:
            word_string += words[0][1:-1] + ": " + words[1] + " occurances. "
    return word_string




# In[209]:


ginsburg['words_readable'] = ginsburg['most_used_words'].apply(lambda x: transl('||'.join(map(str, x))))


# In[212]:


ginsburg.head(60)


# In[214]:


ginsburg.words_readable.head()


# In[73]:


# Cleaning speech count


# In[ ]:





# In[215]:


ginsburg['speech_count'] = ginsburg.speech_count.astype(str)
ginsburg.head()


# In[216]:


ginsburg['count_readable'] = 'Spoke ' + ginsburg['speech_count'].astype(str) + ' times'


# In[217]:


ginsburg.head()


# In[218]:


ginsburg["name_date"] = "<b>Case:</b> " + ginsburg["case_name"] + " , " + ginsburg["date"].map(str) + "<br>"


# In[219]:


ginsburg.head()


# In[220]:


# Joining article properties

ginsburg["article_cell"] = ginsburg["name_date"] + "<br>" + ginsburg["count_readable"].map(str) + "<br>" + ginsburg["words_readable"]


# In[221]:


ginsburg.head()


# # Map Properties

# In[222]:


output = ginsburg.groupby('lower_court')['article_cell'].apply(lambda x: "<div id='article'><P>%s</P></div>" % '</p><p> '.join(x)).reset_index(name='properties.article')
output


# In[97]:


circ_courts = ginsburg_readable.groupby('lower_court')['case_name'].nunique().reset_index(name='properties.headline')
circ_courts.head(20)


# In[223]:


output.iloc[3]['properties.article']


# In[250]:


output1 = output.merge(circ_courts, how='left', on='lower_court')


# In[307]:


output1['properties.color'] = "#251FE0"
output2 = output1.sort_values(by="properties.headline", ascending = False).reset_index()


# In[309]:


output3= output2.drop(columns='index')
output3


# # Courts & Cities

# In[310]:


cities = ["San Franscisco, CA","Atlanta, GA","New York, NY",
    "Richmond, VA","Washington D.C.","Denver, CO","Cincinnati, OH",
          "Philadelphia, PA","Topeka, KS","New Orleans, LA","Washington D.C.",
          "Helena, MT","Olympia, WA","Phoenix, AZ", "St. Louis, MO","Oklahoma City, OK","New Orleans, LA"]


# # Merging with json 

# In[311]:


geo_points = [{"place": "San Franscisco, CA", "geometry.type": "Point", "geometry.coordinates": [-122.4194155, 37.7749295]}, {"place": "Atlanta, GA", "geometry.type": "Point", "geometry.coordinates": [-84.3879824, 33.7489954]}, {"place": "New York, NY", "geometry.type": "Point", "geometry.coordinates": [-74.0059728, 40.7127753]}, {"place": "Richmond, VA", "geometry.type": "Point", "geometry.coordinates": [-77.4360481, 37.5407246]}, {"place": "Washington, DC", "geometry.type": "Point", "geometry.coordinates": [-77.0368707, 38.9071923]}, {"place": "Denver, CO", "geometry.type": "Point", "geometry.coordinates": [-104.990251, 39.7392358]}, {"place": "Cincinnati, OH", "geometry.type": "Point", "geometry.coordinates": [-84.5120196, 39.1031182]}, {"place": "Philadelphia, PA", "geometry.type": "Point", "geometry.coordinates": [-75.1652215, 39.9525839]}, {"place": "Topeka, KS", "geometry.type": "Point", "geometry.coordinates": [-95.67515759999999, 39.0473451]}, {"place": "New Orleans, LA", "geometry.type": "Point", "geometry.coordinates": [-90.0715323, 29.95106579999999]}, {"place": "Washington, DC", "geometry.type": "Point", "geometry.coordinates": [-77.0368707, 38.9071923]}, {"place": "Helena, MT", "geometry.type": "Point", "geometry.coordinates": [-112.0391057, 46.5891452]}, {"place": "Olympia, WA", "geometry.type": "Point", "geometry.coordinates": [-122.9006951, 47.0378741]}, {"place": "Phoenix, AZ", "geometry.type": "Point", "geometry.coordinates": [-112.0740373, 33.4483771]}, {"place": "St. Louis, MO", "geometry.type": "Point", "geometry.coordinates": [-90.19940419999999, 38.6270025]}, {"place": "Oklahoma City, OK", "geometry.type": "Point", "geometry.coordinates": [-97.5164276, 35.4675602]}, {"place": "New Orleans, LA", "geometry.type": "Point", "geometry.coordinates": [-90.0715323, 29.95106579999999]}]


# In[312]:


final_df = pd.DataFrame(geo_points)


# In[313]:


final_df.head()


# In[314]:


final_output = output3.join(final_df, how="outer")
final_output


# In[315]:


final_json = json.loads(final_output.to_json(orient='records'))


# In[316]:


final_json


# In[317]:


def process_to_geojson(file):
    geo_data = {"type": "FeatureCollection", "features":[]}
    for row in file:
        this_dict = {"type": "Feature", "properties":{}, "geometry": {}}
        for key, value in row.items():
            key_names = key.split('.')
            if key_names[0] == 'geometry':
                this_dict['geometry'][key_names[1]] = value
            if str(key_names[0]) == 'properties':
                this_dict['properties'][key_names[1]] = value
        geo_data['features'].append(this_dict)
    return geo_data


# In[318]:


geo_format = process_to_geojson(final_json)


# In[319]:


geo_format


# In[320]:


with open('geo-data12-11.js', 'w') as outfile:
    outfile.write("var infoData = ")
with open('geo-data12-11.js', 'a') as outfile:
    json.dump(geo_format, outfile)


# In[ ]:





# In[ ]:




