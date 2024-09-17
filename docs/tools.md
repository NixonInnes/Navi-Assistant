[<< Index](index)

## `tools pull`
Pull a set of assistant tools from a GitHub repository.

```bash
navi tools pull [OPTIONS] [Repository]
```

### Options
 - `--global`, `--use_global` Use the global configuration.

### Example
```bash
# Input
navi tools pull NixonInnes/Navi-Assistant-Tools-Linux

# Output
·.•°•.·.✧ ✦ 🧚 ✦ [ ✦ Tools:Pull ✦ ]
 | Pulling tools from NixonInnes/Navi-Assistant-Tools-Linux...
Cloning into '.navi/tools'...
remote: Enumerating objects: 23, done.
remote: Counting objects: 100% (23/23), done.
remote: Compressing objects: 100% (4/4), done.
remote: Total 23 (delta 19), reused 23 (delta 19), pack-reused 0 (from 0)
Receiving objects: 100% (23/23), done.
Resolving deltas: 100% (19/19), done.
```