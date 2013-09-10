(function(){
    Ext.onReady(function(){
        var gcm_router = Zenoss.remote.RhybuddGCMRouter;

        Ext.define('net.networksaremadeofstring.rhybydd.ConfigureGCM', {
            extend: 'Ext.form.Panel',
            alias: 'widget.net.networksaremadeofstring.rhybudd.gcm-panel',
            title: 'Rhybudd Self Managed GCM Settings',
            id: 'rhybuddGCMPanel',
            defaults: {
                listeners: {
                    specialkey: function(field, event) {
                        if (event.getKey() == event.ENTER) {
                           field.up('form').submit();
                        }
                    }
                }
            },
            items: [
                {
                    fieldLabel: 'GCM API Key',
                    labelWidth: 150,
                    name: 'gcm_api_key',
                    width: 400,
                    xtype: 'textfield',
                    style: {
                        marginLeft: '15px',
			marginTop: '15px'
                    }
                },
                {
                    fieldLabel: 'GCM Sender ID',
                    labelWidth: 150,
                    name: 'gcm_sender_id',
                    width: 400,
                    xtype: 'textfield',
                    style: {
                        marginLeft: '15px',
                        marginTop: '5px'
                    }
                },
                {
                    xtype: 'button',
                    text: 'Apply',
                    style: {
                        marginBottom: '15px',
			marginLeft: '15px'
                    },
                    handler: function() {
                        var panel = Ext.getCmp('rhybuddGCMPanel');
                        panel.submit();
                    }
                },
            ],
            onRender: function() {
                this.callParent(arguments);
		this.load();
            },
            load: function() {
                gcm_router.get_gcm_settings({}, function(result) 
		{
                    if (!result.success)
                        return;

                    this.getForm().setValues(result.data);
                }, this);
            },
            submit: function() {
                var values = this.getForm().getValues();
                gcm_router.update_gcm_settings(values, function(result) {});
            },
        });

        var settings = Ext.create(net.networksaremadeofstring.rhybydd.ConfigureGCM, {
            renderTo: 'rhybudd-gcm'
        });

    }); // End Ext.onReady.
})(); // End closure.
