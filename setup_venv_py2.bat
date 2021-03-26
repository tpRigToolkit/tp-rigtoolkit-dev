if exist venv2 del venv2
"C:\Python27\Scripts\virtualenv.exe" venv2
cd venv2
cd Scripts
call activate
cd ..
cd ..
pip install -r requirements_tpdcc.txt
pip install -r requirements_tprigtoolkit.txt
pause