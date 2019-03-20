#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Uses pigshare https://pypi.org/project/pigshare/
# Requires ~/.pigshare.conf with a OAuth2 token.
#   Get "Personal Token" from https://figshare.com/account/applications
#   Put into ~/.pigshare.conf, which shoud look like:
#
#       [default]
#       token = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#
# TODO: Reserve DOI and return it.

from __future__ import print_function

import argparse
import sys

from pigshare.api import figshare_api
from pigshare.models import ArticleCreate
from pigshare.pigshare import PigshareConfig
import restkit


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
    project_group = parser.add_mutually_exclusive_group()
    project_group.add_argument("--rsoc",
                               dest="project", action="store_const", const="rsoc",
                               help="Set project to 'ResearchSOC'")
    project_group.add_argument("--trustedci",
                               dest="project", action="store_const", const="trustedci",
                               help="Set project to 'TrustedCI'")
    project_group.add_argument("--swip",
                               dest="project", action="store_const", const="swip",
                               help="Set project to 'SWIP'")
    parser.add_argument("--file", metavar="filename", type=str, help="Upload file")
    parser.add_argument("--keyword", metavar="keyword", type=str, help="Add keyword")
    parser.add_argument("title", metavar="title", type=str, help="Title")
    parser.add_argument("description", metavar="description", type=str, help="Description")
    return parser


def make_article(args):
    """Return ArticleCreate object."""
    article_fields = {
        "title" : args.title,
        "description" : args.description,
        "defined_type" : args.type,
        "funding" : "None",  # Required field
        "license" : 1,  # CC BY 4.0
        # 'tags' is an alias for 'keywords'
        "tags" : [ ],
        "custom_fields" : {},
        "categories" : [
            77 # Applied Computer Science
        ]
    }
    if args.project:
        if args.project == "trustedci":
            article_fields["funding"] = "NSF 1547272"
            article_fields["tags"].append("trustedci")
        elif args.project == "swip":
            article_fields["funding"] = "NSF 1642070, 1642053, and 1642090"
            article_fields["tags"].append("swip")
        elif args.project == "rsoc":
            article_fields["funding"] = "NSF 1840034"
            article_fields["tags"].append("researchsoc")
        else:
            print("Warning: Unrecognized project \"{}\"".format(args.project))
    if args.keyword:
        article_fields["tags"].extend(args.keyword)
    # A keyword is required for publishing
    if len(article_fields["tags"]) == 0:
        article_fields["tags"].append("iucacr")
    article = ArticleCreate()
    article.update(article_fields)
    return article


def main(argv=None):
    parser = make_parser()
    args = parser.parse_args(argv if argv else sys.argv[1:])

    config = PigshareConfig()
    api = figshare_api(token=config.figshare_token)
    article = make_article(args)
    try:
        location = api.call_create_article(article)
    except restkit.errors.Unauthorized as ex:
        # TODO: Get message from ex object
        print("Authorization to publish failed: " + str(ex))
        return(1)
    except restkit.errors.RequestFailed as ex:
        print("Error creating article: " + str(ex))
        return(1)
    id = location.location.rsplit('/', 1)[-1]
    if args.debug:
        print("Article {} created".format(id))
    if args.file:
        try:
            location = api.call_upload_new_file(id, args.file)
        except restkit.errors.RequestFailed as ex:
            print("Error uploading file: " + str(ex))
            return(1)
        if args.debug:
            print("{} uploaded".format(args.file))
    try:
        doi = api.call_reserve_doi(id)
    except restkit.errors.RequestFailed as ex:
        print("Error reserving DOI: " + str(ex))
        return(1)
    print(doi)
    return(0)

if __name__ == "__main__":
    sys.exit(main())
