## Data Wrangling Sample

## Description
This repo provides a simple data wrangling example that you can use as a learning resource.
It demonstrates the process of preparing and transforming data for further analysis or processing. 
This script pulls daily temperature statistics from [open-meteo API](https://open-meteo.com/en/docs) and stores them to a local directory. 

## Setting Up
After cloning the repository,
```bash
# change the working directory
cd data_wrangling_sample

# install the required packages
poetry shell
poetry install
```
Make a copy of `env.example` and name it `.env`. You can modify the date and location parameters for your testing case.
Additionally, in the root folder of this repo, add a `data/` folder, which will be used to store the data locally.

```bash
# in the data_wrangling_sample
mkdir data
```

## Running the script
To pull data for your location(s) and store this to the local directory, run

```bash
python main.py wrangle -s local
```
This will store the data in separate files for your separate locations. If you wish to merge the files

```bash
python main.py wrangle -s local
```
