# RSS reader 

A command-line utility for reading news with RSS, written in Python 3.9. The utility written as a final task for EPAM Python Training 2021.09  

## Installation and run

1. With pip install:


    $ pip install grebarss

Now you can run the utility in two ways:

    $ grebarss <arguments>
    or
    $ rss_reader <arguments>

2. With Git:


    $ git clone https://github.com/Greba3000/Homework

    $ pip install -r requirements.txt

    $ cd .../Homework/AlexanderHreben/grebarss_reader

Now you can run the utility:

    $ python rss_reader.py <arguments>

## Usage

- Find and copy URL for RSS source
- rss_reader [URL]
- Help: rss_reader -h

usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] source

Pure Python command-line RSS reader.

positional arguments:
  source         URL RSS

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided

### --json

In case of using --json argument utility convert the news into JSON format. JSON structure:
- The data are in name/value pairs
- Data objects are separated by commas.
- Curly braces {} hold objects
- Square brackets [] hold arrays.
- Each data element is enclosed with quotes "" if it is a character, or without quotes if it is a numeric value.

Example of item containing news:
{...
    "item": [
        {
            "title": "title_data",
            "pubDate": "pubDate_data",
            "link": "link_data"
            "image": "image_data"
        }
    ]
...}

## Testing

For testing do following:

    $ cd .../Homework/AlexanderHreben/ 
For run all tests:

    $ pytest 
For run specify test:

    $ pytest <name of test>

Test coverage is 52%. To check this, do the following:

    $ pip install pytest pytest-cov

    $ cd .../Homework/AlexanderHreben

    $ pytest --cov=grebarss_reader

## License

Distributed under the MIT License. See LICENSE.txt for more information.

## Contact

Email - greba3000@gmail.com
Follow me on LinkedIn - https://www.linkedin.com/in/alexander-greben-87209319b/


