# Contributing

## Git

Feel free to create a pull request for fixes and improvements. Make sure to write the content of the changes in the description of the pull request, and follow the rules to commit messages.

## Testing

Test your code before commiting. You should write your test cases where necessary. 

Test can be run as follows:

    path/to/zvm-exporter$ tox

## Commit messages

There are rules to commit messages which are ensured by GitCop. After you created a pull request, you will get several automated feedbacks including one from GitCop. The rules that are checked against are:

* Commit messages must start with a short summary line.
* It can include a more detailed description preceded by an empty line.
* It must end with the DCO sign-off. 
* No line should be more than 80 characters long. (Simply use line break to break long lines)

The [Developer Certificate of Origin (DCO)](DCO1.1.txt) certifies that you wrote the patch or otherwise have the right to pass it on as an open-source patch. 

In order to sign it, simply include the following lines at the end of the commit message.

    Signed-off-by: Random J Developer <random@developer.org>

Use your real name and a valid email address.

Example commit message:
```
Add tests for requester.py

It adds tests that verify the send_request function by sending dummy responses
using httpretty.

Signed-off-by: Ye Na Rhee <yrhee@de.ibm.com>
```

Use `git commit --amend` to edit the commit message, if you need to.
