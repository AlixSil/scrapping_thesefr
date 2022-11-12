import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime
import urllib

def findFrenchResume(s : BeautifulSoup) -> str:
    """take the BeautifulSoup of a page and extract the french resume"""
    resume_french = s.find_all(
        "span",
        {
            "property" : "dc:description",
            "xml:lang" : "fr"
        }
    )

    if len(resume_french) == 0 :
        raise Error("No french resume were found")
    elif len(resume_french) > 1 :
        raise Error("Several french resume were found")
    else :
        return (resume_french[0].text.strip())

def findEnglishResume(s : BeautifulSoup) -> str:
    """take the BeautifulSoup of a page and extract the french english"""
    resume_eng = s.find_all(
        "span",
        {
            "property" : "dc:description",
            "xml:lang" : "en"
        }
    )

    if len(resume_eng) == 0 :
        raise ValueError("No english resume were found")
    elif len(resume_eng) > 1 :
        raise ValueError("Several english resume were found")
    else :
        return (resume_eng[0].text.strip())

def findFrenchTitle(s : BeautifulSoup) -> str:
    """Find the french title of the thesis"""
    title_french = s.find_all("h1",
        {
            "property" : "dc:title",
            "xml:lang" : "fr"
        }
    )

    if len(title_french) == 0 :
        raise ValueError("No french title was found")
    elif len(title_french) > 1 :
        raise ValueError("Several french titles were found")
    else :
        return (title_french[0].text.strip())

def findEnglishTitle(s : BeautifulSoup) -> str:
    """Find the french title of the thesis"""
    title_eng = s.find_all("span",
        {
            "property" : "dcterms:alternative",
            "xml:lang" : "en"
        }
    )

    if len(title_eng) == 0 :
        raise ValueError("No english title was found")
    elif len(title_eng) > 1 :
        raise ValueError("Several english titles were found")
    else :
        return (title_eng[0].text.strip())

def findKeywordsEnglish(s : BeautifulSoup) -> str:
    keyWords = s.find_all(
        "span",
        {
            "property" : "dc:subject",
            "xml:lang" : "en"
        }
    )

    if len(keyWords) == 0 :
        return None
    else :
        return ";".join([k.text.strip() for k in keyWords])

def findKeywordsFrench(s : BeautifulSoup) -> str:
    keyWords = s.find_all(
        "span",
        {
            "property" : "dc:subject",
            "xml:lang" : "fr"
        }
    )

    if len(keyWords) == 0 :
        return None
    else :
        return ";".join([k.text.strip() for k in keyWords])

def dataFromThesisPage(url : str) -> None:
    """This function aims to taking a url for the site theses.fr, extract
    interesting data from it"""

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    dictionnary_of_results = {}
    dictionnary_of_results["french_summary"]  = findFrenchResume(soup)
    dictionnary_of_results["english_summary"] = findEnglishResume(soup)
    dictionnary_of_results["french_title"] = findFrenchTitle(soup)
    dictionnary_of_results["french_title"] = findEnglishTitle(soup)
    dictionnary_of_results["english_keywords"] = findKeywordsEnglish(soup)
    dictionnary_of_results["french_keywords"] = findKeywordsFrench(soup)

    print(pd.DataFrame(dictionnary_of_results, index = [0]))



def create_url(date) :
    """From a date, create the url pointing to a csv of all thesis defended at that date"""
    url = "https://www.theses.fr/?q=&zone1=titreRAs&val1=&op1=AND&zone2=auteurs&val2=&op2=AND&zone3=etabSoutenances&val3=&op3=AND&zone4=dateSoutenance&val4a={d}%2F{m}%2F{y}&val4b={d}%2F{m}%2F{y}&lng=fr/&type=avancee&checkedfacets=&format=csv"
    url = url.format(
        d = date.strftime("%d"),
        m = date.strftime("%m"),
        y = date.strftime("%Y"),
    )
    return(url)


def getDefendedThesisList(start_date, end_date):
    '''Download all the general informations of all the theses defended between
     start_date and end_date (end_date excluded)'''
    current_date = start_date
    list_of_all_data_frames = []

    while current_date < end_date :
        print(current_date)
        a = None
        a = pd.read_csv(create_url(current_date), sep=";")
        current_date += datetime.timedelta(days=1)
        if a.shape[0] !=0 :
            list_of_all_data_frames.append(a)

    return(pd.concat(list_of_all_data_frames))

def to_apply(row) :
    url = "https://www.theses.fr/{}".format(row["Identifiant de la these"])
    return(dataFromThesisPage)

if __name__ == "__main__" :
    s_date = datetime.date(2016, 1, 1)
    e_date = datetime.date(2016, 2, 1)


    all_basic_info = getDefendedThesisList(s_date, e_date)
    scrapped_info = all_basic_info.apply(result_type)

    dataFromThesisPage("https://www.theses.fr/s140161")
