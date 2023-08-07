/*
    Todo:
      - how do I need to schedule playerInfo request to keep polling low and new song detection fast?
      -
*/
function f_pi3dpf_create_objects() {
  /* window.origin is set to https://alexa.amazon.de */
  if (! window.hasOwnProperty('pi3dpf') ) {
    window.pi3dpf = {}
  }
  if (! window.pi3dpf.hasOwnProperty('devices')) {
    window.pi3dpf['devices'] = {}
    window.pi3dpf.devices['seq_nbr'] = 0
    window.pi3dpf.devices['content'] = null
  }
  if (! window.pi3dpf.hasOwnProperty('playerInfo') ) {
    window.pi3dpf['playerInfo'] = {}
    window.pi3dpf.playerInfo['seq_nbr'] = 0
    window.pi3dpf.playerInfo['content'] = {}
  }
}
function t() {return new Date().toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', second: 'numeric', hour12: false })}
function log(msg){ console.log(t() +' '+msg)}
function nfo(msg){ console.info(t() +' '+msg)}
function dbg(msg){ console.debug(t() +' '+msg)}
function wrn(msg){ console.warn(t() +' '+msg)}
function err(msg){ console.error(t() +' '+msg)}

f_pi3dpf_create_objects();


(function(XHR) {
    /* From: https://stackoverflow.com/a/10796951 */
    "use strict";


    var open = XHR.prototype.open;
    var send = XHR.prototype.send;

    XHR.prototype.open = function(method, url, async, user, pass) {
        this._url = url;
        window.myXHR = XHR.prototype
        // console.log(user) #undefined
        // console.log(pass) # undefined
        open.call(this, method, url, async, user, pass);
    };

    XHR.prototype.send = function(data) {
        var self = this;
        var oldOnReadyStateChange;
        var url = this._url;

        function onReadyStateChange() {
            if(self.readyState == 4 /* complete */) {
                var responseType = self.responseType == "" ? 'string' : self.responseType
                nfo(responseType)
                var rt = {}
                if (self.responseType == "") {
                    try {
                        rt = JSON.parse(self.response)
                    } catch (e) { void(0)}
                }
                else {
                    rt = self.response
                }

                var fst_key = ""
                try {
                    fst_key = '"' + Object.keys(rt)[0] + '"'
                } catch(e) {void(0)}
                nfo('message type '+fst_key+' received')
                console.log(self)
                if (["playerInfo", "devices"].includes(Object.getOwnPropertyNames(rt)[0])) {
                    // decode and print received data for response of interest
                    console.log(rt)
                }
                if (rt.hasOwnProperty("devices")) {
                    var must_update = false
                    // check if pi3dpf.devices needs update
                    if (window.pi3dpf.devices.content == null ||
                        Object.keys(window.pi3dpf.devices.content.devices).length != Object.keys(rt.devices).length) {
                        must_update = true
                    }
                    else {
                        var i
                        for (i=0; i < Object.keys(rt.devices).length; i++) {
                            if (window.pi3dpf.devices.content.devices[i].accountName != rt.devices[i].accountName ||
                                window.pi3dpf.devices.content.devices[i].serialNumber != rt.devices[i].serialNumber ||
                                window.pi3dpf.devices.content.devices[i].clusterMembers.length != rt.devices[i].clusterMembers.length ||
                                window.pi3dpf.devices.content.devices[i].parentClusters.length != rt.devices[i].parentClusters.length) {
                                    must_update = true
                                    break
                                }
                            else {
                                var k
                                for (k=0; k < rt.devices[i].clusterMembers.length; k++) {
                                    if (window.pi3dpf.devices.content.devices[i].clusterMembers[k] != rt.devices[i].clusterMembers[k]) {
                                        must_update = true
                                    }
                                }
                                for (k=0; k < rt.devices[i].parentClusters.length; k++) {
                                    if (window.pi3dpf.devices.content.devices[i].parentClusters[k] != rt.devices[i].parentClusters[k]) {
                                        must_update = true
                                    }
                                }
                            }
                        }
                    }
                    if (must_update) {
                        window.pi3dpf.devices['seq_nbr'] += 1
                        window.pi3dpf.devices['content'] = rt
                    }
                    else {
                        dbg("'devices' message received, update on window.pi3dpf.devices not necessary")
                    }
                }
                else if (rt.hasOwnProperty("playerInfo")) {
                    if (window.pi3dpf.devices.content != null) {
                        var serialNumber = null
                        var accountName = null
                        // check if multi-room music group is active
                        if (rt.playerInfo.isPlayingInLemur) {
                            var echo_device = 'unidentified'
                            serialNumber = rt.playerInfo.playingInLemurId
                            // identify active serialNumber(=sort of Amazon MAC address) and accountName(= user assigned device name)
                            if (window.pi3dpf.playerInfo.content.hasOwnProperty(serialNumber) ) {
                                if (window.pi3dpf.playerInfo.content[serialNumber].hasOwnProperty('accountName') &&
                                   window.pi3dpf.playerInfo.content[serialNumber].accountName != null ) {
                                    accountName = window.pi3dpf.playerInfo.content[serialNumber].accountName
                                }
                                else {
                                    var i
                                    for (i=0; i < window.pi3dpf.devices.content.devices.length; i++) {
                                        if (window.pi3dpf.devices.content.devices[i].serialNumber == serialNumber ) {
                                            echo_device = window.pi3dpf.devices.content.devices[i].accountName
                                            accountName = window.pi3dpf.devices.content.devices[i].accountName
                                        }
                                    }
                                }
                            }
                        }
                        else {
                            // no multi-room music group active, must be a single device then
                            var url = new URL(self._url)
                            serialNumber = url.searchParams.get('deviceSerialNumber')
                            var i
                            for (i=0; i < pi3dpf.devices.content.devices.length; i++) {
                                if (pi3dpf.devices.content.devices[i].serialNumber == serialNumber) {
                                    accountName = pi3dpf.devices.content.devices[i].accountName
                                    break
                                }
                            }

                        }
                        if (serialNumber != null) {
                            window.pi3dpf.playerInfo['seq_nbr'] += 1
                            window.pi3dpf.playerInfo['content'][serialNumber] = rt.playerInfo
                            window.pi3dpf.playerInfo['content'][serialNumber].accountName = accountName
                            nfo('playerInfo message stored in pi3dpf.playerInfo.content.' + serialNumber+
                            ' (accountName='+accountName+').')
                        }
                        else {
                            nfo('serial number is null!')
                            console.log(self)
                        }
                    }
                    else {
                        nfo('processing playerInfo must wait for pi3dpf.devices to initialize')
                    }
                }
            }

            if(oldOnReadyStateChange) {
                oldOnReadyStateChange();
            }
        }

        /* Set xhr.noIntercept to true to disable the interceptor for a particular call */
        if(!this.noIntercept) {            
            if(this.addEventListener) {
                this.addEventListener("readystatechange", onReadyStateChange, false);
            } else {
                oldOnReadyStateChange = this.onreadystatechange; 
                this.onreadystatechange = onReadyStateChange;
            }
        }

        send.call(this, data);
    }
})(XMLHttpRequest);
