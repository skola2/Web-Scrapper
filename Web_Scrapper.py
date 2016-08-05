#!/usr/bin/python3
import BeautifulSoup
from BeautifulSoup import BeautifulSoup
import sgmllib
import urllib2
from Tkinter import *
import tkMessageBox
import re
import os
import urlparse
import unicodedata
import datetime
import traceback
import sys
#import logging
import requests

global exception_file
exception_file = open("All_exceptions.txt",'w')

def soup_def(url):
  try:
    #request = urllib2.Request(url)
    #request.add_header('User-Agent', 'Mozilla/39.0')
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read())
    return soup
  
  except Exception, e:
    return e
  
def company_rat(j):
  try:
    rating_url=j.find("a","ratingsLabel")
    if rating_url is not None:
      rating_url1 = rating_url['href']
      rating_url2 = rating_url['onmousedown']
      start_rat=rating_url2.find("jt")
      end_rat=rating_url2.find("');")
      meta_rating = rating_url2[start_rat:end_rat]
      comp_url="http://www.indeed.com"
      final_url=str(comp_url)+str(rating_url1)+"?"+ str(meta_rating)
      #print final_url
      soup = soup_def(final_url)
      comp_rat=soup.find("div",{"id":"company_header"})
      company_rating = comp_rat.find("span","value-title")['title']
      
    else:
      company_rating = "no company rating"
    return company_rating

  except Exception, e:
    print "exception in company_rat"
    print e
    return e
    


def jobs_at_other_locations(url_part,rank):
  try:
    subrank = 1
    first_part = "http://www.indeed.com"
    total_url = first_part+str(url_part)
    soup2 = soup_def(total_url)
    #print total_url
    print "L"
    other_jobs=soup2.findAll("div",{"class":"  row  result"})
    other_last_job=soup2.findAll("div",{"class":"lastRow  row  result"})
    other_locations_jobs = {}
    other_locations_jobs = other_jobs,other_last_job
    for i in other_locations_jobs:
      for j in i:
        indeed_subrank = str(rank)+"."+str(subrank)
        write(j,indeed_subrank)
        subrank += 1
    return True

  except Exception, e:
    print "exception in jobs_at_other_locations"
    print e
    return e
    
  
def write(j,rank):
  try:
    current_date = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
    title= j.a['title'].encode('ascii','ignore')
    company = j.find("span",itemprop="name")
    if company is not None:
      if company.find("b"):
        company1=""
        for i in company.contents:
          company1 +=i.string
        company=company1.encode('ascii','ignore')
      else:
        company = company.string.encode('ascii','ignore')
      if " &amp; " in str(company):
        company = company.replace(' &amp; ',' & ')
      elif "&amp;" in str(company):
        company = company.replace('&amp;','&')
    else:
      company = "No Company Name"
    reviews = j.find("a",{"class":"sl"},{"class":""})
    if reviews is not None:
      reviews = reviews.string.encode('ascii','ignore')
      company_rating = company_rat(j)
      #company_rating = "Got Ratings"
      print "R"
    else:
      reviews = "No Reviews"
      company_rating = "No Ratings"
    
    location = j.find("span",itemprop="addressLocality")
    if location is not None:
      location = location.string
    else:
      location = "NO Location Listed"
    posted_date = j.find("span","date")
    if posted_date is not None:
      posted_date = posted_date.string.encode('ascii','ignore')
    else:
      posted_date = "No posted date listed"
    summary = j.find("span","summary")
    if summary is not None:
      if summary.find("b"):
        summary1 = ""
        for i in summary.contents:
          summary1 +=i.string
        summary=summary1.encode('ascii','ignore').lstrip()
      else:
        summary=summary.string.encode('ascii','ignore').lstrip()
    easy_apply = j.find("span","iaLabel")
    if easy_apply is not None:
      easy_apply = easy_apply.string
    else:
      easy_apply = "no easy to apply"
    more_loc = j.find("a","more_loc")
    if more_loc is not None:
      more_loc_url = more_loc['href']
      more_loc = more_loc.string.encode('ascii','ignore')
    else:
      more_loc = "No more extra locations listed"
      more_loc_url = "No Loc"

    sponsored = j.find("span","sdn")
    if sponsored is not None:
      sponsored_tag = sponsored.contents[0]
      sponsored_comp = sponsored.b.string
    else:
      sponsored_tag = "Organic"
      sponsored_comp = ""
      
    if sponsored_tag == "Organic":
      data1.write(str(current_date) + " , " + str(rank)+ " , " + str(title) + " , " + str(company) + " , " +
                  str(reviews) + " , " + str(company_rating)+ " , " + str(location) + " , " + str(posted_date) + " , " +
                  str(easy_apply) + " , " + str(more_loc) + " , " + str(sponsored_tag) + str(sponsored_comp)+ " , " + str(summary) + "\n")

    else:
      data2.write(str(current_date) + " , " + str(rank)+ " , " + str(title) + " , " + str(company) + " , " +
                  str(reviews) + " , " + str(company_rating)+ " , " + str(location) + " , " + str(posted_date) + " , " +
                  str(easy_apply) + " , " + str(more_loc) + " , " + str(sponsored_tag) + str(sponsored_comp)+ " , " + str(summary) + "\n")
      
    
    if more_loc_url != "No Loc":
      jobs_at_other_locations(more_loc_url,rank)
    return True

  except Exception, e:
    print "exception in Write"
    print e
    return e
  
