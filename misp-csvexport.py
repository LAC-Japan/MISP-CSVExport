#!/usr/bin/env python3
__version__ = "V2023.07.06"

# Standard modules
import warnings
import csv
import argparse
import configparser
import traceback
import datetime
from datetime import datetime as dt
from pathlib import Path as pt
from typing import Optional

# Pip additional modules
from pymisp import ExpandedPyMISP, MISPAttribute

# Const;
CONFIG_FILE_PATH = pt(__file__).parent.joinpath('config.ini')
CSV_HEADER = [
    'event_id',
    'event_title',
    'event_timestamp',
    'event_date',
    'event_tags',
    'category',
    'type',
    'value',
    'attribute_tags',
]

# date format pattern
DATE_FORMAT = {
    8: '%Y%m%d',
    10: '%Y%m%d%H',
    12: '%Y%m%d%H%M',
    14: '%Y%m%d%H%M%S',
}


def main() -> None:
    # Config parse
    conf = read_config()

    # Arguments parse
    parser = argparse.ArgumentParser(
        description='Search MISP for specific parameters.')
    parser.add_argument('--version', action='store_true',
                        default=False, help='Print version')
    parser.add_argument('--from', dest='from_timestamp', type=str,
                        help='From timestamp(UTC) to search for')
    parser.add_argument('--to', dest='to_timestamp',
                        type=str, help='To timestamp(UTC) to search for')
    parser.add_argument('-c', '--category', type=str,
                        help='Category to search for')
    parser.add_argument('-t', '--type', dest='type_attribute',
                        type=str, help='Type to search for')
    parser.add_argument('-v', '--value', type=str, help='Value to search for')
    parser.add_argument('-T', '--event-tags', type=str,
                        nargs='+', help='Tag(s) to search for(or condition)')
    parser.add_argument('--all', action='store_true',
                        default=False, help='Export all data')
    parser.add_argument('-o', '--out', dest='output_file', type=str,
                        default='result.csv', help='Output file name')
    parser.add_argument('--full-dump-event', action='store_true',
                        default=False, help='Dump full event data')
    args = parser.parse_args()

    # Check arguments
    if args.version:
        print(__version__)
        exit()

    arguments_specified = is_arguments_specified(args)
    if not args.all and not arguments_specified:
        print('No search criteria specified.')
        print('To output data for the entire period, specify --all option.')
        exit(1)
    elif args.all and arguments_specified:
        print('An attribute condition is specified in the argument.')
        print('The argument --all is ignored in this case.')
        exit(1)

    if "ISO8601" in conf["MISP"]:
        iso8601 = conf.getboolean('MISP', 'ISO8601')
    else:
        iso8601 = False

    # Parse timestamp
    ft = parse_datetime(args.from_timestamp, iso8601)
    tt = parse_datetime(args.to_timestamp, iso8601)
    timestamp = (
        None
        if ft is None and tt is None
        else (ft, tt)
    )

    # Hide warnings
    warnings.filterwarnings('ignore')

    # Connect to MISP
    try:
        misp = ExpandedPyMISP(
            conf['MISP']['URL'],
            conf['MISP']['AUTHKEY'],
            ssl=False,
            cert=(conf['MISP'].get('CERT_FILE_PATH'),
                  conf['MISP'].get('KEY_FILE_PATH')),
        )
    except Exception:
        print('MISP connect failed.')
        print(traceback.format_exc())
        exit(1)

    # Data search
    events = misp.search(
        controller='events',
        timestamp=timestamp,
        category=args.category,
        type_attribute=args.type_attribute,
        value=args.value,
        event_tags=args.event_tags,
        pythonify=True
    )

    # Data processing
    cnt = 0
    with open(args.output_file, 'w', encoding='utf-8-sig', newline='') as f:
        # Output header
        writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
        writer.writeheader()

        for e in events:
            for a in e.attributes:
                # Exclude Attributes Not Matching Conditions
                if (not args.full_dump_event and not match_data(args, a, ft, tt)):
                    continue

                # Output record
                writer.writerow({
                    'event_id': e.id,
                    'event_title': e.info,
                    'event_timestamp': e.timestamp,
                    'event_date': e.date,
                    'event_tags': ','.join([t.name for t in e.tags]),
                    'category': a.category,
                    'type': a.type,
                    'value': a.value,
                    'attribute_tags': ','.join([t.name for t in a.tags])
                })

                cnt += 1

    # Output result
    print(f'Output {cnt} data: {args.output_file}')


def read_config() -> dict:
    """ Read config file """

    if not CONFIG_FILE_PATH.is_file():
        print(f'Not found config file: {CONFIG_FILE_PATH}')
        exit(1)

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    return config


def match_data(args: argparse, target_attribute: MISPAttribute,
               ft: Optional[dt], tt: Optional[dt]) -> bool:
    """ Check the following items to see if they match the search conditions.
    : category
    : type
    : value
    : from_timestamp
    : to_timestamp
    """

    return (_match_data(args.category, target_attribute.category)
            and _match_data(args.type_attribute, target_attribute.type)
            and _match_data(args.value, target_attribute.value)
            and (ft is None
                 or ft.timestamp() <= target_attribute.timestamp.timestamp())
            and (tt is None
                 or tt.timestamp() >= target_attribute.timestamp.timestamp())
            )


def _match_data(check_value: Optional[str], target_value: str) -> bool:
    if check_value is None:
        return True
    return (check_value == target_value)


def parse_datetime(target_date: str, is_isoformat: bool) -> Optional[dt]:
    """ Parse str to datetime """

    if target_date is None:
        return None

    # Parse to datetime
    try:
        if is_isoformat:
            return datetime.datetime.fromisoformat(target_date)
        else:
            return dt.strptime(target_date, DATE_FORMAT[len(target_date)]).replace(tzinfo=datetime.timezone.utc)

    except Exception:
        print(f'Invalid date format: {target_date}')
        exit(1)


def is_arguments_specified(args: argparse) -> bool:
    """ Check the following items to see if an argument is specified.
    : category
    : type_attribute
    : value
    : event_tags
    : from_timestamp
    : to_timestamp
    """

    return (args.category is not None
            or args.type_attribute is not None
            or args.value is not None
            or args.event_tags is not None
            or args.from_timestamp is not None
            or args.to_timestamp is not None
            )


if __name__ == '__main__':
    main()
