"""Adapter for DateTime adapter for WebThings Gateway."""

import logging
import time

from gateway_addon import Adapter
from .config import Config
from .date_device import DateTimeDevice  # , DateTimeTestDevice


class DateTimeAdapter(Adapter):
    """DateTime Adapter to make the rules support better date and time."""

    def __init__(self, verbose=False):
        """
        verbose -- enable verbose logging
        """
        self.name = self.__class__.__name__
        Adapter.__init__(self,
                         'date-time-adapter',
                         'date-time-adapter',
                         verbose=verbose)
        self._config = Config(self.package_name)
        self.start_pairing(1)

    def start_pairing(self, timeout):
        """  Start pairing process. """
        logging.debug('START Pairing')

        log_level = 30
        if self._config.log_level == 'INFO':
            logging.getLogger().setLevel(logging.INFO)
        elif self._config.log_level == 'DEBUG':
            logging.getLogger().setLevel(logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.WARNING)
        logging.info("Log level %s", log_level)

        dev_id = 'DateTimeDevice'
        if self.get_device(dev_id) is None:
            self.handle_device_added(DateTimeDevice(self, dev_id,
                                                    self._config))
        else:
            logging.debug('Device: %s was already created', dev_id)
        # dev_id = 'DateTimeTestDevice'
        # if self.get_device(dev_id) is None:
        #    self.handle_device_added(DateTimeTestDevice(self, dev_id,
        #                                 self._config))
        # else:
        #    logging.info('Device: %s was already created', dev_id)
        logging.debug('END Pairing')

    def cancel_pairing(self):
        """Cancel pairing process."""
        logging.debug('cancel_pairing')

    def unload(self):
        """Perform any necessary cleanup before adapter is shut down."""
        logging.debug('Start unload all devices')
        try:
            for device_id, device in self.get_devices().items():
                device.active_poll = False
            time.sleep(3)
            for dev_id, dev in self.get_devices().items():
                logging.debug('UNLOAD Device: %s', dev_id)
                super().unload()
        except Exception as ex:
            logging.exception('Exception %s', ex)
        logging.debug('End unload all devices')

    def handle_device_removed(self, device):
        logging.debug('Device to be removed name: %s is_alive: %s',
                      device.name, device.thread.is_alive())
        device.active_poll = False
        device.thread.join(20.0)
        logging.debug('Device id: %s is_alive: %s', device.id,
                      device.thread.is_alive())
        super().handle_device_removed(device)
        logging.debug('device:' + device.name + ' is removed. Device ' +
                      device.id)
