from docopt import docopt
if __name__ == '__main__':
    helpdoc = """turbo init project, server or app.
    Usage:
      turbo-admin (-h | --help)
      turbo-admin startproject  <project>
      turbo-admin startserver   <server>
      turbo-admin startapp      <app>
      turbo-admin index         <model_name>

    Options:
      -h,  --help        Show help document
    """

    rgs = docopt(helpdoc)
    if rgs.get('startproject'):
        print "startproject..."
    else:
        print "no startproject..."


    if rgs.get('startserver'):
        print "startserver..."
    else:
    	print "no startserver..."

    if rgs.get('startapp'):
        print "startapp..."
    else:
    	print "no startapp..."

    if rgs.get('index'):
        print "index..."
    else:
        print "no index..."


