# Scrapping theses.fr

## Context
theses.fr is the website referencing PhD thesis defended in France. This website allows access to the manuscript, but also to a summary (in english and/or french) and to several key words to classify the thesis.

## Aim
Create a scrapper that will extract from this site all informations on defended PhD, accessible online in the last 5 years.

 ## Progress
Current scrapper can download data for the choosen dates (that can be parametered in config.yaml)

The scrapper currently assume you have 6 CPUs available, this can be changed within the snakemake call and the Snakefile

```bash
snakemake -c6
```

## To Do
- Putting the data together, and clean it
- Add a conda support for reproducibility
