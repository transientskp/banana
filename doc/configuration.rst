Configuration
-------------

All settings are defined in the python module :mod:`project.settings`. banana
first loads :mod:`project.settings.base` followed by
:mod:`project.settings.local`. When you start using banana for the firs
time, there will be no **local** file. You should copy
:mod:`project.settings.local_example` to
:mod:`project.settings.local` and adjust it to your environment. The **base**
should contains all settings which are required by Banana and you should not
modify this file. You should override, append or define new settings variables
in **local**.
