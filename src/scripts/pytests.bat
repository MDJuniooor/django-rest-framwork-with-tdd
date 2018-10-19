ECHO OFF
cd ..
pytest -s posts/tests/test_async/test_celery_jobs.py -x
cd scripts

REM cd ../src && pytest -s posts/tests/test_views.py -x --ipdb