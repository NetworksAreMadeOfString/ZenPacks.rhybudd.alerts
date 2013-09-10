import routers

import logging
log = logging.getLogger('zen.Rhybudd')

import Globals

from Products.ZenModel.ZenossSecurity import ZEN_MANAGE_DMD
from Products.ZenModel.DataRoot import DataRoot
from Products.ZenModel.UserSettings import UserSettingsManager
from Products.ZenModel.ZenossInfo import ZenossInfo
from Products.ZenModel.ZenPackManager import ZenPackManager
from Products.ZenModel.ZenPack import ZenPack as ZenPackBase
from Products.ZenUtils.Utils import monkeypatch, unused
unused(Globals)

import pkg_resources

BROWSER_PAGE = 'rhybudd-gcm-page'
ACTION_NAME  = 'rhybuddgcm'

# Add "Rhybudd Push" to left navigation on Advanced / Settings page.
for klass in (DataRoot, UserSettingsManager, ZenossInfo, ZenPackManager):
    action = BROWSER_PAGE
    if klass == ZenPackManager:
        action = '../%s' % action

    fti = klass.factory_type_information[0]
    fti['actions'] = fti['actions'] + ({
        'id': BROWSER_PAGE,
        'name': 'Rhybudd Push',
        'action': action,
        'permissions': (ZEN_MANAGE_DMD,)
    },)

@monkeypatch('Products.ZenUI3.navigation.menuitem.PrimaryNavigationMenuItem')
def update(self):
    '''
    Update subviews for this PrimaryNavigationMenuItem.

    Post-processes default behavior to add our subview. This allows the
    secondary navigation bar to be rendered properly when the user is
    looking at the Rhybudd Push settings screen.
    '''
    # original gets injected into locals by monkeypatch decorator.
    original(self)

    if '/zport/dmd/dataRootManage' in self.subviews:
        self.subviews.append('/zport/dmd/%s' % BROWSER_PAGE)

def version():
    """
    Convenience function to determine the ZenPack version at runtime since
    it must be hardcoded in setup.py.
    """
    resources = pkg_resources.require(__name__)
    if not resources:
        return None

    return resources[0].version
