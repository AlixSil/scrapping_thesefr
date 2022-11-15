import pandas as pd
import sys
import datetime


def create_url(date):
    """From a date, create the url pointing to a csv of all thesis defended at that date"""
    url = "https://www.theses.fr/?q=&zone1=titreRAs&val1=&op1=AND&zone2=auteurs&val2=&op2=AND&zone3=etabSoutenances&val3=&op3=AND&zone4=dateSoutenance&val4a={d}%2F{m}%2F{y}&val4b={d}%2F{m}%2F{y}&lng=fr/&type=avancee&checkedfacets=&format=csv"
    url = url.format(
        d=date.strftime("%d"),
        m=date.strftime("%m"),
        y=date.strftime("%Y"),
    )
    return url


def getDefendedThesisList(start_date, end_date):
    """Download all the general informations of all the theses defended between
    start_date and end_date (end_date excluded)"""
    current_date = start_date
    list_of_all_data_frames = []

    while current_date < end_date:
        a = None
        a = pd.read_csv(create_url(current_date), sep=";")
        current_date += datetime.timedelta(days=1)
        if a.shape[0] != 0:
            list_of_all_data_frames.append(a)
    return pd.concat(list_of_all_data_frames)


def getLimitDates():
    """Treat the script entry arguments into proper datetime objects"""
    s_date = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d")
    e_date = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d")
    return (s_date, e_date)


if __name__ == "__main__":
    s_date, e_date = getLimitDates()
    results = getDefendedThesisList(s_date, e_date)
    outFilePath = sys.argv[3]
    results.to_csv(outFilePath, sep=";", index=False)
