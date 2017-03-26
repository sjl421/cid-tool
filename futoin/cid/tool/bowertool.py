
import json
from collections import OrderedDict

from ..buildtool import BuildTool
from .npmtoolmixin import NpmToolMixIn

class bowerTool( NpmToolMixIn, BuildTool ):
    BOWER_JSON = 'bower.json'
    
    def autoDetect( self, config ) :
        return self._autoDetectByCfg( config, self.BOWER_JSON )

    def loadConfig( self, config ) :
        content = self._loadJSONConfig( self.BOWER_JSON )
        if content is None: return
        
        f = 'name'
        if f in content and f not in config:
            config[f] = content[f]

    def updateProjectConfig( self, config, updates ) :
        def updater( json ):
            f = 'name'
            if f in updates :
                    json[f] = updates[f]
                    
            # version is deprecated
            if 'version' in json:
                del json['version']

        return self._updateJSONConfig( self.BOWER_JSON, updater )
    
    def onPrepare( self, config ):
        bowerBin = config['env']['bowerBin']
        self._callExternal( [ bowerBin, 'install' ] )

    def onPackage( self, config ):
        bowerBin = config['env']['bowerBin']
        # TODO: not sure
        self._callExternal( [ bowerBin, 'install', '--production' ] )
    
