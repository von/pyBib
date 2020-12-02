#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Requires ~/.figshare.conf with a Figshare Personal Token.
#   Get "Personal Token" from https://figshare.com/account/applications
#       https://help.figshare.com/article/how-to-get-a-personal-token
#   Put into ~/.figshare.conf, which shoud look like:
#
#       [default]
#       token = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


import argparse
import configparser
import os.path
import sys

from pybib import Figshare


def make_parser():
    """Return arparse>ArgumentParser instance"""
    parser = argparse.ArgumentParser(
        description=__doc__,  # printed with -h/--help
        # Don't mess with format of description
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # To have --help print defaults with trade-off it changes
        # formatting, use: ArgumentDefaultsHelpFormatter
    )
    # Only allow one of debug/quiet mode
    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument("-d", "--debug",
                                 action='store_true', default=False,
                                 help="Turn on debugging")
    verbosity_group.add_argument("-q", "--quiet",
                                 action="store_true", default=False,
                                 help="run quietly")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0")
    type_group = parser.add_mutually_exclusive_group()
    type_group.add_argument("--paper", default="paper",
                            dest="type", action="store_const", const="paper",
                            help="Set type to 'paper'")
    type_group.add_argument("--presentation",
                            dest="type", action="store_const", const="presentation",
                            help="Set type to 'presentation'")
    project_group = parser.add_argument_group()
    project_group.add_argument("--rsoc",
                               dest="project", action="append_const", const="rsoc",
                               help="Set project to 'ResearchSOC'")
    project_group.add_argument("--trustedci",
                               dest="project", action="append_const", const="trustedci",
                               help="Set project to 'TrustedCI'")
    project_group.add_argument("--swip",
                               dest="project", action="append_const", const="swip",
                               help="Set project to 'SWIP'")
    parser.add_argument("--file", metavar="filename", type=str, help="Upload file")
    parser.add_argument("--keyword", metavar="keyword", type=str, help="Add keyword")
    parser.add_argument("title", metavar="title", type=str, help="Title")
    parser.add_argument("description", metavar="description", type=str, help="Description")
    return parser


def make_article(args):
    """Return an article as a dictionary."""
    article_fields = {
        "title" : args.title,
        "description" : args.description,
        "defined_type" : args.type,
        "funding" : [ ],  # Will convert to string later
        "license" : 1,  # CC BY 4.0
        # 'tags' is an alias for 'keywords'
        "tags" : [ ],
        "custom_fields" : {},
        "categories" : [
            77 # Applied Computer Science
        ]
    }
    if args.project:
        for project in args.project:
            if project == "trustedci":
                article_fields["funding"].append("NSF 1920430")
                article_fields["tags"].append("trustedci")
            elif project == "swip":
                article_fields["funding"].extend(
                    ["NSF 1642070", "NSF 1642053", "NSF 1642090"])
                article_fields["tags"].append("swip")
            elif project == "rsoc":
                article_fields["funding"].append("NSF 1840034")
                article_fields["tags"].append("researchsoc")
            else:
                print("Warning: Unrecognized project \"{}\"".format(project))
    if len(article_fields["funding"]) > 0:
        article_fields["funding"] = ", ".join(article_fields["funding"])
    else:
        # Required field, so must have something
        article_fields["funding"] = "None"
    if args.keyword:
        article_fields["tags"].extend(args.keyword)
    # A keyword is required for publishing
    if len(article_fields["tags"]) == 0:
        article_fields["tags"].append("iucacr")
    return article_fields


def main(argv=None):
    parser = make_parser()
    args = parser.parse_args(argv if argv else sys.argv[1:])

    config = configparser.ConfigParser()
    config.read([os.path.expanduser('~/.figshare.conf')])
    api = Figshare(config.get("default", "token"))
    article = make_article(args)
    try:
        location = api.create_article(article)
    except Exception as ex:
        print("Error creating article: " + str(ex))
        if args.debug:
            raise(ex)
        return(1)
    id = location.rsplit('/', 1)[-1]
    if args.debug:
        print("Article {} created".format(id))
    if args.file:
        try:
            location = api.upload_new_file(id, args.file)
        except Exception as ex:
            print("Error uploading file: " + str(ex))
            if args.debug:
                raise(ex)
            return(1)
        if args.debug:
            print("{} uploaded".format(args.file))
    try:
        doi = api.reserve_doi(id)
    except Exception as ex:
        print("Error reserving DOI: " + str(ex))
        if args.debug:
            raise(ex)
        return(1)
    print(doi)
    return(0)

if __name__ == "__main__":
    sys.exit(main())
