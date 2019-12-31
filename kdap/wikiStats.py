#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 17:06:57 2019

@author: descentis
"""

import xmltodict
from datetime import date
import datetime
import mwparserfromhell
#get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from prettytable import PrettyTable


class wikiStats :
    
    #GENERAL STATISTICS
    def __init__(self, article) :
        
        f = open("botList.txt",'r',errors='ignore')
        self.bots = [ x.rstrip('\n') for x in list(f.readlines())]
        
        self.di = xmltodict.parse(open(article+'.knolml',"r",errors='ignore').read())
        #print(self.di)
        self.revisions = [x for x in self.di['KnolML']['KnowledgeData']['Instance']] 
        
        self.editors = {}
        self.botEditors = {}
        self.originals = {}
        
        for x in self.revisions :
            if(x['Knowl']['@key']=='sha' and self.originals.get(x['Knowl']['#text'])==None):
               self.originals[x['Knowl']['#text']] = x['TimeStamp']['CreationDate']
            '''                  
            if x['Knowl'] not in self.originals :
                self.originals[x['sha1']] = x['timestamp']
            '''
            username = x['Contributors']['OwnerUserName']
            if username not in self.bots:
                if username in self.editors :
                    self.editors[username] += 1
                else :
                    self.editors[username] = 1
            else :
                if username in self.botEditors :
                    self.botEditors[username] += 1
                else :
                    self.botEditors[username] = 1 
    
    def isOriginalRevision(self, revision) :
        return True if self.originals[revision['Knowl']['#text']] == revision['TimeStamp']['CreationDate'] else False
    
    def getID(self) :
        return self.di['KnolML']['KnowledgeData']['@Id']
            
    def getRevertedEdits(self) :
        i = 0
        for x in self.revisions :
            if not self.isOriginalRevision(x) :
                i += 1
        return i
    
    def getTotalEdits(self) :
        return len(self.revisions) 
    
    def getMinorEdits(self) :
        i = 0
        for x in self.revisions :
            if(x.get('EditDetails')!=None):
                if 'minor' in x['EditDetails']['EditType'] :
                    i += 1
        return i
    
    def getIPEdits(self) :
        i = 0
        for x in self.revisions :
            if(x['Contributors'].get('OwnerUserId')==None) :
                i += 1
        return i
    
    def getBotEdits(self) :
        ans = 0
        for bot in self.botEditors.keys() :
            ans += self.botEditors[bot]
        return ans
    
    def getEditors(self) :
        return len(self.editors) + len(self.botEditors)
    
    def getPageSize(self) :
        return self.revisions[-1]['Body']['Text']['@Bytes']
    
    def getFirstEdit(self) :
        di = {}
        di['user'] = self.revisions[0]['Contributors']['OwnerUserName']
        di['time'] = self.revisions[0]['TimeStamp']['CreationDate']
        di['text added'] = self.revisions[0]['Body']['Text']['@Bytes']
        return di
    
    def getLatestEdit(self) :
        di = {}
        di['user'] = self.revisions[-1]['Contributors']['OwnerUserName']
        di['time'] = self.revisions[-1]['TimeStamp']['CreationDate']
        try :
            di['text added'] = int(self.revisions[-1]['Body']['Text']['@Bytes']) - int(self.revisions[-2]['Body']['Text']['@Bytes'])
        except :
            di['text added'] = self.revisions[0]['Body']['Text']['@Bytes']
        return di
    
    def getMaxTextAdded(self) :
        di = {}
        di['user'] = self.revisions[0]['Contributors']['OwnerUserName']
        di['time'] = self.revisions[0]['TimeStamp']['CreationDate']
        di['text added'] = int(self.revisions[0]['Body']['Text']['@Bytes'])
        for i in range(1, len(self.revisions)) :
            temp = int(self.revisions[i]['Body']['Text']['@Bytes']) - int(self.revisions[i-1]['Body']['Text']['@Bytes'])
            if self.isOriginalRevision(self.revisions[i]) and temp > di['text added'] :
                di['user'] = self.revisions[i]['Contributors']['OwnerUserName']
                di['time'] = self.revisions[i]['TimeStamp']['CreationDate']
                di['text added'] = temp
        return di
    
    def getMaxTextDeleted(self) :
        di = {}
        di['user'] = None
        di['time'] = None
        di['text deleted'] = 0
        for i in range(1, len(self.revisions)) :
            temp = int(self.revisions[i]['Body']['Text']['@Bytes']) - int(self.revisions[i-1]['Body']['Text']['@Bytes'])
            if temp < di['text deleted'] :
                di['user'] = self.revisions[i]['Contributors']['OwnerUserName']
                di['time'] = self.revisions[i]['TimeStamp']['CreationDate']
                di['text deleted'] = temp
        return di
    
    #EDITS 
    def getAverageEditsPerUser(self) :
        return self.getTotalEdits()/self.getEditors()
    
    def getAverageTimeBetweenEdits(self) :
        timestamps = [ self.di['KnolML']['KnowledgeData']['Instance'][i]['TimeStamp']['CreationDate'] for i in range(len(self.di['KnolML']['KnowledgeData']['Instance']))]
        times = [date(year = int(timestamps[i][:4]), month = int(timestamps[i][5:7]), day = int(timestamps[i][8:10])) for i in range(len(timestamps))]
        timeDiff = date(1, 1, 1) - date(1, 1, 1)
        for i in range(len(times)-1) :
            timeDiff += times[i+1] - times[i]
        return timeDiff.days/(len(times)-1)
    
    def getAverageEditsPerDay(self) :
        t1 = self.getFirstEdit()['time']
        t1 = date(year = int(t1[:4]), month = int(t1[5:7]), day = int(t1[8:10]))
        t2 = datetime.date.today()
        return self.getTotalEdits()/(t2-t1).days
    
    def getAverageEditsPerMonth(self) :
        return 30*self.getAverageEditsPerDay()
    
    def getAverageEditsPerYear(self) :
        return 365*self.getAverageEditsPerDay()
    
    def getEditsInPastXDays(self, x) :
        timestamps = [ self.di['KnolML']['KnowledgeData']['Instance'][i]['TimeStamp']['CreationDate'] for i in range(len(self.di['KnolML']['KnowledgeData']['Instance']))]
        times = [date(year = int(timestamps[i][:4]), month = int(timestamps[i][5:7]), day = int(timestamps[i][8:10])) for i in range(len(timestamps))]
        t0 = datetime.date.today()
        count = 0
        for i in range(len(times)-1, -1, -1) :
            t = times[i]
            tDiff = t0 - t
            if tDiff.days > x :
                break
            else :
                count += 1
        return count
        
    def getEditsInPast24Hours(self) :
        return self.getEditsInPastXDays(x = 1)
    
    def getEditsInPast7Days(self) :
        return self.getEditsInPastXDays(x = 7)
        
    def getEditsInPast30Days(self) :
        return self.getEditsInPastXDays(x = 30)
    
    def getEditsInPast365Days(self) :
        return self.getEditsInPastXDays(x = 365)
    
    def getEditsByTop10Editors(self) :
        arr = []
        for x in self.editors.keys() :
            arr.append(self.editors[x])
        arr.sort(reverse = True)
        top10Edits = 0
        for i in range(10) :
            try :
                top10Edits += arr[i]
            except :
                break
        return top10Edits
    
    def printGeneralStats(self) :
        print("              ID :", self.getID())
        #print("       Page Size :", self.getPageSize())
        print("     Total Edits :", self.getTotalEdits())
        print("         Editors :", self.getEditors())
        print()
        print(" ----------------------------------- ")
        print()
        print("     Minor Edits :", self.getMinorEdits())
        print("        IP Edits :", self.getIPEdits())
        print("       Bot Edits :", self.getBotEdits())
        print("  Reverted Edits :", self.getRevertedEdits())
        print()
        print("      First Edit :", self.getFirstEdit())
        print("     Latest Edit :", self.getLatestEdit())
        print("  Max Text Added :", self.getMaxTextAdded())
        print("Max Text Deleted :", self.getMaxTextDeleted())
        print()
        print(" ----------------------------------- ")
        print()
        print("   Average Time Between Edits (days) :", self.getAverageTimeBetweenEdits(),"days")
        print("              Average Edits Per User :", self.getAverageEditsPerUser())
        print("               Average Edits Per Day :", self.getAverageEditsPerDay())
        print("             Average Edits Per Month :", self.getAverageEditsPerMonth())
        print("              Average Edits Per Year :", self.getAverageEditsPerYear())
        print()
        print("          Edits In The Past 24 Hours :", self.getEditsInPast24Hours())
        print("            Edits In The Past 7 Days :", self.getEditsInPast7Days())
        print("           Edits In The Past 30 Days :", self.getEditsInPast30Days())
        print("          Edits In The Past 365 Days :", self.getEditsInPast365Days())
        print()
        print("Edits Made By The Top 10% Of Editors :", self.getEditsByTop10Editors())
        print()
        print(" ----------------------------------- ")
    
    #charts
    def getMajorMinorGraph(self) :
        labels = ["Major edits","Minor Edits"]
        values = [self.getTotalEdits() - self.getMinorEdits(), self.getMinorEdits()]
        colors = ['#abd4eb', "#b2df8a"]
        explode = [0.01, 0.01]
        for i in range(len(labels)) :
            labels[i] = labels[i] + " · " + str(values[i]) + " (" + "{0:.1f}".format(100*values[i]/self.getTotalEdits()) + "%)"

        legend_elements = [ Line2D([0], [0], marker='o', color='w', markersize=15,
                    label=labels[i],  markerfacecolor=colors[i]) for i in range(len(labels))]

        plt.axis("equal")
        plt.pie(values, colors = colors, explode = explode, startangle=90, counterclock = False)
        plt.legend(labels, handles=legend_elements, loc="center left", fontsize = 12, frameon = False, bbox_to_anchor=(1, 0, 0.5, 1))

        plt.show()
    
    def getAccountIPGraph(self) :
        labels = ["Accounts","IPs"]
        values = [self.getTotalEdits() - self.getIPEdits(), self.getIPEdits()]
        colors = ['#abd4eb', "#b2df8a"]
        explode = [0.01, 0.01]
        for i in range(len(labels)) :
            labels[i] = labels[i] + " · " + str(values[i]) + " (" + "{0:.1f}".format(100*values[i]/self.getTotalEdits()) + "%)"

        legend_elements = [ Line2D([0], [0], marker='o', color='w', markersize=15,
                    label=labels[i],  markerfacecolor=colors[i]) for i in range(len(labels))]

        plt.axis("equal")
        plt.pie(values, colors = colors, explode = explode, startangle=90, counterclock = False)
        plt.legend(labels, handles=legend_elements, loc="center left", fontsize = 12, frameon = False, bbox_to_anchor=(1, 0, 0.5, 1))

        plt.show()
        
    def getTop10Bottom90Graph(self) :
        labels = ["Top 10% ","Bottom 90%"]
        values = [self.getEditsByTop10Editors(), self.getTotalEdits() - self.getEditsByTop10Editors()]
        colors = ['#abd4eb', "#b2df8a"]
        explode = [0.01, 0.01]
        for i in range(len(labels)) :
            labels[i] = labels[i] + " · " + str(values[i])+ " (" + "{0:.1f}".format(100*values[i]/self.getTotalEdits()) + "%)"

        legend_elements = [ Line2D([0], [0], marker='o', color='w', markersize=15,
                    label=labels[i],  markerfacecolor=colors[i]) for i in range(len(labels))]

        plt.axis("equal")
        plt.pie(values, colors = colors, explode = explode, startangle=90, counterclock = False)
        plt.legend(labels, handles=legend_elements, loc="center left", fontsize = 12, frameon = False, bbox_to_anchor=(1, 0, 0.5, 1))

        plt.show()
    
    def modifyEditors(self) :
        editorsArray = []
        for x in self.editors.keys() :
            di ={}
            di["username"] = x
            di["total edits"] = 0
            di["minor edits"] = 0
            di["first edit"] = None
            di["latest edit"] = None
            di["bytes added"] = 0
            editorsArray.append(di)
        
        for i in range(len(self.revisions)) :
            x = self.revisions[i]
            username = x['Contributors']['OwnerUserName']
            for editor in editorsArray :
                if editor["username"] == username :
                    editor["total edits"] += 1
                    editor["minor edits"] += 1 if 'minor' in x else 0
                    if editor["first edit"] == None :
                        editor["first edit"] = x['TimeStamp']['CreationDate'].replace('T', ' ')
                        
                    editor["latest edit"] = x['TimeStamp']['CreationDate'][:-1].replace('T', ' ')
                    if i != 0 and self.isOriginalRevision(x):
                        editor["bytes added"] += max(0, int(self.revisions[i]['Body']['Text']['@Bytes']) - int(self.revisions[i-1]['Body']['Text']['@Bytes']))
                    if i == 0 :
                        editor["bytes added"] += int(x['Body']['Text']['@Bytes'])
        editorsArray.sort(key = lambda x: x["first edit"], reverse = True)
        editorsArray.sort(key = lambda x: x["minor edits"], reverse = True)
        editorsArray.sort(key = lambda x: x["total edits"], reverse = True)
        return editorsArray
    
    def getTop10ByEditsGraph(self) :
        editors = self.modifyEditors()
        editors.sort(key = lambda x: x["total edits"], reverse = True)
        
        labels = [editors[i]["username"] for i in range(min(10, len(editors))) ]
        values = [editors[i]["total edits"] for i in range(len(labels))]
        colors = [ '#abd4eb', "#b2df8a", '#fb9a99', '#f3bf6f', '#cab2d6', '#cfb680', '#8dd3c7', '#fccde5', '#fff7a1', '#fc9272' ]
        explode = [0.01 for i in range(len(labels)) ]
        
        total = 0
        for value in values :
            total += value
            
        for i in range(len(labels)) :
            labels[i] = labels[i] + " · " + str(values[i]) + " (" + "{0:.1f}".format(100*values[i]/total) + "%)"

        legend_elements = [ Line2D([0], [0], marker='o', color='w', markersize=15,
                    label=labels[i],  markerfacecolor=colors[i]) for i in range(len(labels))]

        plt.axis("equal")
        plt.pie(values, radius = 1.5, colors = colors, explode = explode, startangle=90, counterclock = False)
        plt.legend(labels, handles=legend_elements, loc="center left", fontsize = 12, frameon = False, bbox_to_anchor=(1, 0, 0.5, 1))

        plt.show()
        
    def getTop10ByAddedTextGraph(self) :
        editors = self.modifyEditors()
        editors.sort(key = lambda x: x["bytes added"], reverse = True)
        
        labels = [editors[i]["username"] for i in range(min(10, len(editors))) ]
        values = [editors[i]["bytes added"] for i in range(len(labels))]
        colors = [ '#abd4eb', "#b2df8a", '#fb9a99', '#f3bf6f', '#cab2d6', '#cfb680', '#8dd3c7', '#fccde5', '#fff7a1', '#fc9272' ]
        explode = [0.01 for i in range(len(labels)) ]
        plt.pie(values, radius = 1.5, colors = colors, explode = explode, startangle=90, counterclock = False)
 
        total = 0
        for value in values :
            total += value
             
        for i in range(len(labels)) :
            labels[i] = labels[i] + " · " + str(values[i]) + " (" + "{0:.1f}".format(100*values[i]/total) + "%)"

        legend_elements = [ Line2D([0], [0], marker='o', color='w', markersize=15,
                    label=labels[i],  markerfacecolor=colors[i]) for i in range(len(labels))]

        plt.axis("equal")
        plt.legend(labels, handles=legend_elements, loc="center left", fontsize = 12, frameon = False, bbox_to_anchor=(1, 0, 0.5, 1))

        plt.show()
    
    def printTopEditors(self, count = 10) :
        editors = self.modifyEditors()[:count]
        t = PrettyTable(["Username", "Edits", "MinorEdits", "MinorEdits%", "First Edit", "Latest Edit", "Added(bytes)"])
        for x in editors :
            t.add_row([ x["username"], x["total edits"], x["minor edits"], "{0:.1f}".format(100*x["minor edits"]/x["total edits"]) + "%", x["first edit"], x["latest edit"], x["bytes added"]] )
        print(t)

