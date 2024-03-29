# Lecho360 #

### Contents ###
1. [Main](https://github.com/jhalstead85/lecho360/blob/master/Readme.md#lecho360)
2. [Requirements](https://github.com/jhalstead85/lecho360/blob/master/Readme.md#requirements)
3. [Usage](https://github.com/jhalstead85/lecho360/blob/master/Readme.md#usage)
4. [Examples](https://github.com/jhalstead85/lecho360/blob/master/Readme.md#examples)
5. [Title Mapping Format](https://github.com/jhalstead85/lecho360/blob/master/Readme.md#title-mapping-format)
6. [FAQ](https://github.com/jhalstead85/lecho360/blob/master/Readme.md#faq)

Lecho360 is a command-line Python tool that allows you to download lecture
videos from UIUC's Echo360 lecture portal. All that's required is the particular
course's UUID. See the FAQ for tips on how to find it.

An optional file that maps dates to lecture titles may be used in order to get more meaningful filenames. When using that optional file, lectures will be named
like
```
[COURSE] - [LECTURE DATE] - [LECTURE TITLE].m4v
```

Without that optional file, files will be named like

```
[COURSE] - [LECTURE DATE] - Lecture [NUMBER].m4v
```

Please excuse any hackiness in the implementation. :) It was originally intended to be a one-off, one-file solution.

# Requirements #

### Python ###
- Dateutil >= 2.2
- Selenium >= 2.44.0

```
pip install -r requirements.txt
```

### NodeJS ###
- PhantomJS >= 1.9.7

```
npm -g install phantomjs
```

If it fails to install via `npm`, then visit [http://phantomjs.org/download.htm](http://phantomjs.org/download.htm) for further instructions. Alternatively, if you're using `Ubuntu 14.04`, then [these instructions](http://sonnguyen.ws/install-nodejs-phantomjs-casperjs-ubuntu-14-04) worked for me. 

### Operating System ###
- Linux
- OS X

I don't have a Windows machine to test this on, but it should work.

# Usage #
```
>>> python lecho360.py

usage: lecho360.py [-h] --uuid COURSE_UUID [--titles TITLES_PATH]
[--output OUTPUT_PATH] [--after-date AFTER_DATE(YYYY-MM-DD)]
[--before-date BEFORE_DATE(YYYY-MM-DD)]

Download lectures from UIUC's Echo360 portal.

optional arguments:
  -h, --help                              Show this help message and exit

  --uuid COURSE_UUID,                     Echo360 UUID for the course, which is
  -u COURSE_UUID                          found in the URL of the course's video
                                          lecture page.

  --titles TITLES_PATH,                   Path to JSON file containing date to
  -f TITLES_PATH                          title mappings. See Readme.md for info
                                          on the required format.

  --output OUTPUT_PATH,                   Path to the desired output directory.
  -o OUTPUT_PATH                          The output directory must exist. Otherwise
                                          the current directory is used.

  --after-date AFTER_DATE(YYYY-MM-DD),    Only download lectures newer than
  -a AFTER_DATE(YYYY-MM-DD)               AFTER_DATE (inclusive). Note: This may
                                          be combined with --before-date.

  --before-date BEFORE_DATE(YYYY-MM-DD),  Only download lectures older than
  -b BEFORE_DATE(YYYY-MM-DD)              BEFORE_DATE (inclusive). Note: This may
                                          be combined with --after-date.
```
# Examples #

### Download all available lectures ###
```
>>> python lecho360.py                          \
  --uuid "a0143734-86e8-4d0a-aba1-a44715ec085c" \
  --ouput "~/Lectures"
```

### Download all lectures on or before a date ###
```
>>> python lecho360.py                          \
  --uuid "a0143734-86e8-4d0a-aba1-a44715ec085c" \
  --ouput "~/Lectures"                          \
  --before-date "2014-10-14"
```

### Download all lectures on or after a date ###
```
python lecho360.py                              \
  --uuid "a0143734-86e8-4d0a-aba1-a44715ec085c" \
  --ouput "~/Lectures"                          \
  --after-date "2014-10-14"
```

### Download all lectures in a given date range (inclusive) ###
```
>>> python lecho360.py                          \
  --uuid "a0143734-86e8-4d0a-aba1-a44715ec085c" \
  --ouput "~/Lectures"                          \
  --after-date "2014-08-26"                     \
  --before-date "2014-10-14"
```

### Download lectures with intelligent titles ###
```
>>> python lecho360.py                          \
  --uuid "a0143734-86e8-4d0a-aba1-a44715ec085c" \
  --ouput "~/Lectures"                          \
  --after-date "2014-08-26"                     \
  --before-date "2014-10-14"                    \
  --titles "14fa-cs473.json"
```

# Title Mapping Format #
In general, the file format is

```json
{
  "course": "CS 425 - Distributed Systems",
  "uuid": "11ae0191-49e2-4c34-95fd-fc65355262d4",
  "semester": "Fall 2014",
  "professors": ["Indranil (Indy) Gupta"],
  "titles": [
    {
      "date": "20140826",
      "title": "Introduction"
    },
    {
      "date": "20140828",
      "title": "Introduction to Cloud Computing"
    },
    {
      "date": "20140902",
      "title": "Mapreduce and Hadoop"
    }
  ]
}

```

Several real examples of these mapping files can be found in the top-level `lecho360` directory. Note that the provided date is parsed by `dateutil`. So as long as the date format is unambiguous, it should be able to parse it. However, if using an alternate date format fails, then try to use `YYYYMMDD` or `YYYY-MM-DD`. Either of those formats should work.


# FAQ #

### How do I retrieve the UUID for a course? ###
This is the most involved part (unless you have access to a titles file). What you need is the URL to the course's main Echo360 lecture page. It's the main page that lists all the recorded lectures and gives you the option to stream them or download them individually.

![CS 473' Main Echo360 Lecture Page](http://i.imgur.com/TfKRFhg.png)


You can usually find this link on your course's main webpage. If your course webpage only links directly to videos, then you should be able to navigate back to the main portal via that link.

The URL for the Fall 2013 semester of CS 473 looks like

```
http://recordings.engineering.illinois.edu/ess/portal/section/a0143734-86e8-4d0a-aba1-a44715ec085c
```

which you can verify is correct in the above screenshot. The UUID is the last element of the URL. So in the above example it's,

```
a0143734-86e8-4d0a-aba1-a44715ec085c
```

### Why do I need Selenium and/or PhantomJS? ###
The Echo360 portal sets an anonymous cookie when you visit the your course's main Echo360 lecture portal, which is needed when querying their separate REST API. I tried to use Python's `cookielib` to record this cookie before querying their API. However, the cookie is only set when the page loads the contents of a separate iframe. The quickest way I could find to programmatically load that iframe was to use PhantomJS via Selenium (even though PhantomJS dropped support for Python). I'm sure there's a better way to implement this, and exploring alternate solutions is on the `TODO` list.

### Why do I have to explicitly pass the UUID even when using a titles file? ###
You're right. It's on the `TODO` list.
