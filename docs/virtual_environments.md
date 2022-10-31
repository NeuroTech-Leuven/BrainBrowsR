# Virtual Environments

Virtual environments allow the user to manage dependencies across multiple projects. Some projects might require different versions of different packages.

To create a virtual environment, we use a tool called venv.

First, create a new directory that will contain the virtual environment.

```bash
mkdir .venv
```

Proceed to create the virtual env using this command

```bash
python -m venv .venv
```

Finally, we need to activate the virtual environment using on Unix or Mac:

```bash
source .venv/bin/activate
```

and on Windows:

```powershell
.\.venv\Scripts\activate
```

Now the dependencies can be safely installed

```bash
pip install -r requirements.txt
```

[Return to mainpage](../README.md)