def fetch(entries):
  try:
    cities = "New York, NY","Los Angeles, CA","Atlanta, GA","Chicago, IL","Dallas, TX","Durham, NC"
    #cities = "New York, NY" , "Durham, NC"
    global data1
    global data2
    for city in cities:
      city_parameter = city.replace(' ','+').replace(',','%2C')
      for i in entries:
        search_parameter = i[1].get().replace(' ','+').replace('"','%22').replace(':','%3A')
        current_date = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        #search_parameter = entries[0][1].get().replace(' ','+').replace('"','%22').replace(':','%3A')
        #city_parameter = entries[1][1].get().replace(' ','+').replace(',','%2C')
        data_file_org = city + "_" + search_parameter + "_Org.txt"
        print data_file_org
        data_file_spon = city + "_" + search_parameter + "_Spon.txt"
        print data_file_spon
        data1 = open(data_file_org,'w')
        data2 = open(data_file_spon,'w')
        url = "http://www.indeed.com/jobs?q=" + str(search_parameter) + "&l=" + str(city_parameter)
        print "11111111"
        soup = soup_def(url)
        print "2222222222"
        total_pages = 101
        if city == "Durham, NC":
          total_jobs = soup.find("meta",{"name":"description"})['content'].split(' ')[0]
          total_pages = (int(total_jobs.replace(",",""))/10) + 1
        print total_pages
        inc = 10
        indeed_rank = 1
        indeed_spon_rank = 1
        log_count = 1
        jobs_list1 = {}
        jobs_list2 = {}
        for i in range(1,total_pages):
          try:
            print i
            if i==1:
              soup1=soup
            else:
              url = "http://www.indeed.com/jobs?q=" + str(search_parameter) + "&l=" + str(city_parameter) + "&start=" + str(inc)
              soup1=soup_def(url)
              inc = inc+10
            spon_jobs=soup1.findAll("div",{"class":"row  result"})
            spon_last_job=soup1.findAll("div",{"class":"row sjlast result"})
            org_jobs=soup1.findAll("div",{"class":"  row  result"})
            last_job=soup1.findAll("div",{"class":"lastRow  row  result"})
            jobs_quit=soup1.find("p","dupetext")
            jobs_list1 = org_jobs,last_job
            jobs_list2 = spon_jobs,spon_last_job
            for i in jobs_list1:
              for p in i:
                write(p,indeed_rank)
                indeed_rank += 1
            for i in jobs_list2:
              for k in i:
                write(k,indeed_spon_rank)
                indeed_spon_rank += 1
            if jobs_quit is not None:
              break

          except Exception, e:
            print "exception in fetch"
            exception_file.write(str(log_count)+" , "+str(current_date)+str(e) + "\n")
            log_count +=1
            continue
               
        data1.close()
        data2.close()
        print "end"
        
  except Exception, e:
    print "exception in outside fetch"
    exception_file.write("Outside Loop"+" , "+str(e))
    data1.close()
    data2.close()
    exception_file.close()
    print e
    sys.exit(1)

fields = 'Search String1','Search String2','Search String3', 'Search String4','Search String5','Search String6'
field_entries = 'store manager','store manager jobs','retail manager', 'retail manager jobs','retail store manager','retail store manager jobs'
#fields = 'Search String1', 'City Parameter'
#field_entries = 'store manager','New York, NY'
#field_entries = 'store manager','store manager jobs','retail manager', 'retail manager jobs','retail store manager','retail store manager jobs','Los Angeles, CA'
#field_entries = 'store manager','store manager jobs','retail manager', 'retail manager jobs','retail store manager','retail store manager jobs','Atlanta, GA'
#field_entries = 'store manager','store manager jobs','retail manager', 'retail manager jobs','retail store manager','retail store manager jobs','Chicago, IL'
#field_entries = 'store manager','store manager jobs','retail manager', 'retail manager jobs','retail store manager','retail store manager jobs','Dallas, TX'
#field_entries = 'store manager','store manager jobs','retail manager', 'retail manager jobs','retail store manager','retail store manager jobs','Durham, NC'


def makeform(root, fields):
  count = 0
  entries = []
  for field in fields:
    row = Frame(root)
    lab = Label(row, width=15, text=field, anchor='w')
    ent = Entry(row,state=NORMAL)
    ent.insert(INSERT,field_entries[count])
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    lab.pack(side=LEFT)
    ent.pack(side=RIGHT, expand=YES, fill=X)
    entries.append((field, ent))
    count += 1
  return entries


if __name__ == "__main__":
  root = Tk()
  ents = makeform(root, fields)
  root.bind('<Return>', (lambda event, e=ents: fetch(e)))
  b1 = Button(root, text='Indeed',
       command=(lambda e=ents: fetch(e)))
  b1.pack(side=LEFT, padx=5, pady=5)
  b2 = Button(root, text='Quit', command=root.quit)
  b2.pack(side=LEFT, padx=5, pady=5)
  root.mainloop()

