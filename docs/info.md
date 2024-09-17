[<< Index](index.md)

## `info` 
Display information about the assistant.

```bash
navi info [OPTIONS] ...
```

### Options
 - `--global`, `--use_global` Use the global configuration.

### Example
```bash
# Input
$ navi info [OPTIONS] 

# Output
·.•°•.·.✧ ✦ 🧚 ✦ [ ✦ Info ✦ ]
 | Name: navi-test
 | Description: navi-test
 | Instructions: you are an assistant
 | Model: gpt-4o-mini
 | Assistant ID: ~snip~
 | Thread ID: ~snip~
 | Available Tools:
 |   - pci_devices
 |   - system_uptime
 |   - journalctl_logs
 |   - ip_address
 |   - disk_space
 |   - usb_devices
 |   - read_file
 |   - systemctl_status
 |   - webpage
 |   - compare_files
 |   - list_directory
 |   - cpus
 |   - running_processes
 |   - sensor_readings
 |   - write_file
 |   - directory_tree
 |   - logged_in_users
 |   - pattern_search
 |   - block_devices
 |   - current_datetime
 |   - kernel_info
```