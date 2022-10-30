# Virtual Environments

Virtual environments allow the user to manage depenedencies across multiple projects. Some projects might require different versions of different packages.

To create virtual environment, we use a tool called venv.

First create a new directory that will contain the virtual environment.

```bash
mkdir .venv
```

Proceed to create the virtualenv using this command

```bash
python -m venv .venv
```

Finally we need to activate the virtual environment using

On Unix or Mac:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.\.venv\Scripts\activate
```

Now you can safely install the dependencies

```bash
pip install -r requirements.txt
```

[Return to mainpage](../README.md)
