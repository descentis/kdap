#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 11:56:26 2019

@author: descentis
"""
import xml.etree.ElementTree as ET
import math
import time
import glob
import numpy as np
from multiprocessing import Process, Lock, Manager
from datetime import datetime
import re
from urllib.parse import quote
from html.entities import name2codepoint
import string
import psutil
import os
import mwparserfromhell
from nltk.tokenize import word_tokenize
import copy

class knolAnalysis(object):
    
    @staticmethod
    def get_process_memory():
        process = psutil.Process(os.getpid())
        return process.memory_info().rss

    @staticmethod
    def getRevision(file_name,n):
        tree = ET.parse(file_name)
        r = tree.getroot()
        revisionsDict = {}
        for child in r:
            if('KnowledgeData' in child.tag):
                root = child
        length = len(root.findall('Instance'))
        for each in root.iter('Instance'):
            instanceId = int(each.attrib['Id'])
            for child in each:
                if 'Body' in child.tag:
                    revisionsDict[instanceId] = child[0].text
    
    
        #n = int(input(str(length)+" Revisons found, enter the revision number to be loaded: "))
        original = n
        m = int((math.log(length)) ** 2)+1
        if n%m != 0:
            interval = n - (n%m) + 1
            n = n - interval + 1
        else:
            interval = n - (m-1)
            n = n - interval + 1
        
        
        count = interval
        prev_str = revisionsDict[count]
        result = prev_str
        while count < original:
            count += 1
            s = [x.replace("\n", "`").replace("-", "^") for x in prev_str.split(" ")]
            i = 0
            while(True):
                if i == len(s):
                    break;
                if s[i].isspace() or s[i] == '':
                    del s[i]
                else:	
                    i += 1	
        
            next_rev = revisionsDict[count]
            s2 = next_rev.split(" ")
            i = 0
            while(True):
                if i == len(s2):
                    break;
                if s2[i].isspace() or s2[i] == '':
                    del s2[i]
                else:	
                    i += 1	
        
            index = 0
            result = ""
            for x in s2:
                if x.isdigit():
                    for i in range(index, index+int(x)):
                        result += s[i].replace("`", "\n").replace("^", "-")
                        result += " "
                        index += 1
                elif x[0] == "'" and x[-1] == "'" and x[1:-1].isdigit():
        
                        result += x[1:-1].replace("`", "\n			").replace("^", "-")
                        result += " "
                else:
                    if x[0] == '-':
                        for i in range(index, index+int(x[1:])):
                            index += 1
                    else:
                        result += x.replace("`", "\n			").replace("^", "-")		
                        result += " "
        
            prev_str = result
            
        
        return result

    @staticmethod
    def dropSpans(spans, text):
        """
        Drop from text the blocks identified in :param spans:, possibly nested.
        """
        spans.sort()
        res = ''
        offset = 0
        for s, e in spans:
            if offset <= s:         # handle nesting
                if offset < s:
                    res += text[offset:s]
                offset = e
        res += text[offset:]
        return res

    @staticmethod
    def dropNested(text, openDelim, closeDelim):
        """
        A matching function for nested expressions, e.g. namespaces and tables.
        """
        openRE = re.compile(openDelim, re.IGNORECASE)
        closeRE = re.compile(closeDelim, re.IGNORECASE)
        # partition text in separate blocks { } { }
        spans = []                  # pairs (s, e) for each partition
        nest = 0                    # nesting level
        start = openRE.search(text, 0)
        if not start:
            return text
        end = closeRE.search(text, start.end())
        next = start
        while end:
            next = openRE.search(text, next.end())
            if not next:            # termination
                while nest:         # close all pending
                    nest -= 1
                    end0 = closeRE.search(text, end.end())
                    if end0:
                        end = end0
                    else:
                        break
                spans.append((start.start(), end.end()))
                break
            while end.end() < next.start():
                # { } {
                if nest:
                    nest -= 1
                    # try closing more
                    last = end.end()
                    end = closeRE.search(text, end.end())
                    if not end:     # unbalanced
                        if spans:
                            span = (spans[0][0], last)
                        else:
                            span = (start.start(), last)
                        spans = [span]
                        break
                else:
                    spans.append((start.start(), end.end()))
                    # advance start, find next close
                    start = next
                    end = closeRE.search(text, next.end())
                    break           # { }
            if next != start:
                # { { }
                nest += 1
        # collect text outside partitions
        return knolAnalysis.dropSpans(spans, text)

    @staticmethod
    def transform(wikitext):
        """
        Transforms wiki markup.
        @see https://www.mediawiki.org/wiki/Help:Formatting
        """
        # look for matching <nowiki>...</nowiki>
        nowiki = re.compile(r'<nowiki>.*?</nowiki>')
        res = ''
        cur = 0
        for m in nowiki.finditer(wikitext, cur):
            res += knolAnalysis.transform1(wikitext[cur:m.start()]) + wikitext[m.start():m.end()]
            cur = m.end()
        # leftover
        res += knolAnalysis.transform1(wikitext[cur:])
        return res

    @staticmethod
    def transform1(text):
        """Transform text not containing <nowiki>"""

        return knolAnalysis.dropNested(text, r'{{', r'}}')

    @staticmethod
    def makeExternalImage(url, alt=''):

        return alt

    @staticmethod
    def replaceExternalLinks(text):
        """
        https://www.mediawiki.org/wiki/Help:Links#External_links
        [URL anchor text]
        """
        wgUrlProtocols = [
            'bitcoin:', 'ftp://', 'ftps://', 'geo:', 'git://', 'gopher://', 'http://',
            'https://', 'irc://', 'ircs://', 'magnet:', 'mailto:', 'mms://', 'news:',
            'nntp://', 'redis://', 'sftp://', 'sip:', 'sips:', 'sms:', 'ssh://',
            'svn://', 'tel:', 'telnet://', 'urn:', 'worldwind://', 'xmpp:', '//'
        ]
        EXT_LINK_URL_CLASS = r'[^][<>"\x00-\x20\x7F\s]'
        ANCHOR_CLASS = r'[^][\x00-\x08\x0a-\x1F]'
        ExtLinkBracketedRegex = re.compile('\[(((?i)' + '|'.join(wgUrlProtocols) + ')' + EXT_LINK_URL_CLASS + r'+)' + r'\s*((?:' + ANCHOR_CLASS + r'|\[\[' + ANCHOR_CLASS + r'+\]\])' + r'*?)\]',
    re.S | re.U)

        EXT_IMAGE_REGEX = re.compile(
            r"""^(http://|https://)([^][<>"\x00-\x20\x7F\s]+)
            /([A-Za-z0-9_.,~%\-+&;#*?!=()@\x80-\xFF]+)\.((?i)gif|png|jpg|jpeg)$""",
            re.X | re.S | re.U)

        
        s = ''
        cur = 0
        for m in ExtLinkBracketedRegex.finditer(text):
            s += text[cur:m.start()]
            cur = m.end()
    
            url = m.group(1)
            label = m.group(3)
    
            # # The characters '<' and '>' (which were escaped by
            # # removeHTMLtags()) should not be included in
            # # URLs, per RFC 2396.
            # m2 = re.search('&(lt|gt);', url)
            # if m2:
            #     link = url[m2.end():] + ' ' + link
            #     url = url[0:m2.end()]
    
            # If the link text is an image URL, replace it with an <img> tag
            # This happened by accident in the original parser, but some people used it extensively
            m = EXT_IMAGE_REGEX.match(label)
            if m:
                label = knolAnalysis.makeExternalImage(label)
    
            # Use the encoded URL
            # This means that users can paste URLs directly into the text
            # Funny characters like ö aren't valid in URLs anyway
            # This was changed in August 2004
            s += label  # + trail
    
        return s + text[cur:]

    @staticmethod
    def unescape(text):
        """
        Removes HTML or XML character references and entities from a text string.
        :param text The HTML (or XML) source text.
        :return The plain text, as a Unicode string, if necessary.
        """
    
        def fixup(m):
            text = m.group(0)
            code = m.group(1)
            try:
                if text[1] == "#":  # character reference
                    if text[2] == "x":
                        return chr(int(code[1:], 16))
                    else:
                        return chr(int(code))
                else:  # named entity
                    return chr(name2codepoint[code])
            except:
                return text  # leave as is
    
        return re.sub("&#?(\w+);", fixup, text)

    @staticmethod
    def wiki2text(text):
        #
        # final part of internalParse().)
        #
        # $text = $this->doTableStuff( $text );
        # $text = preg_replace( '/(^|\n)-----*/', '\\1<hr />', $text );
        # $text = $this->doDoubleUnderscore( $text );
        # $text = $this->doHeadings( $text );
        # $text = $this->replaceInternalLinks( $text );
        # $text = $this->doAllQuotes( $text );
        # $text = $this->replaceExternalLinks( $text );
        # $text = str_replace( self::MARKER_PREFIX . 'NOPARSE', '', $text );
        # $text = $this->doMagicLinks( $text );
        # $text = $this->formatHeadings( $text, $origText, $isMain );


        syntaxhighlight = re.compile('&lt;syntaxhighlight .*?&gt;(.*?)&lt;/syntaxhighlight&gt;', re.DOTALL)
        
        
        # Drop tables
        # first drop residual templates, or else empty parameter |} might look like end of table.      
        text = knolAnalysis.dropNested(text, r'{{', r'}}')
        text = knolAnalysis.dropNested(text, r'{\|', r'\|}')

        switches = (
            '__NOTOC__',
            '__FORCETOC__',
            '__TOC__',
            '__TOC__',
            '__NEWSECTIONLINK__',
            '__NONEWSECTIONLINK__',
            '__NOGALLERY__',
            '__HIDDENCAT__',
            '__NOCONTENTCONVERT__',
            '__NOCC__',
            '__NOTITLECONVERT__',
            '__NOTC__',
            '__START__',
            '__END__',
            '__INDEX__',
            '__NOINDEX__',
            '__STATICREDIRECT__',
            '__DISAMBIG__'
        )
        # Handle bold/italic/quote

        bold_italic = re.compile(r"'''''(.*?)'''''")
        bold = re.compile(r"'''(.*?)'''")
        italic_quote = re.compile(r"''\"([^\"]*?)\"''")
        italic = re.compile(r"''(.*?)''")
        quote_quote = re.compile(r'""([^"]*?)""')
        magicWordsRE = re.compile('|'.join(switches))
        
 
    
       
        text = bold_italic.sub(r'\1', text)
        text = bold.sub(r'\1', text)
        text = italic_quote.sub(r'"\1"', text)
        text = italic.sub(r'"\1"', text)
        text = quote_quote.sub(r'"\1"', text)
        # residuals of unbalanced quotes
        text = text.replace("'''", '').replace("''", '"')

        # replace internal links
        text = knolAnalysis.replaceInternalLinks(text)

        # replace external links
        text = knolAnalysis.replaceExternalLinks(text)

        # drop MagicWords behavioral switches
        text = magicWordsRE.sub('', text)

        # ############### Process HTML ###############

        # turn into HTML, except for the content of <syntaxhighlight>
        res = ''
        cur = 0
        for m in syntaxhighlight.finditer(text):
            res += knolAnalysis.unescape(text[cur:m.start()]) + m.group(1)
            cur = m.end()
        text = res + knolAnalysis.unescape(text[cur:])
        return text

    @staticmethod
    def clean(text):
        """
        Removes irrelevant parts from :param: text.
        """

        selfClosingTags = ('br', 'hr', 'nobr', 'ref', 'references', 'nowiki')
        comment = re.compile(r'<!--.*?-->', re.DOTALL)
        selfClosing_tag_patterns = [
            re.compile(r'<\s*%s\b[^>]*/\s*>' % tag, re.DOTALL | re.IGNORECASE) for tag in selfClosingTags
            ]
        
        discardElements = [
            'gallery', 'timeline', 'noinclude', 'pre',
            'table', 'tr', 'td', 'th', 'caption', 'div',
            'form', 'input', 'select', 'option', 'textarea',
            'ul', 'li', 'ol', 'dl', 'dt', 'dd', 'menu', 'dir',
            'ref', 'references', 'img', 'imagemap', 'source', 'small',
            'sub', 'sup', 'indicator'
        ]        
        spaces = re.compile(r' {2,}')
        
        dots = re.compile(r'\.{4,}')
        
        placeholder_tags = {'math': 'formula', 'code': 'codice'}
        placeholder_tag_patterns = [
            (re.compile(r'<\s*%s(\s*| [^>]+?)>.*?<\s*/\s*%s\s*>' % (tag, tag), re.DOTALL | re.IGNORECASE),
             repl) for tag, repl in placeholder_tags.items()
            ]

        # Collect spans
        spans = []
        # Drop HTML comments
        for m in comment.finditer(text):
            spans.append((m.start(), m.end()))

        # Drop self-closing tags
        for pattern in selfClosing_tag_patterns:
            for m in pattern.finditer(text):
                spans.append((m.start(), m.end()))

        '''
        # Drop ignored tags
        for left, right in options.ignored_tag_patterns:
            for m in left.finditer(text):
                spans.append((m.start(), m.end()))
            for m in right.finditer(text):
                spans.append((m.start(), m.end()))
        '''

        # Bulk remove all spans
        text = knolAnalysis.dropSpans(spans, text)

        # Drop discarded elements
        for tag in discardElements:
            text = knolAnalysis.dropNested(text, r'<\s*%s\b[^>/]*>' % tag, r'<\s*/\s*%s>' % tag)


        text = knolAnalysis.unescape(text)

        # Expand placeholders
        for pattern, placeholder in placeholder_tag_patterns:
            index = 1
            for match in pattern.finditer(text):
                text = text.replace(match.group(), '%s_%d' % (placeholder, index))
                index += 1

        text = text.replace('<<', '«').replace('>>', '»')

        #############################################

        # Cleanup text
        text = text.replace('\t', ' ')
        text = spaces.sub(' ', text)
        text = dots.sub('...', text)
        text = re.sub(' (,:\.\)\]»)', r'\1', text)
        text = re.sub('(\[\(«) ', r'\1', text)
        text = re.sub(r'\n\W+?\n', '\n', text, flags=re.U)  # lines with only punctuations
        text = text.replace(',,', ',').replace(',.', '.')
        keep_tables = True
        if keep_tables:
            # the following regular expressions are used to remove the wikiml chartacters around table strucutures
            # yet keep the content. The order here is imporant so we remove certain markup like {| and then
            # then the future html attributes such as 'style'. Finally we drop the remaining '|-' that delimits cells.
            text = re.sub(r'!(?:\s)?style=\"[a-z]+:(?:\d+)%;\"', r'', text)
            text = re.sub(r'!(?:\s)?style="[a-z]+:(?:\d+)%;[a-z]+:(?:#)?(?:[0-9a-z]+)?"', r'', text)
            text = text.replace('|-', '')
            text = text.replace('|', '')

        '''
        if options.toHTML:
            text = cgi.escape(text)
        '''
        return text

    @staticmethod
    def getCleanText(text):
        text = knolAnalysis.transform(text)
        text = knolAnalysis.wiki2text(text)
        text = knolAnalysis.clean(text)

        return text        

    @staticmethod
    def findBalanced(text, openDelim=['[['], closeDelim=[']]']):
        """
        Assuming that text contains a properly balanced expression using
        :param openDelim: as opening delimiters and
        :param closeDelim: as closing delimiters.
        :return: an iterator producing pairs (start, end) of start and end
        positions in text containing a balanced expression.
        """
        openPat = '|'.join([re.escape(x) for x in openDelim])
        # pattern for delimiters expected after each opening delimiter
        afterPat = {o: re.compile(openPat + '|' + c, re.DOTALL) for o, c in zip(openDelim, closeDelim)}
        stack = []
        start = 0
        cur = 0
        # end = len(text)
        startSet = False
        startPat = re.compile(openPat)
        nextPat = startPat
        while True:
            next = nextPat.search(text, cur)
            if not next:
                return
            if not startSet:
                start = next.start()
                startSet = True
            delim = next.group(0)
            if delim in openDelim:
                stack.append(delim)
                nextPat = afterPat[delim]
            else:
                opening = stack.pop()
                # assert opening == openDelim[closeDelim.index(next.group(0))]
                if stack:
                    nextPat = afterPat[stack[-1]]
                else:
                    yield start, next.end()
                    nextPat = startPat
                    start = next.end()
                    startSet = False
            cur = next.end()

    
    @staticmethod
    def makeInternalLink(title, label):
        colon = title.find(':')
        keepLinks = False
        acceptedNamespaces = ['w', 'wiktionary', 'wikt']
        if colon > 0 and title[:colon] not in acceptedNamespaces:
            return ''
        if colon == 0:
            # drop also :File:
            colon2 = title.find(':', colon + 1)
            if colon2 > 1 and title[colon + 1:colon2] not in acceptedNamespaces:
                return ''
        if keepLinks:
            return '<a href="%s">%s</a>' % (quote(title.encode('utf-8')), label)
        else:
            return label


    @staticmethod
    def replaceInternalLinks(text):
        """
        Replaces internal links of the form:
        [[title |...|label]]trail
        with title concatenated with trail, when present, e.g. 's' for plural.
        See https://www.mediawiki.org/wiki/Help:Links#Internal_links
        """
        # call this after removal of external links, so we need not worry about
        # triple closing ]]].
        tailRE = re.compile('\w+')
        cur = 0
        res = ''
        for s, e in knolAnalysis.findBalanced(text):
            m = tailRE.match(text, e)
            if m:
                trail = m.group(0)
                end = m.end()
            else:
                trail = ''
                end = e
            inner = text[s + 2:e - 2]
            # find first |
            pipe = inner.find('|')
            if pipe < 0:
                title = inner
                label = title
            else:
                title = inner[:pipe].rstrip()
                # find last |
                curp = pipe + 1
                for s1, e1 in knolAnalysis.findBalanced(inner):
                    last = inner.rfind('|', curp, s1)
                    if last >= 0:
                        pipe = last  # advance
                    curp = e1
                label = inner[pipe + 1:].strip()
            res += text[cur:s] + knolAnalysis.makeInternalLink(title, label) + trail
            cur = end
        return res + text[cur:]


        
    
    @classmethod
    def wikiRetrieval(cls,file_name,n):
        tree = ET.parse(file_name)
        r = tree.getroot()
        revisionsDict = {}
        returnResult = []
        for child in r:
            if('KnowledgeData' in child.tag):
                root = child
        length = len(root.findall('Instance'))
        for each in root.iter('Instance'):
            instanceId = int(each.attrib['Id'])
            for child in each:
                if 'Body' in child.tag:
                    revisionsDict[instanceId] = child[0].text
    
    
        #n = int(input(str(length)+" Revisons found, enter the revision number to be loaded: "))
        original = n
        m = int((math.log(length)) ** 2)+1
        if n%m != 0:
            interval = n - (n%m) + 1
            n = n - interval + 1
        else:
            interval = n - (m-1)
            n = n - interval + 1
        
        
        count = interval
        prev_str = revisionsDict[count]
        result = prev_str
        returnResult.append(result)
        while count < original:
            count += 1
            s = [x.replace("\n", "`").replace("-", "^") for x in prev_str.split(" ")]
            i = 0
            while(True):
                if i == len(s):
                    break;
                if s[i].isspace() or s[i] == '':
                    del s[i]
                else:	
                    i += 1	
        
            next_rev = revisionsDict[count]
            s2 = next_rev.split(" ")
            i = 0
            while(True):
                if i == len(s2):
                    break;
                if s2[i].isspace() or s2[i] == '':
                    del s2[i]
                else:	
                    i += 1	
        
            index = 0
            result = ""
            for x in s2:
                if x.isdigit():
                    for i in range(index, index+int(x)):
                        result += s[i].replace("`", "\n").replace("^", "-")
                        result += " "
                        index += 1
                elif x[0] == "'" and x[-1] == "'" and x[1:-1].isdigit():
        
                        result += x[1:-1].replace("`", "\n			").replace("^", "-")
                        result += " "
                else:
                    if x[0] == '-':
                        for i in range(index, index+int(x[1:])):
                            index += 1
                    else:
                        result += x.replace("`", "\n			").replace("^", "-")		
                        result += " "
        
            prev_str = result
            returnResult.append(result)
        
        return returnResult
    
    
    def allRevisions(self,file_name,root,tree):
        
        
        '''
        for child in r:
            if('KnowledgeData' in child.tag):
                root = child
        '''
        
         
        for child in root:
            if('KnowledgeData' in child.tag):                
                if('Wiki' in child.attrib['Type']):
                    length = len(child.findall('Instance'))        
                    if length == 1:
                        print("No revisions found, generate revisions from xmltoknml.py first")
                        exit()
                    
                    revisionList = []
                    k = int((math.log(length)) ** 2)
                    for i in range(k+1,(math.ceil(length/(k+1))-1)*(k+1)+1,(k+1)):
                        revisionList.append(i)
                        
                    revisionList.append(length)
                #print(revisionList)

        
        
       
        return revisionList
        
   
    @classmethod     
    def getAllRevisions(cls,file_name):
        tree = ET.parse(file_name)
        root = tree.getroot()
        

        for child in root:
            if('KnowledgeData' in child.tag):
                #print(child.attrib['Type'])
                if('Wiki' in child.attrib['Type']):
                    revisionsList = cls.allRevisions(cls,file_name,root,tree)
                elif('QA' in child.attrib['Type']):
                    revisionsList = child
                
        return revisionsList
    
    
    '''
    This is dummy function to refer how to get all the revisions of wiki    
    '''
    def getRev(self, file_name):
        cRev = 1
        #print(revisionList)
        revisionList = self.getAllRevisions(file_name)
        for rev in revisionList:
            revisions = self.wikiRetrieval(file_name,rev)
            #print(len(revisions))
            for revision in revisions:
                # write your analysis for each revision
                x = 0
                '''
                with open('dummy.txt','a') as myFile:
                    myFile.write(revision+'\n')
                    myFile.write(str(cRev)+'\n')
                '''
                cRev+=1

     
    @classmethod           
    def countRev(cls,file_name, *args, **kwargs):
        tree = ET.parse(file_name)
        r = tree.getroot()

        for child in r:
            if('KnowledgeData' in child.tag):
                root = child        

        length = len(root.findall('Instance'))
        if(kwargs.get('revisionLength')!=None):            
            kwargs['revisionLength'][file_name] = length
            #print(kwargs['revisionLength'])
        else:
            return length        


    @staticmethod        
    def countRevInFiles(*args, **kwargs):
        '''
        This piece of code is to ensure the multiprocessing
        '''
        if(kwargs.get('file_list')!=None):
            file_list = kwargs['file_list']
        
        elif(kwargs.get('dir_path')!=None):
            dir_path = kwargs['dir_path']
            
            file_list = glob.glob(dir_path+'/*.knolml')
        
        if(kwargs.get('c_num')!=None):
            cnum = kwargs['c_num']
        else:
            cnum = 24           # Bydefault it is 24
        
        fileNum = len(file_list)
        
        fileList = []
        if(fileNum<cnum):
            for f in file_list:
                fileList.append([f])
        
        else:           

            f = np.array_split(file_list,cnum)
            for i in f:
                fileList.append(i.tolist())        
        
        

        
        manager = Manager()
        revisionLength = manager.dict()

        l = Lock()
        processDict = {}
        if(fileNum<cnum):
            pNum = fileNum
        else:
            pNum = cnum
        for i in range(pNum):
            processDict[i+1] = Process(target=knolAnalysis.countRev, args=(fileList[i]), kwargs={'revisionLength': revisionLength,'l': l})
        
        for i in range(pNum):
            processDict[i+1].start()
        
        for i in range(pNum):
            processDict[i+1].join()  
            
        return revisionLength


    @staticmethod
    def countUsers(*args, **kwargs):
        #print(file_name)
        if(kwargs.get('file_path')!=None):
            file_name = kwargs['file_path']            
            tree = ET.parse(file_name)            
            root = tree.getroot()

           

            uList = []
            for child in root:
                if('KnowledgeData' in child.tag):
                    for ch in child:
                        if('Instance' in ch.tag):
                            for newch in ch:
                                if('Contributors' in newch.tag):
                                    for chi in newch:
                                        if('OwnerUserId' in chi.tag):
                                            if(chi.text not in uList):
                                                uList.append(chi.text)
            return uList
            
        elif(kwargs.get('file_name')!=None):
            file_name = kwargs['file_name']
            for f in file_name:
                tree = ET.parse(f)            
                root = tree.getroot()
                uList = []
                for child in root:
                    if('KnowledgeData' in child.tag):
                        for ch in child:
                            if('Instance' in ch.tag):
                                for newch in ch:
                                    if('Contributors' in newch.tag):
                                        for chi in newch:
                                            if('OwnerUserId' in chi.tag):
                                                if(chi.text not in uList):
                                                    uList.append(chi.text)
                if(kwargs.get('users')!=None):
                    kwargs['users'][f] = uList
                    #print(kwargs['revisionLength'])
        else:
            print("No arguments provided")

    @staticmethod
    def countUsersInFiles(*args, **kwargs):

        if(kwargs.get('file_list')!=None):
            file_list = kwargs['file_list']
        
        elif(kwargs.get('dir_path')!=None):
            dir_path = kwargs['dir_path']
            
            file_list = glob.glob(dir_path+'/*.knolml')
        
        
        if(kwargs.get('c_num')!=None):
            cnum = kwargs['c_num']
        else:
            cnum = 24           # Bydefault it is 24
        
        fileNum = len(file_list)
        
        fileList = []
        if(fileNum<cnum):
            for f in file_list:
                fileList.append([f])
        
        else:           

            f = np.array_split(file_list,cnum)
            for i in f:
                fileList.append(i.tolist())        
        
        
        manager = Manager()
        usersList = manager.dict()

        l = Lock()
        processDict = {}
        if(fileNum<cnum):
            pNum = fileNum
        else:
            pNum = cnum
        for i in range(pNum):            
            processDict[i+1] = Process(target=knolAnalysis.countUsers, kwargs={'file_name':fileList[i],'users': usersList,'l': l})
        
        for i in range(pNum):
            processDict[i+1].start()
        
        for i in range(pNum):
            processDict[i+1].join()  
            
        return usersList


    @staticmethod
    def getKnowledgeAge(*args, **kwargs):
        
        if(kwargs.get('l')!=None):
            l = kwargs['l']
        
        if(kwargs.get('file_path')!=None):
            
            file_name = kwargs['file_path']            
            tree = ET.parse(file_name)            
            root = tree.getroot()    
            
            date_format = "%Y-%m-%dT%H:%M:%S.%f"
            flag = 0
            for child in root:
                if('KnowledgeData' in child.tag):
                    for ch1 in child:
                        if('Instance' in ch1.tag):
                            for ch2 in ch1:
                                if('TimeStamp' in ch2.tag):
                                    for ch3 in ch2:
                                        if('CreationDate' in ch3.tag):
                                            firstDate = datetime.strptime(ch3.text, date_format)
                                            flag = 1
                if(flag):
                    break
            
            currentDate = datetime.strptime(datetime.today().strftime(date_format), date_format)
            
            articleAge = currentDate - firstDate
            return articleAge
        
        elif(kwargs.get('file_name')!=None):
            file_name = kwargs['file_name']
            for f in file_name:
                tree = ET.parse(f)            
                root = tree.getroot()    
                
                date_format = "%Y-%m-%dT%H:%M:%S.%f"
                flag = 0
                for child in root:
                    if('KnowledgeData' in child.tag):
                        for ch1 in child:
                            if('Instance' in ch1.tag):
                                for ch2 in ch1:
                                    if('TimeStamp' in ch2.tag):
                                        for ch3 in ch2:
                                            if('CreationDate' in ch3.tag):
                                                firstDate = datetime.strptime(ch3.text, date_format)
                                                flag = 1
                    if(flag):
                        break
                
                currentDate = datetime.strptime(datetime.today().strftime(date_format), date_format)
                
                articleAge = currentDate - firstDate
                if(kwargs.get('articleAge')!=None):
                    kwargs['articleAge'][f] = articleAge
                
     
    @staticmethod
    def getAgeOfKnowledge(*args, **kwargs):

        '''
        This piece of code is to ensure the multiprocessing
        '''
        if(kwargs.get('file_list')!=None):
            file_list = kwargs['file_list']
        
        elif(kwargs.get('dir_path')!=None):
            dir_path = kwargs['dir_path']
            
            file_list = glob.glob(dir_path+'/*.knolml')
        
        fileNum = len(file_list)
        
        if(kwargs.get('c_num')!=None):
            cnum = kwargs['c_num']
        elif(fileNum<24):
            cnum = fileNum+1           # Bydefault it is 24
        else:
            cnum = 24
        
        
        fileList = []
        if(fileNum<cnum):
            for f in file_list:
                fileList.append([f])
            
        else:           

            f = np.array_split(file_list,cnum)
            for i in f:
                fileList.append(i.tolist())        
        
        

        
        manager = Manager()
        ageList = manager.dict()

        l = Lock()
        processDict = {}
        if(fileNum<cnum):
            pNum = fileNum
        else:
            pNum = cnum
        for i in range(pNum):
            processDict[i+1] = Process(target=knolAnalysis.getKnowledgeAge, kwargs={'file_name':fileList[i],'articleAge': ageList,'l': l})
        
        for i in range(pNum):
            processDict[i+1].start()
        
        for i in range(pNum):
            processDict[i+1].join()  
            
        return ageList        
    
    
    @staticmethod
    def knowledgeByDate(file_name, first_date, *args, **kwargs):
        
        if(kwargs.get('l')!=None):
            l = kwargs['l']
        
        fe = 0
        d_f = "%Y-%m-%d"
        date_format = "%Y-%m-%dT%H:%M:%S.%f"
        first_date = datetime.strptime(first_date, d_f)
        if(kwargs.get('end_date')!=None):
            end_date = kwargs['end_date']
            end_date = datetime.strptime(end_date, d_f)
            fe=1
                        
        tree = ET.parse(file_name)            
        root = tree.getroot()
        length = 0
        revList = []
        dummyList = []
        flag = 0
        wikiFlag = 0
        for child in root:
            if('KnowledgeData' in child.tag):
                length = len(child.findall('Instance'))
                if('Wiki' in child.attrib['Type']):
                    wikiFlag = 1
                for ch1 in child:
                    if('Instance' in ch1.tag):
                        instanceId = ch1.attrib['Id']
                        for ch2 in ch1:
                            if('TimeStamp' in ch2.tag):
                                for ch3 in ch2:
                                    if('CreationDate' in ch3.tag):
                                        firstDate = datetime.strptime(ch3.text, date_format)
                                        if(firstDate >= first_date):
                                            flag=1
                                            
                                        
                                        if(fe==1 and firstDate>end_date):
                                            flag=0
                            
                            if('Body' in ch2.tag):
                                for ch4 in ch2:
                                    if('Text' in ch4.tag and flag==1):
                                        if(wikiFlag==1):
                                            dummyList.append(int(instanceId))
                                        else:
                                            revList.append(ch4.text)
        
        if(wikiFlag==1):
            k = int((math.log(length)) ** 2)
            for i in range(k+1,(math.ceil(length/(k+1))-1)*(k+1)+1,(k+1)):
                if(i in dummyList):
                    revList.append(i)
            if(length in dummyList):
                revList.append(length)
        return revList

    @staticmethod
    def getUrl(*args, **kwargs):
        
        href_regex = r'href=[\'"]?([^\'" >]+)'
        if(kwargs.get('l')!=None):
            l = kwargs['l']
        
        if(kwargs.get('file_path')!=None):
            
            file_name = kwargs['file_path']            
            tree = ET.parse(file_name)            
            root = tree.getroot()    
            
            urlList = []
            for child in root:
                if('KnowledgeData' in child.tag):
                    if('Wiki' in child.attrib['Type'] and 'revision' in child.attrib['Type']):
                        length = len(child.findall('Instance'))
                        revision = knolAnalysis.getRevision(file_name,length)
                        urls = re.findall(href_regex, revision)
                        for ur in urls:
                            urlList.append(ur)
                        
                        return urlList
                        
                    for ch1 in child:
                        if('Instance' in ch1.tag):
                            for ch2 in ch1:
                                if('Body' in ch2.tag):
                                    for ch3 in ch2:
                                        if('Text' in ch3.tag):
                                            urls = re.findall(href_regex, ch3.text)
                                            
                                            for ur in urls:
                                                urlList.append(ur)                                            
            
            return urlList
        
        elif(kwargs.get('file_name')!=None):
            file_name = kwargs['file_name']
            for f in file_name:
                tree = ET.parse(f)            
                root = tree.getroot()    
                urlList = []
                for child in root:
                    if('KnowledgeData' in child.tag):
                        for ch1 in child:
                            if('Instance' in ch1.tag):
                                for ch2 in ch1:
                                    if('Body' in ch2.tag):
                                        for ch3 in ch2:
                                            if('Text' in ch3.tag):
                                                urls = re.findall(href_regex, ch3.text)
                                                
                                                for ur in urls:
                                                    urlList.append(ur)                                            
                if(kwargs.get('url_list')!=None):
                    kwargs['url_list'][f] = urlList


    @staticmethod
    def countWords(*args, **kwargs):
        #t1 = time.time()
        if(kwargs.get('l')!=None):
            l = kwargs['l']
        if(kwargs.get('lastRev')!=None):
            lastRev = kwargs['lastRev']
        dummyDict = {}
        if(kwargs.get('file_path')!=None):
            
            file_name = kwargs['file_path']            
            tree = ET.parse(file_name)            
            root = tree.getroot()    
            wordCount = 0
            for child in root:
                if('KnowledgeData' in child.tag):
                    if('Wiki' in child.attrib['Type']):
                        if(lastRev):
                            length = len(child.findall('Instance'))
                            revision = knolAnalysis.getRevision(file_name,length)
                            Text = knolAnalysis.getCleanText(revision)
                            wordNum = len(re.sub('['+string.punctuation+']', '', Text).split())
                            wordCount+=wordNum                        
                        else:
                            revisionList = knolAnalysis.getAllRevisions(file_name)
                            for rev in revisionList:
                                revisions = knolAnalysis.wikiRetrieval(file_name,rev)
                                for revision in revisions:
                                    Text = knolAnalysis.getCleanText(revision)
                                    wordNum = len(re.sub('['+string.punctuation+']', '', Text).split())
                                    wordCount+=wordNum
                                #print(len(revisions))
                                #for revision in revisions:
                    elif('QA' in child.attrib['Type']):
                        print('yes')
                        if(lastRev):
                            for ch1 in child:
                                if('Instance' in ch1.tag):
                                    for ch2 in ch1:
                                        if('Body' in ch2.tag):
                                            for ch3 in ch2:
                                                if('Text' in ch3.tag):
                                                    Text = ch3.text
                        
                        
                        Text = knolAnalysis.getCleanText(Text)
                        wordNum = len(re.sub('['+string.punctuation+']', '', Text).split())
                        
                            
            
            if(kwargs.get('wordCount')!=None):
                kwargs['wordCount'][file_name] = wordCount
            

                                    
                        
            
        
        elif(kwargs.get('file_name')!=None):
            #print('yes')
            file_name = kwargs['file_name']
            for f in file_name:
                tree = ET.parse(f)            
                root = tree.getroot()                                                    
                wordCount = 0
                for child in root:
                    if('KnowledgeData' in child.tag):
                        if('Wiki' in child.attrib['Type']):

                            if(lastRev):
                                length = len(child.findall('Instance'))
                                revision = knolAnalysis.getRevision(f,length)
                                Text = knolAnalysis.getCleanText(revision)
                                wordNum = len(re.sub('['+string.punctuation+']', '', Text).split())
                                wordCount+=wordNum                                    
                            
                            else:
                                revisionList = knolAnalysis.getAllRevisions(f)
                                for rev in revisionList:
                                    revisions = knolAnalysis.wikiRetrieval(f,rev)
                                    for revision in revisions:
                                        Text = knolAnalysis.getCleanText(revision)
                                        wordNum = len(re.sub('['+string.punctuation+']', '', Text).split())
                                        wordCount+=wordNum
                                        
                                        
                        elif('QA' in child.attrib['Type']):
                            if(lastRev):
                                for ch1 in child:
                                    if('Instance' in ch1.tag):
                                        for ch2 in ch1:
                                            if('Body' in ch2.tag):
                                                for ch3 in ch2:
                                                    if('Text' in ch3.tag):
                                                        Text = ch3.text
                            
                            
                            Text = knolAnalysis.getCleanText(Text)
                            wordNum = len(re.sub('['+string.punctuation+']', '', Text).split())
                            
                                  
                
                if(kwargs.get('wordCount')!=None):
                    kwargs['wordCount'][f] = wordCount
                else:
                    #x = 0
                    dummyDict[f] = wordCount
                
            
            #t2 = time.time()
            #print(t2-t1)

    @staticmethod
    def countAllWords(*args, **kwargs):
        #t1 = time.time()
        if(kwargs.get('file_list')!=None):
            file_list = kwargs['file_list']
            
        elif(kwargs.get('dir_path')!=None):
            dir_path = kwargs['dir_path']
            
            file_list = glob.glob(dir_path+'/*.knolml')
        
        if(kwargs.get('last_rev')!=None):
            if(kwargs['last_rev']==True):
                lastRev = True
        else:
            lastRev = False
            
        fileNum = len(file_list)
        
        if(kwargs.get('c_num')!=None):
            cnum = kwargs['c_num']
        elif(fileNum<24):
            cnum = fileNum+1           # Bydefault it is 24
        else:
            cnum = 24
        
        
        fileList = []
        if(fileNum<cnum):
            for f in file_list:
                fileList.append([f])
            
        else:           

            f = np.array_split(file_list,cnum)
            for i in f:
                fileList.append(i.tolist())        
        
        

        
        manager = Manager()
        countList = manager.dict()

        l = Lock()
        processDict = {}
        if(fileNum<cnum):
            pNum = fileNum
        else:
            pNum = cnum
        for i in range(pNum):
            processDict[i+1] = Process(target=knolAnalysis.countWords, kwargs={'file_name':fileList[i],'wordCount': countList, 'lastRev':lastRev,'l': l})
            #processDict[i+1] = Process(target=self.countWords, kwargs={'file_name':fileList[i], 'lastRev':lastRev,'l': l})
        for i in range(pNum):
            processDict[i+1].start()
        
        for i in range(pNum):
            processDict[i+1].join()  
        
        '''
        t2 = time.time()
        print(t2-t1)
        '''
        return countList 
        

    @staticmethod
    def Infobox(*args, **kwargs):
        if kwargs.get('file_path') != None:
            file_name = kwargs['file_path']
            tree = ET.parse(file_name)
            root = tree.getroot()

            for child in root:
                if('KnowledgeData' in child.tag):
                    root = child

            try:
                revisionId = kwargs['revision_id']
            except:
                revisionId = len(root.findall('Instance'))

            wikiText = knolAnalysis.getRevision(file_name, revisionId)

            if wikiText.find('{{Infobox') != -1:
                return 1
            else:
                return 0


        elif kwargs.get('file_name') != None:
            file_name = kwargs['file_name']
            for f in file_name:
                tree = ET.parse(f)
                root = tree.getroot()

                for child in root:
                    if('KnowledgeData' in child.tag):
                        root = child

                try:
                    revisionId = kwargs['revision_id'][f]
                except:
                    revisionId = len(root.findall('Instance'))

                wikiText = knolAnalysis.getRevision(f, revisionId)

                if wikiText.find('{{Infobox') != -1:
                    check = 1
                else:
                    check = 0

                if(kwargs.get('Infobox')!=None):
                    kwargs['Infobox'][f] = check

    @staticmethod
    def checkInfobox(*args, **kwargs):

        '''
        This piece of code is to ensure the multiprocessing
        '''
        if(kwargs.get('file_list')!=None):
            file_list = kwargs['file_list']

        elif(kwargs.get('dir_path')!=None):
            dir_path = kwargs['dir_path']

            file_list = glob.glob(dir_path+'/*.knolml')

        if kwargs.get('revision_id') != None:
            revisionId = kwargs['revision_id']
        else:
            revisionId = None

        fileNum = len(file_list)

        if(kwargs.get('c_num')!=None):
            cnum = kwargs['c_num']
        elif(fileNum<24):
            cnum = fileNum+1           # Bydefault it is 24
        else:
            cnum = 24

        fileList = []
        if(fileNum<cnum):
            for f in file_list:
                fileList.append([f])

        else:
            f = np.array_split(file_list,cnum)
            for i in f:
                fileList.append(i.tolist())        

        manager = Manager()
        Infobox = manager.dict()

        l = Lock()
        processDict = {}
        if(fileNum<cnum):
            pNum = fileNum
        else:
            pNum = cnum
        for i in range(pNum):
            processDict[i+1] = Process(target=knolAnalysis.Infobox, kwargs={'file_name':fileList[i],'Infobox': Infobox,'l': l, 'revision_id': revisionId})

        for i in range(pNum):
            processDict[i+1].start()

        for i in range(pNum):
            processDict[i+1].join()  
   
        return Infobox


    @staticmethod
    def countImages(*args, **kwargs):
        if kwargs.get('file_path') != None:
            file_name = kwargs['file_path']
            tree = ET.parse(file_name)
            root = tree.getroot()

            for child in root:
                if('KnowledgeData' in child.tag):
                    root = child

            try:
                revisionId = kwargs['revision_id']
            except:
                revisionId = len(root.findall('Instance'))

            wikiText = knolAnalysis.getRevision(file_name, revisionId)

            countImages = 0
            imageFormates = ['.jpg','.jpeg','.svg','.gif','.png','.bmp','.tiff']
            for image in imageFormates:
                countImages += wikiText.count(image)

            return countImages  


        elif kwargs.get('file_name') != None:
            file_name = kwargs['file_name']
            count = 0
            imageFormates = ['.jpg','.jpeg','.svg','.gif','.png','.bmp','.tiff']
            for f in file_name:
                tree = ET.parse(f)
                root = tree.getroot()

                for child in root:
                    if('KnowledgeData' in child.tag):
                        root = child

                try:
                    revisionId = kwargs['revision_id'][f]
                except:
                    revisionId = len(root.findall('Instance'))

                wikiText = knolAnalysis.getRevision(f, revisionId)
                count += 1

                countImages = 0
                for image in imageFormates:
                    countImages += wikiText.count(image)

                if(kwargs.get('images')!=None):
                    kwargs['images'][f] = countImages


    @staticmethod
    def getNumberOfImages(*args, **kwargs):

        '''
        This piece of code is to ensure the multiprocessing
        '''
        if(kwargs.get('file_list')!=None):
            file_list = kwargs['file_list']

        elif(kwargs.get('dir_path')!=None):
            dir_path = kwargs['dir_path']

            file_list = glob.glob(dir_path+'/*.knolml')

        if kwargs.get('revision_id') != None:
            revisionId = kwargs['revision_id']
        else:
            revisionId = None

        fileNum = len(file_list)

        if(kwargs.get('c_num')!=None):
            cnum = kwargs['c_num']
        elif(fileNum<24):
            cnum = fileNum+1           # Bydefault it is 24
        else:
            cnum = 24


        fileList = []
        if(fileNum<cnum):
            for f in file_list:
                fileList.append([f])
  
        else:
            f = np.array_split(file_list,cnum)
            for i in f:
                fileList.append(i.tolist())        


        manager = Manager()
        Images = manager.dict()

        l = Lock()
        processDict = {}
        if(fileNum<cnum):
            pNum = fileNum
        else:
            pNum = cnum
        for i in range(pNum):
            processDict[i+1] = Process(target=knolAnalysis.countImages, kwargs={'file_name':fileList[i],'images': Images,'l': l, 'revision_id': revisionId})

        for i in range(pNum):
            processDict[i+1].start()

        for i in range(pNum):
            processDict[i+1].join()

        return Images


    @staticmethod
    def gini(array):
        array = array.flatten()
        if np.amin(array) < 0:
            array -= np.amin(array)
        for i in array:
            i += 0.0000001
        array = np.sort(array)
        index = np.arange(1,array.shape[0]+1)
        n = array.shape[0]
        return ((np.sum((2 * index - n  - 1) * array)) / (n * np.sum(array)))


    @staticmethod
    def getContributions(file_name):
        tree = ET.parse(file_name)
        root = tree.getroot()

        for child in root:
            if('KnowledgeData' in child.tag):
                root = child

        contributors = {}
        #editor=''
        for child in root:
            if('Instance' in child.tag):
                for newch in child:
                    if('Contributors' in newch.tag):
                        for chi in newch:
                            if('OwnerUserId' in chi.tag):
                                editor = chi.text

                    if('Body' in newch.tag):
                        for chi in newch:
                            if('Text' in chi.tag):
                                editLength = int(chi.attrib['Bytes'])

                try:
                    if editor not in contributors:
                        contributors[editor] = editLength
                    else:
                        contributors[editor] += editLength
                except:
                    #print(file_name)
                    continue

        s = []
        for each in contributors:
            s.append(float(contributors[each]))

        return s


    @staticmethod
    def localGiniCoefficient(*args, **kwargs):
        if kwargs.get('file_path') != None:
            file_name = kwargs['file_path']
            p = np.array(knolAnalysis.getContributions(file_name))
            giniValue = knolAnalysis.gini(p)
            return giniValue

        elif kwargs.get('file_name') != None:
            file_name = kwargs['file_name']
            for f in file_name:
                p = np.array(knolAnalysis.getContributions(f))
                if(len(p)==0):
                    giniValue = -1
                else:
                    giniValue = knolAnalysis.gini(p)

                if(kwargs.get('GiniValues')!=None):
                    kwargs['GiniValues'][f] = giniValue


    @staticmethod
    def getLocalGiniCoefficient(*args, **kwargs):
        if(kwargs.get('file_list')!=None):
            file_list = kwargs['file_list']

        elif(kwargs.get('dir_path')!=None):
            dir_path = kwargs['dir_path']

            file_list = glob.glob(dir_path+'/*.knolml')

        if kwargs.get('revision_id') != None:
            revisionId = kwargs['revision_id']
        else:
            revisionId = None

        fileNum = len(file_list)

        if(kwargs.get('c_num')!=None):
            cnum = kwargs['c_num']
        elif(fileNum<24):
            cnum = fileNum+1           # Bydefault it is 24
        else:
            cnum = 24


        fileList = []
        if(fileNum<cnum):
            for f in file_list:
                fileList.append([f])

        else:
            f = np.array_split(file_list,cnum)
            for i in f:
                fileList.append(i.tolist())


        manager = Manager()
        GiniValues = manager.dict()

        l = Lock()
        processDict = {}
        if(fileNum<cnum):
            pNum = fileNum
        else:
            pNum = cnum
        for i in range(pNum):
            processDict[i+1] = Process(target=knolAnalysis.localGiniCoefficient, kwargs={'file_name':fileList[i],'GiniValues': GiniValues,'l': l})

        for i in range(pNum):
            processDict[i+1].start()

        for i in range(pNum):
            processDict[i+1].join()
        
        return GiniValues
    

    @staticmethod
    def globalGini(*args, **kwargs):
        if kwargs.get('file_name') != None:
            file_name = kwargs['file_name']
            
        if(kwargs.get('l')!=None):
            l = kwargs['l']

        if(kwargs.get('contributors')==None):
            contributors = {}
        for f in file_name:
            tree = ET.parse(f)
            root = tree.getroot()

            for child in root:
                if('KnowledgeData' in child.tag):
                    root = child
            editor=''
            for child in root:
                if('Instance' in child.tag):
                    for newch in child:
                        if('Contributors' in newch.tag):
                            for chi in newch:
                                if('OwnerUserId' in chi.tag):
                                    editor = chi.text
                                elif('LastEditorUserId' in chi.tag):
                                    editor = chi.text

                        if('Body' in newch.tag):
                            for chi in newch:
                                if('Text' in chi.tag):
                                    editLength = int(chi.attrib['Bytes'])
                                    
                    if(kwargs.get('contributors')!=None):
                        if kwargs['contributors'].get(editor)==None:
                            #kwargs['contributors'][editor] = editLength
                            x = 0
                        else:
                            #kwargs['contributors'][editor] += editLength
                            x=1
                    
                    else:
                        if contributors.get(editor)==None:
                            contributors[editor] = editLength
                        else:
                            contributors[editor] += editLength
                            
        
        
        
     
        #print(t2-t1)
        
        if(kwargs.get('contributors')==None):
            s = []
            for each in contributors:
                s.append(float(contributors[each]))
    
            p = np.array(s)
            giniValue = self.gini(p)
            return giniValue            
    
    @staticmethod    
    def globalGiniCoefficient(*args, **kwargs):
        
        if(kwargs.get('file_list')!=None):
            file_list = kwargs['file_list']

        elif(kwargs.get('dir_path')!=None):
            dir_path = kwargs['dir_path']

            file_list = glob.glob(dir_path+'/*.knolml')

        fileNum = len(file_list)

        if(kwargs.get('c_num')!=None):
            cnum = kwargs['c_num']
        elif(fileNum<24):
            cnum = fileNum+1           # Bydefault it is 24
        else:
            cnum = 24


        fileList = []
        if(fileNum<cnum):
            for f in file_list:
                fileList.append([f])

        else:
            f = np.array_split(file_list,cnum)
            for i in f:
                fileList.append(i.tolist())


        manager = Manager()
        contributors = manager.dict()

        l = Lock()
        processDict = {}
        if(fileNum<cnum):
            pNum = fileNum
        else:
            pNum = cnum
        for i in range(pNum):
            processDict[i+1] = Process(target=knolAnalysis.globalGini, kwargs={'file_name':fileList[i],'contributors': contributors,'l': l})

        for i in range(pNum):
            processDict[i+1].start()

        for i in range(pNum):
            processDict[i+1].join()



        s = []
        for key,items in contributors.items():
            s.append(float(contributors[key]))

        p = np.array(s)
        giniValue = knolAnalysis.gini(p)
        return giniValue
 
    @staticmethod
    def revisionEdits(file_name, slab):
        tree = ET.parse(file_name)
        root = tree.getroot()

        result = {
            'Content Added': 0,
            'Content Deleted': 0,
            'Content Reorganised': 0,
            'Hyperlink Added': 0,
            'Hyperlink Deleted': 0,
            'Hyperlink Fixed': 0
        }
        for child in root:
            if('KnowledgeData' in child.tag):
                root = child

        if 'Wiki' in root.attrib['Type']:
            length = len(root.findall('Instance'))
            revlength = int(length/20)
            prevRevision = ''
            prevTotalLinks = []
            count = 1
            slabNo = 1 
            slabs = {}
            revisionList = knolAnalysis.getAllRevisions(file_name)
            for rev in revisionList:
                revisions = knolAnalysis.wikiRetrieval(file_name,rev)
                for revision in revisions:
                    currRevision = revision

                    code = mwparserfromhell.parse(currRevision)
                    externalLinks = code.filter_external_links()
                    wikiLinks = code.filter_wikilinks()

                    for i in range(len(externalLinks)):
                        externalLinks[i] = str(externalLinks[i])
                    for i in range(len(wikiLinks)):
                        wikiLinks[i] = str(wikiLinks[i])

                    externalLinks = list(set(externalLinks))
                    wikiLinks = list(set(wikiLinks))
                    totalLinks = []
                    for each in externalLinks:
                        totalLinks.append(each)
                    for each in wikiLinks:
                        totalLinks.append(each)

                    if totalLinks != prevTotalLinks:
                        if len(totalLinks) > len(prevTotalLinks):
                            result['Hyperlink Added'] += 1
                        elif len(totalLinks) < len(prevTotalLinks):
                            result['Hyperlink Deleted'] += 1
                        else:
                            result['Hyperlink Fixed'] += 1

                    if currRevision != prevRevision:
                        if len(word_tokenize(currRevision)) > len(word_tokenize(prevRevision)):
                            result['Content Added'] += 1
                        elif len(word_tokenize(currRevision)) < len(word_tokenize(prevRevision)):
                            result['Content Deleted'] += 1
                        else:
                            result['Content Reorganised'] += 1

                    prevRevision = currRevision
                    prevTotalLinks = totalLinks

                    if count%revlength == 0:
                        slabs['Slab'+str(slabNo)] = copy.deepcopy(result)
                        slabNo += 1

                    count += 1

            return slabs

        else:
            length = len(root.findall('Instance'))
            content = {}
            hyperlink = {}
            s1 = []
            s2 = []
            totalLinks = 0
            slabs = {}
            if slab < length:
                revlength = int(length/slab)
            else:
                revlength = 1
            count = 0
            slabNo = 1
            for child in root:
                if 'Instance' in child.tag:
                    if 'RevisionId' in child.attrib:
                        revisionId = child.attrib['RevisionId']
                    else:
                        # This means its a comment
                        continue

                    for each in child:
                        if 'Body' in each.tag:
                            for i in each:
                                if 'Text' in i.tag:
                                    s = re.findall(r'(http?://\S+)', i.text)

                                    if len(s) != 0: #If Hyperlink is found
                                        if revisionId in hyperlink:
                                            if len(hyperlink[revisionId]) < len(s):
                                                result['Hyperlink Added'] += 1
                                            elif len(hyperlink[revisionId]) > len(s):
                                                result['Hyperlink Deleted'] += 1
                                            elif len(hyperlink[revisionId]) == len(s) and hyperlink[revisionId] != s:
                                                result['Hyperlink Fixed'] += 1
                                        else:
                                            result['Hyperlink Added'] += 1                                        
                                        hyperlink[revisionId] = s

                                    if revisionId in content:
                                        #check if content is added or not
                                        if len(content[revisionId]) < len(i.text):
                                            result['Content Added'] += 1
                                        elif len(content[revisionId]) > len(i.text):
                                            result['Content Deleted'] += 1
                                        elif len(content[revisionId]) == len(i.text) and content[revisionId] != i.text:
                                            result['Content Reorganised'] += 1
                                         
                                    else:
                                        #content is added
                                        result['Content Added'] += 1

                                    content[revisionId] = i.text

                    if count%revlength == 0:
                        slabs['Slab'+str(slabNo)] = copy.deepcopy(result)
                        slabNo += 1

                count += 1

            return slabs


    @staticmethod
    def revisionTypes(*args, **kwargs):
        slab = 20
        if kwargs.get('file_path') != None:
            file_name = kwargs['file_path']
            return knolAnalysis.revisionEdits(file_name, slab)

        elif kwargs.get('file_name') != None:
            file_name = kwargs['file_name']
            for f in file_name:
                if(kwargs.get('RevisionEdits')!=None):
                    kwargs['RevisionEdits'][f] = knolAnalysis.revisionEdits(f, slab)


    @staticmethod
    def getRevisionTypes(*args, **kwargs):
        if(kwargs.get('file_list')!=None):
            file_list = kwargs['file_list']

        elif(kwargs.get('dir_path')!=None):
            dir_path = kwargs['dir_path']

            file_list = glob.glob(dir_path+'/*.knolml')

        if kwargs.get('revision_id') != None:
            revisionId = kwargs['revision_id']
        else:
            revisionId = None

        fileNum = len(file_list)

        if(kwargs.get('c_num')!=None):
            cnum = kwargs['c_num']
        elif(fileNum<24):
            cnum = fileNum+1           # Bydefault it is 24
        else:
            cnum = 24


        fileList = []
        if(fileNum<cnum):
            for f in file_list:
                fileList.append([f])

        else:
            f = np.array_split(file_list,cnum)
            for i in f:
                fileList.append(i.tolist())


        manager = Manager()
        RevisionEdits = manager.dict()

        l = Lock()
        processDict = {}
        if(fileNum<cnum):
            pNum = fileNum
        else:
            pNum = cnum
        for i in range(pNum):
            processDict[i+1] = Process(target=knolAnalysis.revisionTypes, kwargs={'file_name':fileList[i],'RevisionEdits': RevisionEdits,'l': l})

        for i in range(pNum):
            processDict[i+1].start()

        for i in range(pNum):
            processDict[i+1].join()

        return RevisionEdits
    
    
    @staticmethod
    def findTags(list_tags, *args, **kwargs):
        if(kwargs.get('file_path')!=None):
            file_name = kwargs['file_path']            
            tree = ET.parse(file_name)            
            root = tree.getroot()
    
           
    
            uList = []
            for child in root:
                if('KnowledgeData' in child.tag):
                    for ch in child:
                        if('Instance' in ch.tag):
                            for newch in ch:
                                if('Contributors' in newch.tag):
                                    for chi in newch:
                                        if('OwnerUserId' in chi.tag):
                                            if(chi.text not in uList):
                                                uList.append(chi.text)
            return uList
            
        elif(kwargs.get('file_name')!=None):
            file_name = kwargs['file_name']
            for f in file_name:
                tree = ET.parse(f)            
                root = tree.getroot()
                postList = []
                
                for child in root:
                    if('KnowledgeData' in child.tag):
                        for ch in child:
                            if('Instance' in ch.tag):
                                for newch in ch:
                                    if('Body' in newch.tag):
                                        for txt in newch:
                                            if('Text' in txt.tag):                                            
                                                postList.append(txt.text)                            
                                    
                                    if('Tags' in newch.tag):
                                        
                                        if(list_tags in newch.text):
                                                continue
                                        else:
                                            postList = []
                                            print(f)
                                            
                                            
    
    
                if(kwargs.get('tagPosts')!=None):
                    kwargs['tagPosts'][f] = postList
                    #print(kwargs['revisionLength'])
        else:
            print("No arguments provided")    
    
    def findAllTags(list_tags, *args, **kwargs):
        #t1 = time.time()
        if(kwargs.get('file_list')!=None):
            file_list = kwargs['file_list']
            
        elif(kwargs.get('dir_path')!=None):
            dir_path = kwargs['dir_path']
            
            file_list = glob.glob(dir_path+'/*.knolml')
            
        fileNum = len(file_list)
        
        if(kwargs.get('c_num')!=None):
            cnum = kwargs['c_num']
        elif(fileNum<24):
            cnum = fileNum+1           # Bydefault it is 24
        else:
            cnum = 24
        
        
        fileList = []
        if(fileNum<cnum):
            for f in file_list:
                fileList.append([f])
            
        else:           
    
            f = np.array_split(file_list,cnum)
            for i in f:
                fileList.append(i.tolist())        
        
        
    
        
        manager = Manager()
        tagPosts = manager.dict()
    
        l = Lock()
        processDict = {}
        if(fileNum<cnum):
            pNum = fileNum
        else:
            pNum = cnum
        for i in range(pNum):
            processDict[i+1] = Process(target=knolAnalysis.findTags, args=(list_tags), kwargs={'file_name':fileList[i],'tagPosts':tagPosts,'l': l})
            #processDict[i+1] = Process(target=self.countWords, kwargs={'file_name':fileList[i], 'lastRev':lastRev,'l': l})
        for i in range(pNum):
            processDict[i+1].start()
        
        for i in range(pNum):
            processDict[i+1].join()  
        
        '''
        t2 = time.time()
        print(t2-t1)
        '''
        return tagPosts     
