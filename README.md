# MISP CSVExport

MISP project: <http://www.misp-project.org/>

## Overview
This Python script retrieves data from MISP (Malware Information Sharing Platform) and exports the results to a CSV file. 
The search parameters can be specified as arguments when running the script.

- Search data from MISP based on specified parameters.
- Export the search results to a CSV file.
- Search parameters can be specified as arguments.

## License

This software is released under the BSD License, see LICENSE.txt.

## Operation confirmed environment

* Python 3.10
* PyMISP 2.4.172

## Installation
1. Clone the repository.
2. Install the required Python libraries using pip.
```
pip3 install pymisp
```
3. Create config.ini based on config.sample.
4. Set MISP URL, MISP AUTHKEY in config.ini. 
If client certificate authentication is set to MISP, also specify CERT FILE PATH and KEY FILE PATH.
5. Run the script with the desired arguments.

## Usage

```
python3 misp-csvexport.py --from <date string> --to <date string> -c category -t type -v value -T tag1 tag2
```
Arguments
- `--from YYYYMMDD(HHMMSS)` : Search for data after this timestamp(UTC).
- `--to YYYYMMDD(HHMMSS)` : Search for data up to this timestamp(UTC).
- `-c, --category category` : Search for data of this category.
- `-t, --type-attribute type` : Search for data of this type.
- `-v, --value value` : Search for data with this value.
- `-T, --event-tags tag1 tag2` : Search for data that has any of the specified tags in the event tag.
- `--all` : Export all data.
- `--out` : Specify the output file name. If not specified, the file name will be output as result.csv.
- `--full-dump-event` : Outputs all event data associated with the attribute hit by the search. If not specified, only attributes that match the conditions will be output.
