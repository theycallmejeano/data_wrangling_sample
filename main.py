"""Commands to run the data wrangling pipeline"""
from argparse import ArgumentParser
from loguru import logger
import pandas as pd

from data_wrangling.wrangle import WrangleData
from data_wrangling.validate import validate_data
from data_wrangling.utils import get_coords, format_url, LOCATION_NAMES

def args_parser():
    """
    Command line arguments for the data pipeline
    """
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    wrangle = subparsers.add_parser('wrangle')
    wrangle.add_argument('-s', '--save', type=str, choices=['remote', 'local'],
                        required=True,
                        help='Save file to local or remote storage.')
    wrangle.add_argument("-m", "--merge", dest="merge", action="store_true",
                        help="Merges output from multiple API searches into one file")

    return parser.parse_args()


def main():
    """
    Main function to execute the data pipeline based on command-line arguments.

    """
    args = args_parser()

    if args.command == 'wrangle':
        logger.info('Starting the data pipeline...')

        merged_df = pd.DataFrame()

        for loc in LOCATION_NAMES:
            logger.info(f'Pulling data for {loc.title()}')
            lat, long = get_coords(loc)
            url = format_url(lat, long)
            wrangle = WrangleData(url)

            logger.info('Loading, transforming and validating data...')
            data = wrangle.load_data()
            df_transformed = wrangle.transform_data(data, loc)

            merged_df = pd.concat([merged_df, df_transformed], ignore_index=True)

        if validate_data(merged_df):
            logger.info('Data validated, exporting to storage')

            if args.merge:
                wrangle.export_data(merged_df, 'data/merged_data.csv', args.save)
            else:
                for loc in LOCATION_NAMES:
                    loc_df = merged_df[merged_df['location'] == loc.lower()]
                    wrangle.export_data(loc_df, f'data/{loc.lower()}.csv', args.save)
        else:
            raise ValueError('Data validation failed')


if __name__ == "__main__":
    main()
