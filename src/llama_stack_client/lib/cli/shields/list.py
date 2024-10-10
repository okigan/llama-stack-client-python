# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

import json
import argparse

from llama_stack_client import LlamaStackClient
from llama_stack_client.lib.cli.configure import get_config
from llama_stack_client.lib.cli.subcommand import Subcommand
from llama_stack_client.lib.cli.common.utils import print_table_from_response


class ShieldsList(Subcommand):
    def __init__(self, subparsers: argparse._SubParsersAction):
        super().__init__()
        self.parser = subparsers.add_parser(
            "list",
            prog="llama-stack-client shields list",
            description="Show available llama models at distribution endpoint",
            formatter_class=argparse.RawTextHelpFormatter,
        )
        self._add_arguments()
        self.parser.set_defaults(func=self._run_shields_list_cmd)

    def _add_arguments(self):
        self.endpoint = get_config().get("endpoint")
        self.parser.add_argument(
            "--endpoint",
            type=str,
            help="Llama Stack distribution endpoint",
            default=self.endpoint,
        )

    def _run_shields_list_cmd(self, args: argparse.Namespace):
        if not args.endpoint:
            self.parser.error(
                "A valid endpoint is required. Please run llama-stack-client configure first or pass in a valid endpoint with --endpoint. "
            )
        client = LlamaStackClient(
            base_url=args.endpoint,
        )

        shields_list_response = client.shields.list()

        if shields_list_response:
            print_table_from_response(shields_list_response)
