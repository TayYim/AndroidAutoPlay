from com.dtmilano.android.viewclient import ViewClient


def init(pause=1):
    _s = pause
    kwargs1 = {'ignoreversioncheck': False,
               'verbose': False, 'ignoresecuredevice': False}
    device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
    # device is a adbclient
    kwargs2 = {'forceviewserveruse': False, 'useuiautomatorhelper': False, 'ignoreuiautomatorkilled': True,
            'autodump': False, 'debug': {}, 'startviewserver': True, 'compresseddump': True}
    vc = ViewClient(device, serialno, **kwargs2)
    return vc
    

if __name__ == '__main__':
    vc = init(1)
