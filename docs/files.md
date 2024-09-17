[<< Index](index)

## `files set`
Set the store files for the assistant.
```bash
navi files set [OPTIONS]
```

### Options
- `--global`, `--use_global` Use the global configuration.
- `--dir <str>`, `-d <str>` Add a path to included directories
- `--file-ext <str>`, `-e <str>` Add a file extension for included files 

### Example
Add all of the files in `src/` and `test/` with a `.py` file extension:
```bash
navi files set --dir src --dir test --file-ext py
```

## `files sync`
Sync the store files with the assistant.
```bash
navi files sync [OPTIONS]
```

### Options
 - `--global`, `--use_global` Use the global configuration.

## `info`
Display information about the assistant.

```bash
navi info [OPTIONS]
```

### Options
 - `--global`, `--use_global` Use the global configuration.

### Example