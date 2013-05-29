===============================================================================
ZenPacks.rhybydd.GCM
===============================================================================


About
-------------------------------------------------------------------------------
This ZenPack adds new event notification actions that are used by the
``zenactiond`` daemon.


Features
-------------------------------------------------------------------------------

The following event notification actions have been added:

GCM Device ID
  This action 

Configurable SNMP Trap
  This action allows for the port, community string, and SNMP protocol version
  to be specified.

User Command
  This action allows for environment variables to be set, and also allows per-
  user information to be extracted using TALES expressions.


Prerequisites
-------------------------------------------------------------------------------

==================  =========================================================
Prerequisite        Restriction
==================  =========================================================
Product             Zenoss 4.1.1 or higher
Required ZenPacks   None
Other dependencies  An Android (4.0.3+) device with Rhybudd (4.0+) installed https://play.google.com/store/apps/details?id=net.networksaremadeofstring.rhybudd 
==================  =========================================================


Limitations
-------------------------------------------------------------------------------
These notification actions are not able to provide immediate feedback as to
whether or not configuration information is correct, so the ``zenactiond.log``
file must be checked to ensure that the actions are working correctly.


Usage
-------------------------------------------------------------------------------
1. Install the Rhybudd app to your phone.

2. Configure the Zenoss server details, make a note of your 'Device ID'

3. Navigate to ``Events`` -> ``Triggers`` page.

4. Click on the ``Notifications`` menu item.

5. Click on the plus sign ('+') to add a new notification.

6. From the dialog box, specify the name of the notification and select the
   ``Rhybudd GCM Alert`` action.

7. Enable the notification and add a trigger to be associated with this action.

8. Click on the ``Contents`` tab.

9. Add the device ID found in step 2.

10. Click on the ``Submit`` button.


Installing
-------------------------------------------------------------------------------

Install the ZenPack via the command line and restart Zenoss::

    zenpack --install ZenPacks.rhybudd.GCM-<version>.egg
    zenoss restart


Removing
-------------------------------------------------------------------------------

To remove the ZenPack, use the following command::

    zenpack --remove ZenPacks.rhybudd.GCM
    zenoss restart


Troubleshooting
-------------------------------------------------------------------------------

The Zenoss support team will need the following output:

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
   console.


Appendix Related Daemons
-------------------------------------------------------------------------------

============  ===============================================================
Type          Name
============  ===============================================================
Notification  zenactiond
============  ===============================================================
