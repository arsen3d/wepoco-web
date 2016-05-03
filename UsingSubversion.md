# Subversion reference #

http://svnbook.red-bean.com/

# Using keywords #

By default svn doesn't substitute $Date$, $Author$, etc.  To use these you'll need to set the keywords property on new source files.

e.g.  `svn propset svn:keywords "Date Author Id" *.py`



