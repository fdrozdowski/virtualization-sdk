---
title: Virtualization SDK
---

# Platform Libraries
Set of functions that plugins can use these for executing remote commands, etc.

## run_bash

Executes a bash command on a remote Unix host.

### Signature

`def run_bash(remote_connection, command, variables=None, use_login_shell=False)`

### Arguments

Argument | Type | Description
-------- | ---- | -----------
remote_connection | [SourceConnection](Classes.md#sourceconnection) | Connection associated with the remote host to run the command on.
command | String | Command to run on the host.
variables | dict[String, String] | **Optional**. Environement variables to set when running the command.
use_login_shell | boolean | **Optional**. Whether to use a login shell.

### Returns
An object of `RunBashResponse`

Field | Type | Description
----- | ---- | -----------
exit_code | Integer | Exit code from the command.
stdout | String | Stdout from the command.
stderr | String | Stderr from the command.

### Examples

Calling bash with an inline command.

```python
from dlpx.virtualization import libs

command = "echo 'Hi' >> /tmp/debug.log"
vars = {"var": "val"}

response = libs.run_bash(connection, command, vars)

print response.exit_code
print response.stdout
print response.stderr
```

Using parameters to construct a bash command.

```python
from dlpx.virtualization import libs

name = virtual_source.parameters.username
port = virtual_source.parameters.port
command = "mysqldump -u {} -p {}".format(name,port)

response = libs.run_bash(connection, command)
```

Running a bash script that is saved in a directory.

```python
 
 import pkgutil
 from dlpx.virtualization import libs

 script_content = pkgutil.get_data('resources', 'get_date.sh')

 # Execute script on remote host
 response = libs.run_bash(direct_source.connection, script_content)
```
For more information please go to [Managing Scripts for Remote Execution](/Best_Practices/Managing_Scripts_For_Remote_Execution/) section.

## run_expect

Executes a tcl command or script on a remote Unix host.

### Signature

`def run_expect(remote_connection, command, variables=None)`

### Arguments

Argument | Type | Description
-------- | ---- | -----------
remote_connection | [SourceConnection](Classes.md#sourceconnection) | Connection associated with the remote host to run the command on.
command | String | Expect(Tcl) command to run.
variables | dict[String, String] | **Optional**. Environement variables to set when running the command.

### Returns

None

### Example

```python
from dlpx.virtualization import libs

command = "puts 'Hi'"
vars = {"var": "val"}

libs.run_expect(connection, command, vars)
```

## run_powershell

Executes a powershell command on a remote Windows host.

### Signature

`def run_powershell(remote_connection, command, variables=None)`

### Arguments

Argument | Type | Description
-------- | ---- | -----------
remote_connection | [SourceConnection](Classes.md#sourceconnection) | Connection associated with the remote host to run the command on.
command | String | Command to run to the remote host.
variables | dict[String, String] | **Optional**. Environement variables to set when running the command.

### Returns
An object of `RunPowershellResponse`

Field | Type | Description
----- | ---- | -----------
exit_code | Integer | Exit code from the command.
stdout | String | Stdout from the command.
stderr | String | Stderr from the command.

### Example

```python
from dlpx.virtualization import libs

command = "Write-Output 'Hi'"
vars = {"var": "val"}

response = libs.run_powershell(connection, command, vars)

print response.exit_code
print response.stdout
print response.stderr
```