# py-inotify-test

- [py-inotify-test](#py-inotify-test)
  - [Usage](#usage)
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
