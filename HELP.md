# Helpful information

## Manage python versions on your machine

### Install pyenv

Run the following lines in your terminal to install [pyenv](https://github.com/pyenv/pyenv) on your machine. This will allow you to have multiple python versions installed on your machine.

First update your system and install all necessary packages:
`sudo apt update && sudo apt upgrade -y`

`sudo apt install git python3 curl make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python3-openssl`

Then install pyenv:
`curl https://pyenv.run | bash`

After installation you need to adjust your `.bashrc` 
E.g. run `nano ~/.bashrc` to edit it.

At the end of the file, add the following lines:

```
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc 
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc 
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
```

After saving the file with `CTRL + X, Y` you need to resource the `.bashrc` to have an effect in your terminal.

Just run `source  ~/.bashrc` to activate the changes.

Now you are able to use pyenv

### Installing python versions with pyenv

Check the version you have set in your `tox.ini`.
This version needs to be installed on your system, so the tox-environment can be activated.

Here we have an example content of the `tox.ini`:

```
[tox]
envlist=dev
skipsdist = True

[testenv]
basepython = python3.11
deps = -r{toxinidir}/requirements.txt
```

According to this, the version to use is `3.11`.
You can check which python 3.11 versions are available with pyenv by running:

`pyenv install --list | grep -i "3.11"`

E.g. the newest version available for `3.11` is `3.11.6`
So you can run `pyenv install 3.11.6` to install the newest version of `python3.11`.


