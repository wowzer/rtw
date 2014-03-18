Real Time Web
=============


Setup a virtual environment:

$ mkvirtualenv rtw


If you're running Mavericks, you'll have to run the following before running dependencies.
clang seems to be a bit too picky.

$ export CFLAGS=-Qunused-arguments
$ export CPPFLAGS=-Qunused-arguments


For each project run the appropriate requirements.txt file:

$ pip install -r requirements.txt
