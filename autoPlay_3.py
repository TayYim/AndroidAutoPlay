from com.dtmilano.android.viewclient import ViewClient


def init():
    kwargs1 = {'ignoreversioncheck': False,
               'verbose': False, 'ignoresecuredevice': False}
    device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
    # device is a adbclient
    kwargs2 = {'forceviewserveruse': False, 'useuiautomatorhelper': False, 'ignoreuiautomatorkilled': True,
               'autodump': False, 'debug': {}, 'startviewserver': True, 'compresseddump': True}
    vc = ViewClient(device, serialno, **kwargs2)
    return vc


def autoplay():
    currentActivity = stack[-1]
    currentViewList = dict.get(currentActivity)
    currentRootView = currentViewList[0]
    dfs(currentRootView)
    # remove the activity finished
    stack.pop()
    # if there are activities left, go back to the stack top
    if(len(stack) > 0):
        vc.device.startActivity(stack[-1])



def dfs(rootView):
    currentActivity = stack[-1]
    currentViewList = dict.get(currentActivity)
    currentViewList.remove(rootView)

    performAction(rootView)

    # start new activity
    newActivity = vc.device.getFocusedWindowName()
    if (currentActivity != newActivity):
        stack.append(newActivity)
        # if the new activity has never been visited
        if not dict.has_key(newActivity):
            dict[newActivity] = vc.dump()
        autoplay()
    
    # traverse children
    for childView in rootView.getChildren():
        if childView in currentViewList:
            dfs(childView)


def performAction(view):

    viewClass = view.getClass().split('.')[-1]

    print viewClass
    print view.getText()
    print view.getCenter()
    print '\n'

    view.touch()

    vc.sleep(1)


if __name__ == '__main__':
    vc = init()

    stack = []
    dict = {}

    mainActivity = vc.device.getFocusedWindowName()
    viewList = vc.dump()
    stack.append(mainActivity)
    dict[mainActivity] = viewList

    autoplay()
