ECHO OFF
cd ..
python manage.py test --settings=superapi.settings.developments
cd scripts

REM cd ../src && pytest -s posts/tests/test_views.py -x --ipdb