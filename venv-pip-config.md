Virtual Environment allows the creation of isolated Python installation and install packages into that virtual installation. 
When switching projects, we can simply create a new virtual environment and not have to worry about breaking the packages installed in other environments.

for that:
`pip install --user virtualenv`

to create virtualenv:
`python -m venv env`

to activate virtualenv:
`.\env\Scripts\activate`

to deactivate virtualenv:
`deactivate`


just like package.json in npm we have requirements.txt in pip

we can set the dependencies in requirements.txt
and install using the command:
    `pip install -r requirements.txt`

inorder to create a requirements.txt file we can use the command:
    `pip freeze > requirements.txt` 
    this will create requirements.txt file according to the installed dependencies 

to uninstall pip package:
    `pip uninstall {package}`
    but this removes just the package and not its unused dependencies
    for that we need pip-autoremove

    install pip-autoremove
        `pip install pip-autoremove`
        remove "somepackage" plus its dependencies:
        `pip-autoremove somepackage -y`