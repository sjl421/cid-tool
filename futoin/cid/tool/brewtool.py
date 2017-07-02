
from ..runenvtool import RunEnvTool


class brewTool(RunEnvTool):
    """Homebrew. The missing package manager for macOS.

Home: https://brew.sh/

brewInstall is use for admin user installation.
brewDir & brewGit is used for local install.

Hint: Unprivileged brew does not work well with many bottles, you may want to use
    brewSudo='/usr/bin/sudo -n -H -u adminaccount' with "cid sudoers" config.
"""
    __slots__ = ()

    _MACOS_ADMIN_GID = 80  # dirty hack for now
    _GLOBAL_BREW_DIR = '/usr/local'

    def envNames(self):
        return ['brewBin', 'brewDir', 'brewGit', 'brewInstall', 'brewSudo']

    def _installTool(self, env):
        if self._isLocalBrew(env):
            self._warn(
                'Unprivileged Homebrew install has many drawbacks. Check "cid tool describe brew"')
            homebrew_git = env['brewGit']
            homebrew_dir = env['brewDir']

            git = self._path.which('git')

            if not git:
                xcode_select = self._path.which('xcode-select')
                self._exec.callExternal(
                    [xcode_select, '--install'], suppress_fail=True)
                git = self._path.which('git')

            self._exec.callExternal([git, 'clone', homebrew_git, homebrew_dir])
        else:
            # should be system-available
            curl = self._path.which('curl')
            ruby = self._path.which('ruby')
            homebrew_install = env['brewInstall']

            curl_args = self._configutil.timeouts(env, 'curl')

            brew_installer = self._exec.callExternal(
                [curl, '-fsSL', homebrew_install] + curl_args
            )

            self._exec.callExternal([ruby, '-'], input=brew_installer)

    def _isLocalBrew(self, env):
        return env['brewDir'] != self._GLOBAL_BREW_DIR

        if self._MACOS_ADMIN_GID not in self._os.getgroups():
            return True

        return False

    def initEnv(self, env, bin_name=None):
        ospath = self._ospath
        os = self._os
        brewSudo = env.get('brewSudo', '')

        if self._MACOS_ADMIN_GID not in os.getgroups() and not brewSudo:
            homebrew_dir = ospath.join(self._environ['HOME'], '.homebrew')
            env.setdefault('brewDir', homebrew_dir)
        else:
            env.setdefault('brewDir', self._GLOBAL_BREW_DIR)

            if brewSudo:
                self._environ['brewSudo'] = brewSudo

        env.setdefault('brewGit',
                       'https://github.com/Homebrew/brew.git')
        env.setdefault('brewInstall',
                       'https://raw.githubusercontent.com/Homebrew/install/master/install')

        if self._isLocalBrew(env):
            homebrew_dir = env['brewDir']
            bin_dir = ospath.join(homebrew_dir, 'bin')
            brew = ospath.join(bin_dir, 'brew')

            if ospath.exists(brew):
                self._path.addBinPath(bin_dir, True)
                env['brewBin'] = brew
                self._have_tool = True
        else:
            env.setdefault('brewDir', self._GLOBAL_BREW_DIR)
            super(brewTool, self).initEnv(env, bin_name)
