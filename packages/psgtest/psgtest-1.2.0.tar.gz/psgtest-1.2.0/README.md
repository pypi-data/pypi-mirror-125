
<p align="center">
  <img src="https://raw.githubusercontent.com/PySimpleGUI/PySimpleGUI/master/images/for_readme/Logo%20with%20text%20for%20GitHub%20Top.png" alt="Python GUIs for Humans">
<br>  
     <img src="https://raw.githubusercontent.com/PySimpleGUI/PySimpleTest/main/images_for_readme/PySimpleTest%20Icon.png?token=ALAGMYZB22HOKH2A3OGNFJTBQ35R4" alt="Python GUIs for Humans">
  <h2 align="center">PySimpleTest</h2>
  <h2 align="center">Simple Python Testing</h2>


</p>

Run your Python programs using the interpreter version of your choice, and display the output in a GUI window.

## Installation

### Old-school Straight Pip

pip install pysimpletest

### pip via `python -m pip` the python recommended way

#### If `python` is your command

python -m pip install pysimpletest

#### If `python3` is your command

python3 -m pip install pysimpletest

## Usage

pysimpletest

## About

![](https://raw.githubusercontent.com/PySimpleGUI/PySimpleTest/main/images_for_readme/PySimpleTest%20Screenshot.jpg?token=ALAGMYZDX4APHZAELG2Z6O3BQ35OK)

This is an example of another utility used in the development of PySimpleGUI that is being released for other PySimpleGUI users to use either as a standalone tool or as example code / design pattern to follow.

It can be challenging to manage multiple versions of Python and the need to test across multiple versions.  Virtual Environments are one approach that is often used.  PySimpleTest does not use virtual environments.  Instead, it invokes the Python interpreter of your choice directly.

## Executing Multiple Programs

To run multiple programs, select the files to run from the list of files on the left portion of the window.  Then click the "Run" button.


## Editing Programs

You can also edit the programs selected by clicking the "Edit" button.  You will need to set up your editor using the PySimpleGUI global settings.  If you have pip installed a version of PySimpleGUI that's 4.53.0 or greater, then you can type `psgsettings` from the command line.  You can also change the settings by calling `sg.main()` (or typing from the command line `psgmain`).



## Output

The stdout and stderr from each program you execute will be displayed in a tab with a name that matches your filename.  Each program you run will open a new tab.

In each tab you'll find 2 buttons that operate on the output shown in that tab.

Use the `Copy To Clipboard` button to copy the contents of the output to the clipboard.  

Use the `Clear` button to delete the output.

## License

Licensed under an LGPL3 License

## Designed and Written By

Mike from PySimpleGUI.org

## Contributing

Like the PySimpleGUI project, this project is currently licensed under an open-source license, the project itself is structured like a proprietary product. Pull Requests are not accepted.

## Copyright

Copyright 2021 PySimpleGUI
