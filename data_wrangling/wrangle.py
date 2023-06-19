"""Data wrangling functions"""
import pandas as pd
from loguru import logger
from data_wrangling.utils import get_api_response


class WrangleData:
    """
    Class with data processing functions for this pipeline
    """
    def __init__(self, url:str):
        self.url = url

    # function to load data
    def load_data(self) -> pd.DataFrame:
        """
        Load data from the API and transform to a dataframe

        Returns
            data - dataframe of data from the API
        """
        # get API response
        logger.info("Pulling data from the API")
        api_response = get_api_response(self.url)

        if not api_response:
            return api_response

       # format the data
        api_data = api_response.json()

        # convert to dataframe
        data = pd.DataFrame.from_dict(api_data["daily"])

        logger.info(f"{len(data)} records pulled from the API")
        return data

    # function to transform data
    def transform_data(self, data: pd.DataFrame, location:str) -> pd.DataFrame:
        """
        Transform data and return pivoted dataframe

        Args
            df - pandas dataframe for wrangling

        Returns
            df_pivot, pivoted dataframe
        """
        # rename columns
        data.rename(
            columns={
                "time": "date",
                "temperature_2m_max": "max_temp",
                "temperature_2m_min": "min_temp",
            }, inplace=True
        )

        # add location identifier
        data.loc[:, 'location'] = location.lower()

        # reshape data
        df_pivot = pd.melt(
            data,
            id_vars=["date", "location"],
            value_vars=["max_temp", "min_temp"],
            var_name='indicator',
        ).sort_values(["date", "indicator"], ignore_index=True)

        # store as dates
        df_pivot['date'] = pd.to_datetime(df_pivot['date'])

        return df_pivot

    # function to export data
    def export_data(self, data:pd.DataFrame, path:str, storage:str) -> None:
        """
        Export data to the required location

        Args
            path - file path
            df - dataframe for export
            storage- storage type
        """
        if storage == 'remote':
            # if you have some remote storage, such as S3, add the command here
            logger.info(f'Data saved to local storage at {path}')


        if storage == 'local':
            data.to_csv(path, index=False)
            logger.info(f'Data saved to local storage at {path}')
         