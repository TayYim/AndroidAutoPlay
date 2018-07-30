from com.dtmilano.android.viewclient import ViewClient

_s = 1


kwargs1 = {'ignoreversioncheck': False, 'verbose': False, 'ignoresecuredevice': False}
device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
# device is a adbclient
kwargs2 = {'forceviewserveruse': False, 'useuiautomatorhelper': False, 'ignoreuiautomatorkilled': True, 'autodump': False, 'debug': {}, 'startviewserver': True, 'compresseddump': True}
vc = ViewClient(device, serialno, **kwargs2)

# main function
def handleViews():
    # get current activity
    currentActivity = activityStack[-1]
    print "current activity:" + currentActivity + '\n'
    # get views of current activity
    views = dict.get(currentActivity)
    viewSet = deepcopy(views)
    # for every component
    for view in viewSet:
        performAction(view)
        # remove the view visited
        views.remove(view)

        # handle new activity
        newActivity = device.getFocusedWindowName()
        if (currentActivity != newActivity) :
            activityStack.append(newActivity)
            # if has never been visited
            if not dict.has_key(newActivity):
                dict[newActivity] = vc.dump(window=-1)
            handleViews()

    # remove the activity finished
    activityStack.pop()
    # if there are activities left, go back to the stack top
    if(len(activityStack) > 0):
        device.startActivity(activityStack[-1])

def performAction(view):
    viewClass = view.getClass().split('.')[-1]
   
    # for debug
    print viewClass 
    print view.getCenter()
    print view.getText().encode("utf-8") + '\n'

    ## handle scrollable
    if view.isScrollable() :
        handleScrollable(view)

    # view.touch()

    vc.sleep(_s)

def handleScrollable(view):
    while(1):
        viewsCurrentPage = set(vc.dump())
        view.uiScrollable.flingForward()
        viewsNew = set(vc.dump())
        viewsSaved = dict.get(activityStack[-1])
        # print "\ncurrent:"
        # print viewsCurrentPage
        # print "\nnew:"
        # print viewsNew
        if viewsCurrentPage == viewsNew :
            print "over"
            break
        else :
            viewsSaved = viewsSaved.union(viewsNew)
    print viewsSaved

# for everything clickable
def handleClickable(view):
    viewClass = view.getClass().split('.')[-1]
    if viewClass == 'EditText':
        handleEditText(view)
    else:
        view.touch()

# type some text
def handleEditText(editText):
    editText.setText('23333')

# deep copy utils
def deepcopy(oldSet):
    newSet = set()
    for item in oldSet:
        newSet.add(item)
    return newSet


views = set(vc.dump(window=-1)) # as a set
mainActivity = device.getFocusedWindowName()
activityStack = [mainActivity]
dict = {mainActivity : views}
handleViews()
