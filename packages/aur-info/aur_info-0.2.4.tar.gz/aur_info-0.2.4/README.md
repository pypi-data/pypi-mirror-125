AUR-INFO
--------
Helper program to show package info for a package from Arch User Repository.

Installation
------------

    ```pip install aur-info```


Usage
-----

While inside the interpreter or writing a script:

```
    import aur_info as ai
    pkginfo = ai.get_info('package')
```

... which returns a result of the form:

```
pkginfo = {'name': 'Package',
 'maintainer': 'goofy',
 'last_packager': 'goofy',
 'votes': 1,
 'popularity': 0.000000,
 'created': '2016-01-07 07:50',
 'description': 'Package Description.',
 'git_url': 'https://aur.archlinux.org/packagerepo.git',
 'updated': '2020-01-05 11:33',
 'version': '3.1.1-3',
 'submitted': '2016-01-07 07:50'}
 ```
