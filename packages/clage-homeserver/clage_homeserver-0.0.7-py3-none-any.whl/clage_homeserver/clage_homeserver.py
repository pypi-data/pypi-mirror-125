# -*- coding: utf-8 -*-

# API-documentation: https://app.swaggerhub.com/apis/klacol/ClageHomeServer/1.0.0

import requests
import datetime
from json import JSONDecodeError
from datetime import datetime
import urllib3

class ClageHomeServerStatusMapper:

    def __phaseDetection(self, phase, bit):
        if phase & bit:
            return 'on'
        else:
            return 'off'

    def mapApiStatusResponse(self, status):

        numberOfConnectedHeaters = 1  # I have only one heater, so i start with this scenario

        homeserver_version = ClageHomeServer.VERSION.get(status.get('version')) or 'unknown'       # 1.4
        homeserver_error = ClageHomeServer.ERROR.get(status.get('error')) or 'unknown'             # OK
        posixTimestamp = int(status.get('time', 0))                               # see https://www.epochconverter.com/
        homeserver_time = str(datetime.utcfromtimestamp(posixTimestamp))             # 1631263211 => Freitag, 10. September 2021 10:40:11 GMT+02:00 DST
        homeserver_success = bool(status.get('success'))                          # True
        homeserver_cached = bool(status.get('cached'))                            # True

        heater = status.get('devices')[numberOfConnectedHeaters-1]
        heater_id = heater.get('id')                                              # 2049DB0CD7
        heater_busId = heater.get('busId')                                        # 1
        heater_name = heater.get('name')                                          # ""
        heater_connected = bool(heater.get('connected'))                          # true
        heater_signal = heater.get('signal')                                      # -67
        heater_rssi = heater.get('rssi')                                          # 0
        heater_lqi = heater.get('lqi')                                            # 0

        heater_status = heater.get('status')
        heater_status_setpoint = float(heater_status.get('setpoint'))/10          # 600 => 60 °C
        heater_status_tIn = float(heater_status.get('tIn'))/10                    # 274 => 27.4 °C
        heater_status_tOut = float(heater_status.get('tOut'))/10                  # 244 => 24.4 °C
        heater_status_tP1 = float(heater_status.get('tP1'))/10                    # 0
        heater_status_tP2 = float(heater_status.get('tP2'))/10                    # 0
        heater_status_tP3 = float(heater_status.get('tP3'))/10                    # 0
        heater_status_tP4 = float(heater_status.get('tP4'))/10                    # 0
        heater_status_flow = float(heater_status.get('flow'))                     # 0
        heater_status_flowMax = float(heater_status.get('flowMax'))/100/1000      # 254 => 2.54 Liter => 0.00254 m³
        heater_status_valvePos = int(heater_status.get('valvePos'))               # 71 = 71 %
        heater_status_valveFlags = int(heater_status.get('valveFlags'))           # 0
        heater_status_power = float(heater_status.get('power'))                   # 0
        heater_status_powerMax = float(heater_status.get('powerMax'))/10          # 140 => 14 kW
        heater_status_power100 = float(heater_status.get('power100'))             # 0
        heater_status_fillingLeft = int(heater_status.get('fillingLeft'))         # 0
        heater_status_flags = int(heater_status.get('flags'))                     # 1
        heater_status_sysFlags = int(heater_status.get('sysFlags'))               # 0
        heater_status_error = ClageHomeServer.ERROR.get(heater_status.get('error')) or 'unknown'  # OK

        return ({
            'homeserver_version': homeserver_version,
            'homeserver_error': homeserver_error,
            'homeserver_time': homeserver_time,
            'homeserver_success': homeserver_success,
            'homeserver_cached': homeserver_cached,
            'heater_id': heater_id,
            'heater_busId': heater_busId,
            'heater_name': heater_name,
            'heater_connected': heater_connected,
            'heater_signal': heater_signal,
            'heater_rssi': heater_rssi,
            'heater_lqi': heater_lqi,
            'heater_status_setpoint': heater_status_setpoint,
            'heater_status_tIn': heater_status_tIn,
            'heater_status_tOut': heater_status_tOut,
            'heater_status_tP1': heater_status_tP1,
            'heater_status_tP2': heater_status_tP2,
            'heater_status_tP3': heater_status_tP3,
            'heater_status_tP4': heater_status_tP4,
            'heater_status_flow': heater_status_flow,
            'heater_status_flowMax': heater_status_flowMax,
            'heater_status_valvePos': heater_status_valvePos,
            'heater_status_valveFlags': heater_status_valveFlags,
            'heater_status_power': heater_status_power,
            'heater_status_powerMax': heater_status_powerMax,
            'heater_status_power100': heater_status_power100,
            'heater_status_fillingLeft': heater_status_fillingLeft,
            'heater_status_flags': heater_status_flags,
            'heater_status_sysFlags': heater_status_sysFlags,
            'heater_status_error': heater_status_error,
        })


