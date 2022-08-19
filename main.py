#!/usr/bin/env python3

import inotify.adapters
from dataclasses import dataclass
import uvloop
from loguru import logger
from blake3 import blake3
import yaml


@dataclass
class INotifyEvent:
    """Basic inotify event

    path - path to watched directory
    filename - filename of file
    events - list of inotify events"""

    path: str
    filename: str
    events: list


class Helpers:
    def __init__(self) -> None:
        """Some helpers, that may be used in Watchers.

        calc_checksum - calculates BLAKE3 checksum of file"""
        pass

    def calc_checksum(self, filename: str):
        """Calculates Blake3 Chesksum of file `filename`"""
        with open(filename, "rb") as f:
            hash = blake3(f.read()).hexdigest()
        return hash


class Watchers:
    default_watch_events = [
        "IN_MODIFY",
        "IN_CLOSE_WRITE",
        "IN_CREATE",
        "IN_DELETE",
        "IN_DELETE_SELF",
    ]

    def __init__(self, watch_dirs: list, watch_events: list = None) -> None:
        """Class contains inotify watcher function and event handlers

        watch_dirs - list of directories that will be watched
        watch_events - list of events that will be watched.
        If None - will watch default events

        Default events: `IN_MODIFY`, `IN_CLOSE_WRITE`, `IN_CREATE`,
        `IN_DELETE`, `IN_DELETE_SELF`"""
        self.watch_dirs = watch_dirs
        if watch_events is None:
            watch_events = self.default_watch_events
        self.watch_events = watch_events
        self.helpers = Helpers()

    def inotify_watcher(self):
        """Creates inotify watcher

        Watches for all directories in self.watch_dirs
        Calls event_handler for all events in self.watch_events"""
        logger.info("Init new inotify adapter")

        i = inotify.adapters.Inotify()

        for dir in self.watch_dirs:
            logger.info(f"Adding inotify_tree_watcher to {dir}")
            i.add_watch(dir)

        for event in i.event_gen(yield_nones=False):
            (_, event_list, path, filename) = event
            logger.debug(f"Captured new event: {event_list} on {path}/{filename}")
            if not any(item in self.watch_events for item in event_list):
                continue
            event = INotifyEvent(path=path, filename=filename, events=event_list)
            self.event_handler(event)

    def event_handler(self, event: INotifyEvent):
        """Basic inotify event handler"""
        logger.debug(event)

        # Calc checksum if file was modified
        if any(item in ["IN_MODIFY", "IN_CLOSE_WRITE"] for item in event.events):
            sum = self.helpers.calc_checksum(f"{event.path}/{event.filename}")
            logger.info(
                f"File {event.path}/{event.filename} was modified. New checksum: {sum}"
            )

        # Log if file was created
        if "IN_CREATE" in event.events:
            logger.info(f"File {event.path}/{event.filename} was created")

        # Log if file was deleted
        if any(item in ["IN_DELETE", "IN_DELETE_SELF"] for item in event.events):
            logger.info(f"File {event.path}/{event.filename} was deleted")


if __name__ == "__main__":

    try:
        logger.info("Start python inotify event handler")
        logger.info("Loading configuration...")

        # Read config file
        try:
            with open("config.yml", "r") as config_file:
                config: dict = yaml.safe_load(config_file)
        except FileNotFoundError as e:
            logger.exception(e)
            exit(1)
        logger.debug(config)

        # Init Watchers class with our configuration
        w = Watchers(watch_dirs=config["watch"], watch_events=config["events"])

        # Create event loop and run our function
        loop = uvloop.new_event_loop()
        loop.create_task(w.inotify_watcher())
        loop.run_forever()

    except KeyboardInterrupt:
        # If Ctrl+C Pressed - exit.
        logger.info("KeyboardInterrupt")
        exit(0)
