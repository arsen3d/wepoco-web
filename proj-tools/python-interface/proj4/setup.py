from distutils.core import setup, Extension

module1 = Extension("proj4",
                    include_dirs = ["/usr/local/include"],
                    libraries = ["proj"],
                    library_dirs = ["/usr/local/lib"],
                    sources = ["proj4.c"])

setup (name = "Proj4",
       version = "0.2",
       description = "This is a simple interface to Proj4",
       author = "Michael Saunby",
       author_email = "mike@saunby.net",
       url = "http://mike.saunby.net/",
       ext_modules = [module1])
