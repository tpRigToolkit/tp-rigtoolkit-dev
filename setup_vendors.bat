if exist vendors del vendors
mkdir vendors
cd vendors

REM Autodesk Maya vendors
mkdir maya
cd maya
mkdir 2017
mkdir 2018
mkdir 2019
mkdir 2020
mkdir 2022
"C:\Python27\Scripts\pip.exe" install numpy -t ./2017 -i https://pypi.anaconda.org/carlkl/simple
"C:\Python27\Scripts\pip.exe" install numpy -t ./2018 -i https://pypi.anaconda.org/carlkl/simple
"C:\Python27\Scripts\pip.exe" install numpy -t ./2019 -i https://pypi.anaconda.org/carlkl/simple
"C:\Python27\Scripts\pip.exe" install numpy -t ./2020 -i https://pypi.anaconda.org/carlkl/simple
"C:\Python37\Scripts\pip.exe" install numpy -t ./2022
cd ..
cd ..

pause