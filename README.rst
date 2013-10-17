===============================================================================
ZenPacks.rhybudd.alerts
===============================================================================


About
-------------------------------------------------------------------------------
This ZenPack adds new event notification actions that are used by the
``zenactiond`` daemon to instantly deliver alerts to any Rhybudd enabled Android
devices.


Features
-------------------------------------------------------------------------------

The following event notification actions have been added:

Send Alert to Rhybudd
  This action allows Zenoss to push events directly to Android devices that have
  the Rhybudd App installed.
  
  Alert delivery is usually sub-second.
  
  Rhybudd is free, open source and available from http://bit.ly/ZenossAndroid


Prerequisites
-------------------------------------------------------------------------------

==================  =========================================================
Prerequisite        Restriction
==================  =========================================================
Product             Zenoss 4.1.1 or higher / ZaaS *(any version)*
Required ZenPacks   None
Other dependencies  An Android (4.0.3+) device with Rhybudd (4.0+) http://bit.ly/ZenossAndroid 
==================  =========================================================


Limitations
-------------------------------------------------------------------------------
These notification actions are not able to provide immediate feedback as to
whether or not configuration information is correct, so the ``zenactiond.log``
file must be checked to ensure that the actions are working correctly.

Rhybudd must be installed to your phone or tablet and the steps detailed in the 
usage section below must be followed.

===============
Usage
===============

Phone / Tablet:
-------------------------------------------------------------------------------

**New Install:**

1. Install the Rhybudd app to your phone.
2. Configure the Zenoss server details (URL, username & password)
3. Tap the ``Configure Rhybudd Push`` Tab
4. Confirm all tests pass
5. *[Optional]* Add an event filter *(see below for server side configuration of filters)*

**Existing Install upgraded to Rhybudd 4.0**

1. Load up the app
2. Tap the Home / Drawer menu icon
3. Choose ``Configure Rhybudd Push``
4. Confirm all tests pass
5. *[Optional]* Add an event filter *(see below for server side configuration of filters)*

Zenoss:
-------------------------------------------------------------------------------

**Basic Configuration:**


1. Navigate to ``Events -> Triggers`` page.

2. Click on the ``Notifications`` menu item.

3. Click on the plus sign ('+') to add a new notification.

4. From the dialog box, specify the name of the notification and select the
   ``Send Alert to Rhybudd`` action.

5. Enable the notification and add a trigger to be associated with this action.


**Configuring Filters:**

1. Follow steps 1 - 4 of Basic Configuration

2. Click on the ``Contents`` tab.

3. Input a "Filter Key"

4. Click on the ``Submit`` button.

5. On your Android device tap the Home / Drawer menu icon

6. Choose ``Configure Rhybudd Push``

7. Confirm all tests pass

8. Add the Filter key from Step 3 into the edit box. Tap Back or the Home button on the ActionBar

**Advanced Configuration:**

To prevent your alerts traversing the ColdStart.io infrastructure and instead have them go straight to your phone (*via Google GCM)* do the following;

1. Login to Zenoss and navigate to ``Advanced``

2. Select ``Rhybudd Push`` from the left hand menu

3. Follow the instructions from Google to create a GCM key http://developer.android.com/google/gcm/gs.html

4. Add the ``GCM API Key`` and ``Sender ID`` to the page, press ``submit``

5. On your phone load the app, tap the Home icon, choose ``Configure Rhybudd Push``, tap the refresh icon on the action bar. *(This will update the local Sender ID and change the GCM Registration ID if neccessary)*


Installing
-------------------------------------------------------------------------------

Install the ZenPack via the command line and restart Zenoss::

    zenpack --install ZenPacks.rhybudd.alerts-<version>.egg
    zenoss restart


Removing
-------------------------------------------------------------------------------

To remove the ZenPack, use the following command::

    zenpack --remove ZenPacks.rhybudd.alerts
    zenoss restart


Troubleshooting
-------------------------------------------------------------------------------

To assist with any troubleshooting the aither will need the following output:

1. Set the ``zenhub`` daemon into ``DEBUG`` level logging by typing
   ``zenhub debug`` from the command-line. This will ensure that we can see the
   incoming event in the ``zenhub.log`` file.

2. Set the ``zenactiond`` daemon into ``DEBUG`` level logging by typing
   ``zenactiond debug`` from the command-line. This will ensure that we can see
   the incoming notification request and processing activity in the
   ``zenactiond.log`` file.

3. Create an event from the remote source, by the ``zensendevent`` command or by
   the event console ``Add an Event`` button. This event must match the trigger
   definition that will invoke your notification action.

4. Verify that the event was processed by the ``zenhub`` daemon by examining the
   ``zenhub.log`` file.

5. Wait for the ``zenactiond`` daemon to receive and then process the
   notification request.

6. In the case of errors an event will be generated and sent to the event
   console or the zen log on the local file system.


Appendix Related Daemons
-------------------------------------------------------------------------------

============  ===============================================================
Type          Name
============  ===============================================================
Notification  zenactiond
============  ===============================================================