class ClageHomeServer:

    ipAddress = ""
    homeserverId = ""
    heaterId = ""
    username = "appuser"
    password = "smart"

    def __init__(self, ipAddress, homeserverId, heaterId):
        if (ipAddress is None or ipAddress == ''):
            raise ValueError("ipAddress must be specified")
        self.ipAddress = ipAddress
        if (homeserverId is None or homeserverId == ''):
            raise ValueError("homeserverId must be specified")
        self.homeserverId = homeserverId
        if (heaterId is None or heaterId == ''):
            raise ValueError("heaterId must be specified")
        self.heaterId = heaterId


    VERSION = {
        '1.4': '1.4'
    }

    ERROR = {
        0: 'OK',
        1: 'Known, but not documented',
        3: 'Known, but not documented',
        8: 'Known, but not documented',
        10: 'Known, but not documented'
    }

    def __queryStatusApi(self):
        try:
            urllib3.disable_warnings()
            
            # Use HTTP Long Polling (lp); see API docs
            # rev=1; 
            # while (1): 
            #     url = "https://"+self.ipAddress+"/devices?lp="+str(rev)+"&showBusId=1&showErrors=1&showLogs=1&showTotal=1"   
            #     long_polling_timeout = 35 # greater than 30 Seconds; after 30 Seconds the server terminated the long polling request automatically
            #     statusRequest = requests.get(url, auth=(self.username, self.password), timeout=long_polling_timeout, verify=False)
            #     status_resonse_json = statusRequest.json() 
            #     rev_old=rev
            #     rev=status_resonse_json['rev']
            #     temperature = status_resonse_json['devices'][0]['info']['setpoint']
            #     if (rev != rev_old):
            #       print(str(datetime.today()) + ' - changed: setpoint = '+str(int(temperature)/10) + ' °C')
            #     else:
            #       print(str(datetime.today()) + ' - unchanged: setpoint = '+str(int(temperature)/10) + ' °C')   
            

            url = "https://"+self.ipAddress+"/devices/status/"+self.heaterId
            statusRequest = requests.get(url, auth=(self.username, self.password), timeout=5, verify=False)
            status = statusRequest.json()
            return status
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            return {}

    def setTemperature(self, temperature):
        tempApiValue = str(int(temperature*10))
        url = "https://"+self.ipAddress+"/devices/setpoint/"+self.heaterId
        body = {'data': tempApiValue, 'cid': '1'}

        setRequest = requests.put(url=url, auth=(self.username, self.password), data=body, timeout=5, verify=False)
        return ClageHomeServerStatusMapper().mapApiStatusResponse(setRequest.json())

    def requestStatus(self):
        response = {}
        try:
            status = self.__queryStatusApi()
            response = ClageHomeServerStatusMapper().mapApiStatusResponse(status)
        except JSONDecodeError:
            response = ClageHomeServerStatusMapper().mapApiStatusResponse({})
        return response

######################################################################################
# from clage_homeserver import ClageHomeserver
# clageHomeServer = ClageHomeServer('192.168.0.78','F8F005DB0CD7','2049DB0CD7') # <- change to your charger IP, your homeServerId and your heaterId
# response = clageHomeServer.requestStatus()
#
# clageHomeServer.setTemperature(44)
#
# print(response)
#
######################################################################################
