import requests
from bs4 import BeautifulSoup


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


def dataFromThesisPage(url : str) -> None:
    """This function aims to taking a url for the site theses.fr, extract
    interesting data from it"""

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    resume = soup.find_all("ul", class_ = "resume")
    french_resume  = findFrenchResume(soup)
    eng_resume = findEnglishResume(soup)
    french_title = findFrenchTitle(soup)
    english_title = findEnglishTitle(soup)



dataFromThesisPage("https://www.theses.fr/s311849")
