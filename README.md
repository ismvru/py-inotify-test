# py-inotify-test

- [py-inotify-test](#py-inotify-test)
  - [Usage](#usage)
    - [Example output](#example-output)
  - [Configuration](#configuration)
  - [inotify events](#inotify-events)
    - [inotify basic events](#inotify-basic-events)
    - [inotify flags](#inotify-flags)

Watches for file changes using inotify

## Usage

```bash
pip install -r requirements.txt
python3 main.py
```

### Example output

```log
2022-08-19 15:33:50.838 | INFO     | __main__:<module>:105 - Start python inotify event handler
2022-08-19 15:33:50.838 | INFO     | __main__:<module>:106 - Loading configuration...
2022-08-19 15:33:50.839 | DEBUG    | __main__:<module>:114 - {'watch': ['/tmp'], 'events': ['IN_MODIFY', 'IN_CLOSE_WRITE', 'IN_CREATE', 'IN_DELETE', 'IN_DELETE_SELF']}
2022-08-19 15:33:50.839 | INFO     | __main__:inotify_watcher:67 - Init new inotify adapter
2022-08-19 15:33:50.839 | INFO     | __main__:inotify_watcher:72 - Adding inotify_tree_watcher to /tmp
2022-08-19 15:33:58.144 | DEBUG    | __main__:inotify_watcher:77 - Captured new event: ['IN_CREATE'] on /tmp/tmp.Gni02STFzX
2022-08-19 15:33:58.144 | DEBUG    | __main__:event_handler:85 - INotifyEvent(path='/tmp', filename='tmp.Gni02STFzX', events=['IN_CREATE'])
2022-08-19 15:33:58.144 | INFO     | __main__:event_handler:96 - File /tmp/tmp.Gni02STFzX was created
2022-08-19 15:33:58.145 | DEBUG    | __main__:inotify_watcher:77 - Captured new event: ['IN_OPEN'] on /tmp/tmp.Gni02STFzX
2022-08-19 15:33:58.145 | DEBUG    | __main__:inotify_watcher:77 - Captured new event: ['IN_CLOSE_WRITE'] on /tmp/tmp.Gni02STFzX
2022-08-19 15:33:58.145 | DEBUG    | __main__:event_handler:85 - INotifyEvent(path='/tmp', filename='tmp.Gni02STFzX', events=['IN_CLOSE_WRITE'])
2022-08-19 15:33:58.145 | INFO     | __main__:event_handler:90 - File /tmp/tmp.Gni02STFzX was modified. New checksum: af1349b9f5f9a1a6a0404dea36dcc9499bcb25c9adc112b7cc9a93cae41f3262
2022-08-19 15:33:58.146 | DEBUG    | __main__:inotify_watcher:77 - Captured new event: ['IN_OPEN'] on /tmp/tmp.Gni02STFzX
2022-08-19 15:33:58.146 | DEBUG    | __main__:inotify_watcher:77 - Captured new event: ['IN_CLOSE_NOWRITE'] on /tmp/tmp.Gni02STFzX
^C2022-08-19 15:34:02.675 | INFO     | __main__:<module>:125 - KeyboardInterrupt
```

## Configuration

`watch` - list of directories that will be watched
`events` - list of events that will be watched.

```yaml
watch:
  - /tmp

events:
  - "IN_MODIFY"
  - "IN_CLOSE_WRITE"
  - "IN_CREATE"
  - "IN_DELETE"
  - "IN_DELETE_SELF"
```

## inotify events

### inotify basic events

- `IN_ACCESS` - File was accessed
- `IN_ATTRIB` - Metadata changed
- `IN_CLOSE_WRITE` - File opened for writing was closed
- `IN_CLOSE_NOWRITE` - File or directory not opened for writing was closed
- `IN_CREATE` - File/directory created in watched directory
- `IN_DELETE` - File/directory deleted from watched directory
- `IN_DELETE_SELF` - Watched file/directory was itself deleted. This event also occurs if an object is moved to another filesystem
- `IN_MODIFY` - File was modified
- `IN_MOVE_SELF` - Watched file/directory was itself moved
- `IN_MOVED_FROM` - Generated for the directory containing the old filename when a file is renamed.
- `IN_MOVED_TO` - Generated for the directory containing the new filename when a file is renamed.
- `IN_OPEN` - File or directory was opened.

### inotify flags

- `IN_IGNORED` - Watch was removed explicitly (inotify_rm_watch(2)) or automatically (file was deleted, or filesystem was unmounted)
- `IN_ISDIR` - Subject of this event is a directory
- `IN_Q_OVERFLOW` - Event queue overflowed (wd is -1 for this event)
- `IN_UNMOUNT` - Filesystem containing watched object was unmounted.  In addition, an IN_IGNORED event will subsequently be generated for the watch descriptor
