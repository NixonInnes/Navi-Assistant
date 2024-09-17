[<< Index](index.md)

## `config`
Modify the assistant configuration.

```bash
navi config [OPTIONS] [key] [value]
```

Valid keys:
 - `name`
 - `description`
 - `instructions`
 - `model`
 - `store_id`
 - `assistant_id`
 - `thread_id`

### Options
 - `--global`, `--use_global` Use the global configuration.

### Example
```bash
# Input
navi config --global model gpt-4o

# Output
·.•°•.·.✧ ✦ 🧚 ✦ [ ✦ Config ✦ ]
 > Global configuration
 | Set model to gpt-4o
```