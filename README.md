Welcome to pyGameScanner!
=====================
[![Code Health](https://landscape.io/github/akshetpandey/pyGameScanner/master/landscape.png)](https://landscape.io/github/akshetpandey/pyGameScanner/master)

This code, written in python, scans the LAN and locates all multiplayer games that are running in in efficient and more importantly fast manner. The idea is to facilitate multiplayer gaming by showing available servers that a player can join.

This is a hobby project so expect bugs and any help is welcome.

As of now the following protocols are under development:

>- Steam (90% Done)

And I am going to work on the following protocols soon:

>- Gamespy 2
>- Gamespy 3
>- BattleNet
>- MSDirectPlay

Once all 5 protocols are supported the scanner should be able to pick up over 500 games.

Dependencies
-------------

    1. Requires Python2.7 (http://www.python.org/)
    2. Requires libraries listed in requirements.txt
    3. Requires a HTTP webserver (like apache/nginx) or a browser if you want to use it only for yourself

How To Use
-----------

To run the server,

- First install the dependencies *(Only needs to be done once)*<br>
$ ```pip install -r requirements.txt```

- Then setup the files inside a folder of your choice, run<br>
$ ```git clone https://github.com/akshetpandey/pyGameScanner```

- This will download the source code into a folder named **pyGameScanner**. Then run the configuration code which will setup the server according to your needs<br>
$ ```cd pyGameScanner/src && python runSetup.py```

- Make sure your HTTP server is running and support symlinking. Symlink a folder inside your HTTP server base directory to `<absolute path>/pyGameScanner/www`

- Then start the scanner from inside the `pyGameScanner/src` folder using<br>
$ ```python runServer.py```

- Browse to `http://localhost/<name_of_symlink>` to see the games start to populate, if there are any running.

Bug Reports
------------

In case of any problem/bugs or suggestions do create an issue in the issue tracker.

If you would like to contribute, do check out the TODO.md for a list of pending tasks<br>

If you can submit a patch for the bugs that would be awesome :)
