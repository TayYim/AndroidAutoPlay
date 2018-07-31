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

    if rootView in currentViewList:
        performAction(rootView) 
        currentViewList.remove(rootView)

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
    currentActivity = stack[-1]
    currentViewList = dict.get(currentActivity)

    viewClass = view.getClass().split('.')[-1]

    # dbg
    print view.getClass()
    print view.getText()
    print view.getCenter()
    print '\n'

    # hide keyboard
    if vc.device.isKeyboardShown():
        vc.device.press('KEYCODE_BACK')

    if view.isScrollable():
        scrollId = view.getId()
        while(1):
            currentScrollView = vc.findViewById(scrollId)
            # delete itself from the list to avoid endless loop
            currentViewList.remove(currentScrollView)
            dfs(currentScrollView)
            oldViews = vc.dump()
            currentScrollView.uiScrollable.flingForward()
            newViews = vc.dump()

            if isSamePage(oldViews,newViews) :
                print "scroll over"
                # for "remove" command in dfs(), add the original view object to the view list
                currentViewList.append(view)
                break
            else :
                newScrollView = vc.findViewById(scrollId)
                currentViewList.extend(newScrollView.getChildren())
                # add the new scroll view to the list for calling dfs()
                currentViewList.append(newScrollView) 
                
    elif viewClass == 'EditText':
        view.setText('23333')

    elif view.isClickable() or view.isCheckable() or viewClass == 'TextView':
        print 'touch'
        view.touch()

    elif view.map.get('long-clickable') == u'true':
        print 'long touch'
        view.longTouch(2000)

    vc.sleep(0.1)

# judge if is the same page
def isSamePage(oldViews,newViews):
    if len(oldViews) != len(newViews):
        return False
    else:
        for view in zip(oldViews,newViews):
            if (view[0].map != view[1].map) :
                return False
        return True

# judge the type of scrollable component
def isVerticleScroll(view):
    oldViews = vc.dump()
    vc.sleep(2)
    view.uiScrollable.flingForward()
    newViews = vc.dump()
    vc.sleep(2)
    view.uiScrollable.flingBackward()
    if isSamePage(oldViews,newViews):
        return False
    else:
        return True

if __name__ == '__main__':
    vc = init()

    stack = []
    dict = {}

    mainActivity = vc.device.getFocusedWindowName()
    viewList = vc.dump()
    stack.append(mainActivity)
    dict[mainActivity] = viewList

    autoplay()
