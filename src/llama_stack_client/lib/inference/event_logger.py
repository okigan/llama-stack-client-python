# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.


from llama_stack_client.types import (
    ChatCompletionStreamChunk,
    InferenceChatCompletionResponse,
)
from termcolor import cprint


class LogEvent:
    def __init__(
        self,
        content: str = "",
        end: str = "\n",
        color="white",
    ):
        self.content = content
        self.color = color
        self.end = "\n" if end is None else end

    def print(self, flush=True):
        cprint(f"{self.content}", color=self.color, end=self.end, flush=flush)


class EventLogger:
    async def log(self, event_generator):
        for chunk in event_generator:
            if isinstance(chunk, ChatCompletionStreamChunk):
                event = chunk.event
                if event.event_type == "start":
                    yield LogEvent("Assistant> ", color="cyan", end="")
                elif event.event_type == "progress":
                    yield LogEvent(event.delta, color="yellow", end="")
                elif event.event_type == "complete":
                    yield LogEvent("")
            elif isinstance(chunk, InferenceChatCompletionResponse):
                yield LogEvent("Assistant> ", color="cyan", end="")
                yield LogEvent(chunk.completion_message.content, color="yellow")
            else:
                yield LogEvent("Assistant> ", color="cyan", end="")
                yield LogEvent(chunk, color="yellow")
