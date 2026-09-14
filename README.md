 # SZD HOMEWORKS 
Repository with code for SZD1 and SZD2 homeworks. Homeworks are deployed [here](https://pages.github.com/) using ***github pages*** and ***Jupyter Book***
## Development enviroment setup
Create python enviroment:
```
# SZD HOMEWORKS

Repository with code for SZD1 and SZD2 homeworks. Homeworks are deployed using ***GitHub Pages*** and ***Jupyter Book***.

Lokální archiv webových stránek předmětu SZD se nachází ve složce `public_html/` a je dostupný přímo z online knihy:
* [Web předmětu SZD (přehled v knize)](source/szd_web.md)
* [Původní web předmětu SZD](/public_html/SZD/index.html?view)

## Development environment setup

Create python environment:
```bash


Clone dev branch of the repo to enviroment folder:
```

Clone dev branch of the repo to environment folder:
```bash



Activate python virtual enviroment:
- *Linux:*

Activate python virtual environment:
* Linux:
  ```bash
  source SZD/bin/activate
  ```
* Windows:
  ```powershell
  .SZD\Scripts\Activate.ps1
  ```

Install required packages:
```bash
pip install -r requirements.txt

source SZD/bin/activate
```
- *Windows:*
```
.SZD\Scripts\Activate.ps1
```
Install requered packages:
```
 pip install -r requirements.txt
```
Install QADA python virtual enviroment to Jupyter:
```

Install QADA python virtual environment to Jupyter:
```bash






```bash
jupyter-book build --html

jupyter book start
or to start a live development server:
```bash
jupyter-book start