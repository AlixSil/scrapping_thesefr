import pandas as pd
import sys
from bs4 import BeautifulSoup
import requests
import urllib
import swifter


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
        return(None)
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
        return(None)
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
        return(None)
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
        return(None)
    if len(title_eng) > 1 :
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
    return dictionnary_of_results

def extract_thesis_info_from_df_row(row) :
    url = "https://www.theses.fr/{}".format(row["Identifiant de la these"])
    print(row)
    return(dataFromThesisPage(url))

if __name__ == "__main__" :
    all_basic_info = pd.read_csv(sys.argv[1], sep=";")
    all_basic_info = all_basic_info.reset_index(drop = True)
    extra_results = all_basic_info.apply(extract_thesis_info_from_df_row, result_type="expand", axis = 1)
    extra_results.to_csv(sys.argv[2], sep=";", index=False)
