




import pandas as pd
import csv

from bs4 import BeautifulSoup
from bs4.element import Comment



#  KeepAlphaNumbericWords2
#  KeepAlphaNumbericWords
#  SaveNestedList2CSV
#  GetXpathOfSoupElement
#  TagVisible
#  VisibleTextFromHTML2
#  CreateTextListAndDfFromSoup
#  AddHomeToPath


#%%###########################################################################################################
def KeepAlphaNumbericWords2(string):
    "Only keep alpha Nummber and spaces but remove multiple spaces"
    first =  ''.join( l if l in " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789./+=?!'@#*" else " " for l in string).strip()
    return  ' '.join([ l for l in first.split(" ") if l !=""])

def KeepAlphaNumbericWords(string):
    "Only keep alpha Nummber and spaces but remove multiple spaces"
    first =  ''.join( l if l.isalnum() else " " for l in string).strip()
    return  ' '.join([ l for l in first.split(" ") if l !=""])

def ExtractNumbersFromString(string):
    string1="".join([s  if s.isdigit() else " " for s in string ])
    return [int(n) for n in string1.split(" ") if n != ""]  

#%%###########################################################################################################

def SaveNestedList2CSV(nlist,filename):
    with open(filename, 'w', newline='') as csvfile:
        csvsaver = csv.writer(csvfile, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvsaver.writerow('SiteNo Site TextNo Text Xpath'.split())
        for l in nlist:
            csvsaver.writerow(l)

def MakeDirIfNotExist(foldpath):
    import os
    if not os.path.isdir(foldpath) :
        if os.path.isfile(foldpath):
           print(f"Warning a File Exists at :'{foldpath}'") 
        else:
           os.mkdir(foldpath)

def ReadTextFile(fp,print_=True,sep="\n"):
   "ReadTextFile(fp,print_=True)" 
   prefix = "" if "." in fp else ".txt"
   if print_:
      print(f"Reading in File: '{fp+prefix}'") 
   with open(fp, 'r', encoding="utf-8") as file:
        return file.read().split(sep) 

def SaveTextFile(fp,data,print_=True,sep="\n"):
    "SaveTextFile(fp,data,print_)"
    prefix = "" if "." in fp else ".txt"   
    if print_:
       print(f"Saving File: '{fp+prefix}'")
    with open(fp+prefix, 'w', encoding="utf-8") as file:
         file.write(sep.join(data)) 
        
def SafeFilepath(filepath):
    for badchar in '<>"|?*':
        if badchar in filepath:
            filepath = filepath.replace(badchar,"")
    return filepath  


def SaveRead_Dict_with_text_df(*args,fp="allhtmlvisibletext",sep="**^**",both=False,to_dic=False):
    #from Scrape_Library import ReadTextFile,SaveTextFile,cumsum
    fp_txt, fp_csv = fp+".txt",  fp+".csv"

    if   len(args)==0:#Read
        
        dfin = pd.read_csv(fp_csv, index_col=0)
        dfin = [n[1] for n in dfin.groupby("Home_")] 
        cutlocs = cumsum([len(n) for n in dfin])
        
        textin = ReadTextFile(fp_txt, sep=sep)
        textin = [textin[s:f] for s,f in zip([0]+cutlocs,cutlocs)]
        if to_dic:
            text_dic_____ = { list(v2["Home_"])[0] :[v1,v2]  for v1,v2 in zip(textin, dfin)}
            return text_dic_____ 
        return textin,dfin
    
    elif len(args)==1: #Save_dic
        text_dic___ = args[0]        
        textout, dfout = [],[]        
        for k,v in text_dic___.items():
            text_,df_ = v
            df_["Home_"] = k
            textout.append(text_)
            dfout.append(df_)
            
    dfout = pd.concat(dfout)
    textout = [tt for t in textout for tt in t]    
    SaveTextFile(fp_txt,textout, sep=sep)
    dfout.to_csv(fp_csv)
    if both:
        return SaveRead_Dict_with_text_df(both=both,to_dic=to_dic)





#%%###########################################################################################################
def GetXpathOfSoupElement(element):
    # type: (typing.Union[bs4.element.Tag, bs4.element.NavigableString]) -> str
    """
    Generate xpath from BeautifulSoup4 element.
    :param element: BeautifulSoup4 element.
    :type element: bs4.element.Tag or bs4.element.NavigableString
    :return: xpath as string
    :rtype: str
    Usage
    -----
    >>> import bs4
    >>> html = (
    ...     '<html><head><title>title</title></head>'
    ...     '<body><p>p <i>1</i></p><p>p <i>2</i></p></body></html>'
    ...     )
    >>> soup = bs4.BeautifulSoup(html, 'html.parser')
    >>> xpath_soup(soup.html.body.p.i)
    '/html/body/p[1]/i'
    >>> import bs4
    >>> xml = '<doc><elm/><elm/></doc>'
    >>> soup = bs4.BeautifulSoup(xml, 'lxml-xml')
    >>> xpath_soup(soup.doc.elm.next_sibling)
    '/doc/elm[2]'
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:  # type: bs4.element.Tag
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name if 1 == len(siblings) else '%s[%d]' % (
                child.name,
                next(i for i, s in enumerate(siblings, 1) if s is child)
                )
            )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)

def GetElementFromSoupUsingXpath(soup, xpath):
    """    Gets you the element when given an xpath soup    """
    pars  = xpath.split("/")[1:]   
    pars2 = [f.replace("]","").split("[") for f in pars]
    pars2 = [[f[0],1] if len(f)==1 else [f[0],int(f[1])] for f in pars2]
    top = soup.findAll(pars2[0][0])[0]
    celem = top # current element
    parrent_parts = pars2[1:]
    
    for i,p in enumerate(parrent_parts):
        count=1
        for sib in celem.children:       
            if sib.name==p[0]:
                if count==p[1]:
                   celem =sib
                   break
                count+=1
        else:
           return None
    #print(GetXpathOfSoupElement(celem),xpath)            
    return celem


def TagVisible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def VisibleTextFromHTML2(body,elements=False):
    if type(body) is str:
        soup = BeautifulSoup(body, 'html.parser')
    else:
        soup = body
    texts = soup.findAll(text=True)
    visible_texts = list(filter(TagVisible, texts))
    if elements:
        return visible_texts
    return u" ".join(t.strip() for t in visible_texts)



def CreateTextListAndDfFromSoup(soup,only_xpaths=False,return_text=False):
    #vtext0           = VisibleTextFromHTML2(html,True)
    vtext0           = VisibleTextFromHTML2(soup,True)  
    #locations        = [i for i,t in enumerate(vtext0) if len(t.strip())>0]
    vtexts           = [i for i in vtext0 if len(i.strip())>0]
    texts            = [str(i) for i in vtexts]
    
    xpaths           = [GetXpathOfSoupElement(i) for i in vtexts]
    #vtexts           = [vtext0[i] for i in locations]
    #textsparents     = [i.parent for i in vtexts] 
    if only_xpaths:
        if return_text:
            return texts, xpaths
        return vtexts, xpaths
   
    columns = ["length","link","font","fontsize","italic","bold","xpath","link_parents","org_loc","header","group"]
    
    texts_df         = pd.DataFrame(index=range(len(vtexts)),columns=columns).fillna("")
    
    texts_df["length"        ] = [len(i) for i in vtexts] 
    texts_df["link"          ] = [text.parent.get("href","")  for text in vtexts]
    texts_df["class_parrent" ] = [" ".join(text.parent.get("class",[]))  for text in vtexts]
    texts_df["class_parrent2"] = [" ".join(text.parent.parent.get("class",[]))  for text in vtexts]
    
    texts_df["class_parrents"] = ["*".join([  " ".join(par.get("class",[])) for par in text.parents] )  for text in vtexts]

    texts_df["link_parents"  ] = [" ".join([n for n in [n.get("href","") for n in vtext0_.parents] if not n ==""]) for vtext0_ in vtexts]
    texts_df["org_loc"       ] = list(range(len(vtexts)))#locations   
    texts_df["xpath"         ] = xpaths
    if return_text:
       return  texts, texts_df        
    return vtexts,texts_df



#%%###########################################################################################################
   
    


def GetStyleInfoForBeautifulSoupElement(browser,bs_elem=False,xpath=False,return_xpath=False):
    if xpath==False:
       xpath    = GetXpathOfSoupElement(bs_elem)
    elements = browser.find_element_by_xpath(xpath)   
    #out = {k:element.value_of_css_property(k) for k in "font-size font-style font-weight height".split(" ")}
    style_dict = {k:elements.value_of_css_property(k) for k in "font-size font-style font-weight height font-family".split(" ")}    
    if return_xpath:
        return style_dict,xpath
    return style_dict

def FindStyleInformationAndAddToDataFrame(browser,dataframe=None,locationinfo=False):
    """Based ib the xpath column it adds four new ones with style information about this element   """
    
    columns_dict = {"italic"  :"font-style",
                    "fontsize":"font-size",
                    "bold"    :"font-weight",
                    "font"    :"font-family"}
    columns2 = [[],["locx","locy","sizx","sizy"]][locationinfo]
                
    if not dataframe is None:
        for extra_col in list(columns_dict)+columns2:
            if extra_col not in dataframe.columns:
               dataframe[extra_col] = None
        
        for i in dataframe.index:
            if i%20==(20-1):
               print(f"Finding CCS info for element:{str(i+1).rjust(5)} / {len(dataframe.index)}")
            xpath =  dataframe.loc[i,"xpath"]
            style_dict = GetStyleInfoForBeautifulSoupElement(browser,xpath=xpath) 
            for kcol,vsty in columns_dict.items():
                dataframe.loc[i, kcol ] = style_dict[ vsty ]
            if locationinfo:
                ele = browser.find_element_by_xpath(xpath) 
                dataframe.loc[i, columns2 ] = list(ele.location.values())+list(ele.size.values())
        return dataframe




def FindLocationOfElementSelenium(browser):
    """ This needs some work
    """
    browser.maximize_window() # now screen top-left corner == browser top-left corner 
    browser.get("http://stackoverflow.com/questions")
    question = browser.find_element_by_link_text("Questions")
    y_relative_coord = question.location['y']
    browser_navigation_panel_height = browser.execute_script('return window.outerHeight - window.innerHeight;')
    y_absolute_coord = y_relative_coord + browser_navigation_panel_height
    x_absolute_coord = question.location['x']
    return x_absolute_coord,y_absolute_coord



#%%###########################################################################################################

def AddHomeToPath(home,child):
    if not child.startswith("/"):
        return child
    #print(home.split("/")[:3]+[child])
    return "/".join( home.split("/")[:3])+child

def CumSum(lis,c=0):
    p=[]
    for ele in lis:
        c+=ele
        p.append(c)
    return p  

def FindXpathOfSegmentsFromXpathOfTitles(xpaths):
    """Find the xpath of the segment which contains the title """
    def KeepStart(a,b):
         loc = [i for i,(aa,bb) in enumerate(zip(a,b)) if aa!=bb][0]
         return "/".join(b[:loc+1])    
    vv   = [n.split("/") for n in xpaths]
    vvv  = [[ KeepStart(a,b) for a in vv if a!=b ] for b in vv]
    vvvv = [max(b, key=lambda s: len(s)) for b in vvv]
    return vvvv














