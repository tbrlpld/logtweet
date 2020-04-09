# LogTweet

Command line tool to create a tweet based on a #100DaysOfCode log message.


## Usage
The log from which the tweet will be generated has to have a format like my log.
You can find my log at [https://log100days.lpld.io/log.md](https://log100days.lpld.io/log.md).
My log is based on the [original #100DaysOfCode log repo](https://github.com/kallaway/100-days-of-code/blob/master/log.md).
But I am diverting from that format a little.
Specifically, I am using sub-headings (of the third level `### ...`) instead of strong text `**...**` to delimit the daily sub-sections ("Today's Progress", "Thoughts", "Links").
Check out [my raw log](https://raw.githubusercontent.com/tbrlpld/100-days-of-code/master/log.md) for details.

This is a markdown log, that is converted into an HTML page.
I have created a little [Quart/Flask app that converts my log to an HTML site](https://github.com/tbrlpld/log100days) using the `markdown2` package.
But other Markdown converters should work similar.

Once you have an HTML document with `h2` day headers and `h3` sections for "Today's Progress" and "Link(s)", you can point the tool at the URL of your HTML log page and generate a Tweet from it.

To actually enable the tweeting, you need to create a Twitter developer account and get an API key, API secret, Access Token and Access Token Secret.

The tweet will also contain the first link that you define in the "Link(s)" section under today's log.
To save some space, the link is shortened.
By default, I use [my own link shortener](https://s.lpld.io).

If you want to, you can also use the [Bit.ly service](https://bit.ly).
Their links might be a bit shorter and they provide you with some engagement and tracking info.
My link shortener does not do that.
To use the Bitly service, you need to generate an API key through them and add it to the config (see below).


### Options

If you want to create a tweet for a different day than today, you can do so with the `--offset` command line flag.
The offset is defined in integer days relative to today.
So to generate a tweet for yesterday use `-o -1`.

If you want to suppress the actual tweeting and only see the message in the console, use the `--testmode` command line flag.

## Installation
I recommend [`pipx`](https://pipxproject.github.io/pipx/) to install python scripts and other tools in isolated virtual environments. This keeps the your platform Python installation clean and you don't have to worry about activating a particular virtual environment to use a tool/script.

```shell
pipx install logtweet
```

This way you will have a clean environment and the tool still available on the command line.

But if you want to, you should be able to install it with `pip install logtweet`.

## Configuration

You need a configuration file for the script to work.
The `config.ini` can either be in the current working directory or in `~/.config/logtweet/`.

Because I can not figure out how to define a "post-install hook" that is run by `pip`, I can not generate an example config at the defined location.
This means you have to put the config there manually.
You can find an [example config on GitHub](./config.ini.example).

In that config file you define the URL where your log can be found and the API keys and access tokens that are needed for Twitter and Bit.ly.


## Development

Install with
```shell
python -m pip install -e ".[develop]"
```

This installs the app dependencies as well as tools to develop and distribute the package.

## Distribution

To distribute the package on PyPi, first create the latest build with:
```shell
python setup.py sdist bdist_wheel
```

This creates the new distribution files in the `/dist` directory.

Upload the created files (e.g. for version 0.1.4) with `twine`.
```shell
twine upload dist/logtweet-0.1.4*
```

