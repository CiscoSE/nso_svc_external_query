# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service
import requests


# ------------------------
# SERVICE CALLBACK EXAMPLE
# ------------------------
class ServiceCallbacks(Service):

    # ------------------------
    # HELPERS
    # ------------------------
    def makeCall(self,p_url, method):
        """
        Sample API call re-usable method
        :return:
        """
        methodName = ">>> makeCall: "
        
        self.log.info(methodName + "Sending " + method + " request to " + p_url)
        
        headers = {
            "Content-type": "application/json;"
        }
        if method == "GET":
            response = requests.get(p_url, headers=headers, verify=False)
        else:
            self.log.error(methodName + "HTTP Method not supported")
        if 199 < response.status_code < 300:
            return response.json()
        else:
            self.log.error(methodName + response.text)

    def getDescription(self,p_group):
        url="http://localhost:12345/api/description?group=" + p_group
        description = self.makeCall(p_url=url,method="GET")["description"]
        return description
    

    # The create() callback is invoked inside NCS FASTMAP and
    # must always exist.
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        methodName = ">>> cb_create: "
        self.log.info(methodName + 'Service create(service=', service._path, ')')

        vars = ncs.template.Variables()
        
        template = ncs.template.Template(service)
        
        for group in service.deviceGroups:
            # Print 
            for deviceName in root.devices.device_group[group.name].device_name:
                self.log.info(methodName + "Device group name " + group.name)
                self.log.info(methodName + "Device name " + deviceName)
                self.log.info(methodName + "+++++")

            group.devices = root.devices.device_group[group.name].device_name
            group.loopbackDescription = self.getDescription(group.name)
        vars.add('deviceGroups', service.deviceGroups)
        template.apply('api-group-example-template', vars)
        self.log.info(methodName + 'Completed')


    # The pre_modification() and post_modification() callbacks are optional,
    # and are invoked outside FASTMAP. pre_modification() is invoked before
    # create, update, or delete of the service, as indicated by the enum
    # ncs_service_operation op parameter. Conversely
    # post_modification() is invoked after create, update, or delete
    # of the service. These functions can be useful e.g. for
    # allocations that should be stored and existing also when the
    # service instance is removed.

    # @Service.pre_lock_create
    # def cb_pre_lock_create(self, tctx, root, service, proplist):
    #     self.log.info('Service plcreate(service=', service._path, ')')

    # @Service.pre_modification
    # def cb_pre_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')

    # @Service.post_modification
    # def cb_post_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')


# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')

        # Service callbacks require a registration for a 'service point',
        # as specified in the corresponding data model.
        #
        self.register_service('api-group-example-servicepoint', ServiceCallbacks)

        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')
