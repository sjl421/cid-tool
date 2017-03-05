
from __future__ import print_function, absolute_import

class PackageMixIn( object ):
    def _requireDeb(self, packages):
        apt_get = self._which('apt-get')
        
        if apt_get:
            self._trySudoCall(
                [apt_get, 'install', '-y'] + packages,
                errmsg = 'WARNING: you may need to install build deps manually !'
            )

    def _requireYum(self, packages):
        yum = self._which('yum')
        
        if yum:
            self._trySudoCall(
                [yum, 'install', '-y'] + packages,
                errmsg = 'WARNING: you may need to install build deps manually !'
            )

    def _requireZypper(self, packages):        
        zypper = self._which('zypper')

        if zypper:
            self._trySudoCall(
                [zypper, 'install', '-y'] + packages,
                errmsg='WARNING: you may need to install build deps manually !'
            )
            
    def _requireRpm(self, packages):
        self._requireYum(packages)
        self._requireZypper(packages)
    
    def _requirePackages(self, packages):
        self._requireDeb(packages)
        self._requireRpm(packages)