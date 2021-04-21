import os, shutil, re, zipfile, esprima, codecs, json
from crx_unpack import unpack

PERMISSIONS_NEEDED = ['chrome.downloads','webview','chrome.declarativeContent','chrome.declarativeWebRequest','chrome.contentSetting.clear', 'chrome.contentSetting.set', 'chrome.alarms.create', 'chrome.alarms.get', 'chrome.alarms.getAll', 'chrome.alarms.clear', 'chrome.alarms.clearAll', 'chrome.alarms.onAlarm', 'chrome.audio.getDevices', 'chrome.audio.setActiveDevices', 'chrome.audio.setProperties', 'chrome.audio.getMute', 'chrome.audio.setMute', 'chrome.audio.onLevelChanged', 'chrome.audio.onMuteChanged', 'chrome.audio.onDeviceListChanged', 'chrome.bookmarks.get', 'chrome.bookmarks.getChildren', 'chrome.bookmarks.getRecent', 'chrome.bookmarks.getTree', 'chrome.bookmarks.getSubTree', 'chrome.bookmarks.search', 'chrome.bookmarks.create', 'chrome.bookmarks.move', 'chrome.bookmarks.update', 'chrome.bookmarks.remove', 'chrome.bookmarks.removeTree', 'chrome.bookmarks.MAX_WRITE_OPERATIONS_PER_HOUR', 'chrome.bookmarks.MAX_SUSTAINED_WRITE_OPERATIONS_PER_MINUTE', 'chrome.bookmarks.onCreated', 'chrome.bookmarks.onRemoved', 'chrome.bookmarks.onChanged', 'chrome.bookmarks.onMoved', 'chrome.bookmarks.onChildrenReordered', 'chrome.bookmarks.onImportBegan', 'chrome.bookmarks.onImportEnded', 'chrome.management.getAll', 'chrome.management.get', 'chrome.management.getPermissionWarningsById',  'chrome.management.setEnabled', 'chrome.management.uninstall','chrome.management.launchApp', 'chrome.management.createAppShortcut', 'chrome.management.setLaunchType', 'chrome.management.generateAppForLink', 'chrome.management.canInstallReplacementAndroidApp', 'chrome.management.installReplacementAndroidApp', 'chrome.management.installReplacementWebApp', 'chrome.management.onInstalled', 'chrome.management.onUninstalled', 'chrome.management.onEnabled', 'chrome.management.onDisabled',  'chrome.browser.openTab', 'chrome.browsingData.settings', 'chrome.browsingData.remove', 'chrome.browsingData.removeAppcache', 'chrome.browsingData.removeCache', 'chrome.browsingData.removeCacheStorage', 'chrome.browsingData.removeCookies', 'chrome.browsingData.removeDownloads', 'chrome.browsingData.removeFileSystems', 'chrome.browsingData.removeFormData', 'chrome.browsingData.removeHistory', 'chrome.browsingData.removeIndexedDB', 'chrome.browsingData.removeLocalStorage', 'chrome.browsingData.removePluginData', 'chrome.browsingData.removePasswords', 'chrome.browsingData.removeServiceWorkers', 'chrome.browsingData.removeWebSQL', 'navigator.clipboard.readText', 'navigator.clipboard.writeText', 'chrome.contextMenus.create', 'chrome.contextMenus.update', 'chrome.contextMenus.remove', 'chrome.contextMenus.removeAll', 'chrome.contextMenus.ACTION_MENU_TOP_LEVEL_LIMIT', 'chrome.contextMenus.onClicked', 'chrome.contentSettings.cookies', 'chrome.contentSettings.images', 'chrome.contentSettings.javascript', 'chrome.contentSettings.location', 'chrome.contentSettings.plugins', 'chrome.contentSettings.popups', 'chrome.contentSettings.notifications', 'chrome.contentSettings.fullscreen', 'chrome.contentSettings.mouselock', 'chrome.contentSettings.microphone', 'chrome.contentSettings.camera', 'chrome.contentSettings.unsandboxedPlugins', 'chrome.contentSettings.automaticDownloads', 'chrome.cookies.get', 'chrome.cookies.getAll', 'chrome.cookies.set', 'chrome.cookies.remove', 'chrome.cookies.getAllCookieStores', 'chrome.cookies.onChanged', 'chrome.debugger.attach', 'chrome.debugger.detach', 'chrome.debugger.sendCommand', 'chrome.debugger.getTargets', 'chrome.debugger.onEvent', 'chrome.debugger.onDetach', 'chrome.declarativeContent.onPageChanged', 'chrome.declarativeNetRequest.updateDynamicRules', 'chrome.declarativeNetRequest.getDynamicRules', 'chrome.declarativeNetRequest.updateEnabledRulesets', 'chrome.declarativeNetRequest.getEnabledRulesets', 'chrome.declarativeNetRequest.getMatchedRules', 'chrome.declarativeNetRequest.setActionCountAsBadgeText', 'chrome.declarativeNetRequest.MAX_NUMBER_OF_RULES', 'chrome.declarativeNetRequest.MAX_NUMBER_OF_DYNAMIC_RULES', 'chrome.declarativeNetRequest.GETMATCHEDRULES_QUOTA_INTERVAL', 'chrome.declarativeNetRequest.MAX_GETMATCHEDRULES_CALLS_PER_INTERVAL', 'chrome.declarativeNetRequest.MAX_NUMBER_OF_REGEX_RULES', 'chrome.declarativeNetRequest.MAX_NUMBER_OF_STATIC_RULESETS', 'chrome.declarativeNetRequest.DYNAMIC_RULESET_ID', 'chrome.declarativeNetRequest.onRuleMatchedDebug', 'chrome.desktopCapture.chooseDesktopMedia', 'chrome.desktopCapture.cancelChooseDesktopMedia',  'chrome.downloads.download', 'chrome.downloads.search', 'chrome.downloads.pause', 'chrome.downloads.resume', 'chrome.downloads.cancel', 'chrome.downloads.getFileIcon', 'chrome.downloads.open', 'chrome.downloads.show', 'chrome.downloads.showDefaultFolder', 'chrome.downloads.erase', 'chrome.downloads.removeFile', 'chrome.downloads.acceptDanger', 'chrome.downloads.setShelfEnabled', 'chrome.downloads.onCreated', 'chrome.downloads.onErased', 'chrome.downloads.onChanged', 'chrome.downloads.onDeterminingFilename', 'chrome.fileSystem.getDisplayPath', 'chrome.fileSystem.getWritableEntry', 'chrome.fileSystem.isWritableEntry', 'chrome.fileSystem.chooseEntry', 'chrome.fileSystem.restoreEntry', 'chrome.fileSystem.isRestorable', 'chrome.fileSystem.retainEntry', 'chrome.fileSystem.requestFileSystem', 'chrome.fileSystem.getVolumeList', 'chrome.fileSystem.onVolumeListChanged', 'chrome.fontSettings.clearFont', 'chrome.fontSettings.getFont', 'chrome.fontSettings.setFont', 'chrome.fontSettings.getFontList', 'chrome.fontSettings.clearDefaultFontSize', 'chrome.fontSettings.getDefaultFontSize', 'chrome.fontSettings.setDefaultFontSize', 'chrome.fontSettings.clearDefaultFixedFontSize', 'chrome.fontSettings.getDefaultFixedFontSize', 'chrome.fontSettings.setDefaultFixedFontSize', 'chrome.fontSettings.clearMinimumFontSize', 'chrome.fontSettings.getMinimumFontSize', 'chrome.fontSettings.setMinimumFontSize', 'chrome.fontSettings.onFontChanged', 'chrome.fontSettings.onDefaultFontSizeChanged', 'chrome.fontSettings.onDefaultFixedFontSizeChanged', 'chrome.fontSettings.onMinimumFontSizeChanged', 'chrome.gcm.send', 'chrome.gcm.register', 'chrome.gcm.unregister', 'chrome.gcm.MAX_MESSAGE_SIZE', 'chrome.gcm.onMessage', 'chrome.gcm.onMessagesDeleted', 'chrome.gcm.onSendError', 'chrome.instanceID.getID', 'chrome.instanceID.getCreationTime', 'chrome.instanceID.getToken', 'chrome.instanceID.deleteToken', 'chrome.instanceID.deleteID', 'chrome.instanceID.onTokenRefresh', 'navigator.geolocation.getCurrentPosition', 'navigator.geolocation.watchPosition', 'navigator.geolocation.clearWatch', 'chrome.hid.getDevices', 'chrome.hid.getUserSelectedDevices', 'chrome.hid.connect', 'chrome.hid.disconnect', 'chrome.hid.receive', 'chrome.hid.send', 'chrome.hid.receiveFeatureReport', 'chrome.hid.sendFeatureReport', 'chrome.hid.onDeviceAdded', 'chrome.hid.onDeviceRemoved', 'chrome.history.search', 'chrome.history.getVisits', 'chrome.history.addUrl', 'chrome.history.deleteUrl', 'chrome.history.deleteRange', 'chrome.history.deleteAll', 'chrome.history.onVisited', 'chrome.history.onVisitRemoved', 'chrome.identity.getAccounts', 'chrome.identity.getAuthToken', 'chrome.identity.getProfileUserInfo', 'chrome.identity.removeCachedAuthToken', 'chrome.identity.launchWebAuthFlow', 'chrome.identity.getRedirectURL', 'chrome.identity.onSignInChanged', 'chrome.idle.queryState', 'chrome.idle.setDetectionInterval', 'chrome.idle.getAutoLockDelay', 'chrome.idle.onStateChanged', 'chrome.input.ime.Methods', 'chrome.input.ime.setComposition', 'chrome.input.ime.clearComposition', 'chrome.input.ime.commitText', 'chrome.input.ime.sendKeyEvents', 'chrome.input.ime.hideInputView', 'chrome.input.ime.setCandidateWindowProperties', 'chrome.input.ime.setCandidates', 'chrome.input.ime.setCursorPosition', 'chrome.input.ime.setAssistiveWindowProperties', 'chrome.input.ime.setAssistiveWindowButtonHighlighted', 'chrome.input.ime.setMenuItems', 'chrome.input.ime.updateMenuItems', 'chrome.input.ime.deleteSurroundingText', 'chrome.input.ime.keyEventHandled', 'chrome.input.ime.onActivate', 'chrome.input.ime.onDeactivated', 'chrome.input.ime.onFocus', 'chrome.input.ime.onBlur', 'chrome.input.ime.onInputContextUpdate', 'chrome.input.ime.onKeyEvent', 'chrome.input.ime.onCandidateClicked', 'chrome.input.ime.onMenuItemActivated', 'chrome.input.ime.onSurroundingTextChanged', 'chrome.input.ime.onReset', 'chrome.input.ime.onAssistiveWindowButtonClicked', 'chrome.mdns.forceDiscovery', 'chrome.mdns.MAX_SERVICE_INSTANCES_PER_EVENT', 'chrome.mdns.onServiceList', 'chrome.mediaGalleries.getMediaFileSystems', 'chrome.mediaGalleries.addUserSelectedFolder', 'chrome.mediaGalleries.dropPermissionForMediaFileSystem', 'chrome.mediaGalleries.startMediaScan', 'chrome.mediaGalleries.cancelMediaScan', 'chrome.mediaGalleries.addScanResults', 'chrome.mediaGalleries.getMediaFileSystemMetadata', 'chrome.mediaGalleries.getAllMediaFileSystemMetadata', 'chrome.mediaGalleries.getMetadata', 'chrome.mediaGalleries.addGalleryWatch', 'chrome.mediaGalleries.removeGalleryWatch', 'chrome.mediaGalleries.getAllGalleryWatch', 'chrome.mediaGalleries.removeAllGalleryWatch', 'chrome.mediaGalleries.onGalleryChanged', 'chrome.mediaGalleries.onScanProgress', 'chrome.networking.onc.getProperties', 'chrome.networking.onc.getManagedProperties', 'chrome.networking.onc.getState', 'chrome.networking.onc.setProperties', 'chrome.networking.onc.createNetwork', 'chrome.networking.onc.forgetNetwork', 'chrome.networking.onc.getNetworks', 'chrome.networking.onc.getDeviceStates', 'chrome.networking.onc.enableNetworkType', 'chrome.networking.onc.disableNetworkType', 'chrome.networking.onc.requestNetworkScan', 'chrome.networking.onc.startConnect', 'chrome.networking.onc.startDisconnect', 'chrome.networking.onc.getCaptivePortalStatus', 'chrome.networking.onc.getGlobalPolicy', 'chrome.networking.onc.onNetworksChanged', 'chrome.networking.onc.onNetworkListChanged', 'chrome.networking.onc.onDeviceStateListChanged', 'chrome.networking.onc.onPortalDetectionCompleted', 'chrome.notifications.create', 'chrome.notifications.update', 'chrome.notifications.clear', 'chrome.notifications.getAll', 'chrome.notifications.getPermissionLevel', 'chrome.notifications.onClosed', 'chrome.notifications.onClicked', 'chrome.notifications.onButtonClicked', 'chrome.notifications.onPermissionLevelChanged', 'chrome.notifications.onShowSettings', 'chrome.pageCapture.saveAsMHTML', 'chrome.power.requestKeepAwake', 'chrome.power.releaseKeepAwake', 'chrome.printerProvider.onGetPrintersRequested', 'chrome.printerProvider.onGetUsbPrinterInfoRequested', 'chrome.printerProvider.onGetCapabilityRequested', 'chrome.printerProvider.onPrintRequested', 'chrome.privacy.network', 'chrome.privacy.services', 'chrome.privacy.websites', 'chrome.proxy.settings', 'chrome.proxy.onProxyError', 'chrome.serial.getDevices', 'chrome.serial.connect', 'chrome.serial.update', 'chrome.serial.disconnect', 'chrome.serial.setPaused', 'chrome.serial.getInfo', 'chrome.serial.getConnections', 'chrome.serial.send', 'chrome.serial.flush', 'chrome.serial.getControlSignals', 'chrome.serial.setControlSignals', 'chrome.serial.setBreak', 'chrome.serial.clearBreak', 'chrome.serial.onReceive', 'chrome.serial.onReceiveError', 'chrome.sessions.getRecentlyClosed', 'chrome.sessions.getDevices', 'chrome.sessions.restore', 'chrome.sessions.MAX_SESSION_RESULTS', 'chrome.sessions.onChanged', 'chrome.socket.create', 'chrome.socket.destroy', 'chrome.socket.connect', 'chrome.socket.bind', 'chrome.socket.disconnect', 'chrome.socket.read', 'chrome.socket.write', 'chrome.socket.recvFrom', 'chrome.socket.sendTo', 'chrome.socket.listen', 'chrome.socket.accept', 'chrome.socket.setKeepAlive', 'chrome.socket.setNoDelay', 'chrome.socket.getInfo', 'chrome.socket.getNetworkList', 'chrome.socket.joinGroup', 'chrome.socket.leaveGroup', 'chrome.socket.setMulticastTimeToLive', 'chrome.socket.setMulticastLoopbackMode', 'chrome.socket.getJoinedGroups', 'chrome.socket.secure', 'chrome.storage.sync', 'chrome.storage.sync.get','chrome.storage.sync.set','chrome.storage.local', 'chrome.storage.local.set', 'chrome.storage.local.get', 'chrome.storage.managed', 'chrome.storage.onChanged', 'chrome.syncFileSystem.requestFileSystem', 'chrome.syncFileSystem.setConflictResolutionPolicy', 'chrome.syncFileSystem.getConflictResolutionPolicy', 'chrome.syncFileSystem.getUsageAndQuota', 'chrome.syncFileSystem.getFileStatus', 'chrome.syncFileSystem.getFileStatuses', 'chrome.syncFileSystem.getServiceStatus', 'chrome.syncFileSystem.onServiceStatusChanged', 'chrome.syncFileSystem.onFileStatusChanged', 'chrome.system.cpu.getInfo', 'chrome.system.display.getInfo', 'chrome.system.display.getDisplayLayout', 'chrome.system.display.setDisplayProperties', 'chrome.system.display.setDisplayLayout', 'chrome.system.display.enableUnifiedDesktop', 'chrome.system.display.overscanCalibrationStart', 'chrome.system.display.overscanCalibrationAdjust', 'chrome.system.display.overscanCalibrationReset', 'chrome.system.display.overscanCalibrationComplete', 'chrome.system.display.showNativeTouchCalibration', 'chrome.system.display.startCustomTouchCalibration', 'chrome.system.display.completeCustomTouchCalibration', 'chrome.system.display.clearTouchCalibration', 'chrome.system.display.setMirrorMode', 'chrome.system.display.onDisplayChanged', 'chrome.system.memory.getInfo', 'chrome.system.network.getNetworkInterfaces', 'chrome.system.powerSource.getPowerSourceInfo', 'chrome.system.powerSource.requestStatusUpdate', 'chrome.system.powerSource.onPowerChanged', 'chrome.system.storage','chrome.system.storage.getInfo', 'chrome.system.storage.ejectDevice', 'chrome.system.storage.getAvailableCapacity', 'chrome.system.storage.onAttached', 'chrome.system.storage.onDetached', 'chrome.tabCapture.capture', 'chrome.tabCapture.getCapturedTabs', 'chrome.tabCapture.captureOffscreenTab', 'chrome.tabCapture.getMediaStreamId', 'chrome.tabCapture.onStatusChanged', 'chrome.topSites.get', 'chrome.tts.speak', 'chrome.tts.stop', 'chrome.tts.pause', 'chrome.tts.resume', 'chrome.tts.isSpeaking', 'chrome.tts.getVoices', 'chrome.ttsEngine.updateVoices', 'chrome.ttsEngine.onSpeak', 'chrome.ttsEngine.onStop', 'chrome.ttsEngine.onPause', 'chrome.ttsEngine.onResume', 'chrome.types.get', 'chrome.types.set', 'chrome.types.clear', 'chrome.types.onChange', 'chrome.usb.getDevices', 'chrome.usb.getUserSelectedDevices', 'chrome.usb.getConfigurations', 'chrome.usb.requestAccess', 'chrome.usb.openDevice', 'chrome.usb.findDevices', 'chrome.usb.closeDevice', 'chrome.usb.setConfiguration', 'chrome.usb.getConfiguration', 'chrome.usb.listInterfaces', 'chrome.usb.claimInterface', 'chrome.usb.releaseInterface', 'chrome.usb.setInterfaceAlternateSetting', 'chrome.usb.controlTransfer', 'chrome.usb.bulkTransfer', 'chrome.usb.interruptTransfer', 'chrome.usb.isochronousTransfer', 'chrome.usb.resetDevice', 'chrome.usb.onDeviceAdded', 'chrome.usb.onDeviceRemoved', 'chrome.virtualKeyboard.restrictFeatures', 'chrome.webNavigation.getFrame', 'chrome.webNavigation.getAllFrames', 'chrome.webNavigation.onBeforeNavigate', 'chrome.webNavigation.onCommitted', 'chrome.webNavigation.onDOMContentLoaded', 'chrome.webNavigation.onCompleted', 'chrome.webNavigation.onErrorOccurred', 'chrome.webNavigation.onCreatedNavigationTarget', 'chrome.webNavigation.onReferenceFragmentUpdated', 'chrome.webNavigation.onTabReplaced', 'chrome.webNavigation.onHistoryStateUpdated', 'chrome.webRequest.handlerBehaviorChanged', 'chrome.webRequest.MAX_HANDLER_BEHAVIOR_CHANGED_CALLS_PER_10_MINUTES', 'chrome.webRequest.onBeforeRequest', 'chrome.webRequest.onBeforeSendHeaders', 'chrome.webRequest.onSendHeaders', 'chrome.webRequest.onHeadersReceived', 'chrome.webRequest.onAuthRequired', 'chrome.webRequest.onResponseStarted', 'chrome.webRequest.onBeforeRedirect', 'chrome.webRequest.onCompleted', 'chrome.webRequest.onErrorOccurred', 'chrome.webRequest.onActionIgnored', 'chrome.accessibilityFeatures.spokenFeedback', 'chrome.accessibilityFeatures.largeCursor', 'chrome.accessibilityFeatures.stickyKeys', 'chrome.accessibilityFeatures.highContrast', 'chrome.accessibilityFeatures.screenMagnifier', 'chrome.accessibilityFeatures.autoclick', 'chrome.accessibilityFeatures.virtualKeyboard', 'chrome.accessibilityFeatures.caretHighlight', 'chrome.accessibilityFeatures.cursorHighlight', 'chrome.accessibilityFeatures.cursorColor', 'chrome.accessibilityFeatures.focusHighlight', 'chrome.accessibilityFeatures.selectToSpeak', 'chrome.accessibilityFeatures.switchAccess', 'chrome.accessibilityFeatures.animationPolicy', 'chrome.certificateProvider.requestPin', 'chrome.certificateProvider.stopPinRequest', 'chrome.certificateProvider.setCertificates', 'chrome.certificateProvider.reportSignature', 'chrome.certificateProvider.onCertificatesUpdateRequested', 'chrome.certificateProvider.onSignatureRequested', 'chrome.certificateProvider.onCertificatesRequested', 'chrome.certificateProvider.onSignDigestRequested', 'chrome.clipboard.setImageData', 'chrome.clipboard.onClipboardDataChanged', 'chrome.documentScan.scan', 'chrome.enterprise.deviceAttributes.getDirectoryDeviceId', 'chrome.enterprise.deviceAttributes.getDeviceSerialNumber', 'chrome.enterprise.deviceAttributes.getDeviceAssetId', 'chrome.enterprise.deviceAttributes.getDeviceAnnotatedLocation', 'chrome.enterprise.deviceAttributes.getDeviceHostname', 'chrome.enterprise.networkingAttributes.getNetworkDetails', 'chrome.enterprise.platformKeys.getTokens', 'chrome.enterprise.platformKeys.getCertificates', 'chrome.enterprise.platformKeys.importCertificate', 'chrome.enterprise.platformKeys.removeCertificate', 'chrome.enterprise.platformKeys.challengeMachineKey', 'chrome.enterprise.platformKeys.challengeUserKey', 'chrome.fileBrowserHandler.selectFile', 'chrome.fileBrowserHandler.onExecute', 'chrome.fileSystemProvider.mount', 'chrome.fileSystemProvider.unmount', 'chrome.fileSystemProvider.getAll', 'chrome.fileSystemProvider.get', 'chrome.fileSystemProvider.notify', 'chrome.fileSystemProvider.onUnmountRequested', 'chrome.fileSystemProvider.onGetMetadataRequested', 'chrome.fileSystemProvider.onGetActionsRequested', 'chrome.fileSystemProvider.onReadDirectoryRequested', 'chrome.fileSystemProvider.onOpenFileRequested', 'chrome.fileSystemProvider.onCloseFileRequested', 'chrome.fileSystemProvider.onReadFileRequested', 'chrome.fileSystemProvider.onCreateDirectoryRequested', 'chrome.fileSystemProvider.onDeleteEntryRequested', 'chrome.fileSystemProvider.onCreateFileRequested', 'chrome.fileSystemProvider.onCopyEntryRequested', 'chrome.fileSystemProvider.onMoveEntryRequested', 'chrome.fileSystemProvider.onTruncateRequested', 'chrome.fileSystemProvider.onWriteFileRequested', 'chrome.fileSystemProvider.onAbortRequested', 'chrome.fileSystemProvider.onConfigureRequested', 'chrome.fileSystemProvider.onMountRequested', 'chrome.fileSystemProvider.onAddWatcherRequested', 'chrome.fileSystemProvider.onRemoveWatcherRequested', 'chrome.fileSystemProvider.onExecuteActionRequested', 'chrome.loginState.getProfileType', 'chrome.loginState.getSessionState', 'chrome.loginState.onSessionStateChanged', 'chrome.networking.config.finishAuthentication', 'chrome.networking.config.setNetworkFilter', 'chrome.networking.config.onCaptivePortalDetected', 'chrome.platformKeys.selectClientCertificates', 'chrome.platformKeys.getKeyPair', 'chrome.platformKeys.getKeyPairBySpki', 'chrome.platformKeys.subtleCrypto', 'chrome.platformKeys.verifyTLSServerCertificate', 'chrome.printing.submitJob', 'chrome.printing.cancelJob', 'chrome.printing.getPrinters', 'chrome.printing.getPrinterInfo', 'chrome.printing.MAX_SUBMIT_JOB_CALLS_PER_MINUTE', 'chrome.printing.MAX_GET_PRINTER_INFO_CALLS_PER_MINUTE', 'chrome.printing.onJobStatusChanged', 'chrome.printingMetrics.getPrintJobs ', 'chrome.printingMetrics.onPrintJobFinished', 'chrome.vpnProvider.createConfig', 'chrome.vpnProvider.destroyConfig', 'chrome.vpnProvider.setParameters', 'chrome.vpnProvider.sendPacket', 'chrome.vpnProvider.notifyConnectionStateChanged', 'chrome.vpnProvider.onPlatformMessage', 'chrome.vpnProvider.onPacketReceived', 'chrome.vpnProvider.onConfigRemoved', 'chrome.vpnProvider.onConfigCreated', 'chrome.vpnProvider.onUIEvent', 'chrome.wallpaper.setWallpaper', 'chrome.enterprise.hardwarePlatform.getHardwarePlatformInfo', 'chrome.declarativeWebRequest.onRequest', 'chrome.declarativeWebRequest.onMessage', 'chrome.processes.getProcessIdForTab', 'chrome.processes.terminate', 'chrome.processes.getProcessInfo', 'chrome.processes.onUpdated', 'chrome.processes.onUpdatedWithMemory', 'chrome.processes.onCreated', 'chrome.processes.onUnresponsive', 'chrome.processes.onExited', 'chrome.signedInDevices.get', 'chrome.signedInDevices.onDeviceInfoChange', 'chrome.activityLogPrivate.getExtensionActivities', 'chrome.activityLogPrivate.deleteActivities', 'chrome.activityLogPrivate.deleteActivitiesByExtension', 'chrome.activityLogPrivate.deleteDatabase', 'chrome.activityLogPrivate.deleteUrls', 'chrome.activityLogPrivate.onExtensionActivity', 'chrome.brailleDisplayPrivate.getDisplayState', 'chrome.brailleDisplayPrivate.writeDots', 'chrome.brailleDisplayPrivate.updateBluetoothBrailleDisplayAddress', 'chrome.brailleDisplayPrivate.onDisplayStateChanged', 'chrome.brailleDisplayPrivate.onKeyEvent', 'chrome.commandLinePrivate.hasSwitch', 'chrome.developerPrivate.autoUpdate', 'chrome.developerPrivate.getExtensionsInfo', 'chrome.developerPrivate.getExtensionInfo', 'chrome.developerPrivate.getExtensionSize', 'chrome.developerPrivate.getItemsInfo', 'chrome.developerPrivate.getProfileConfiguration', 'chrome.developerPrivate.updateProfileConfiguration', 'chrome.developerPrivate.showPermissionsDialog', 'chrome.developerPrivate.reload', 'chrome.developerPrivate.updateExtensionConfiguration', 'chrome.developerPrivate.loadUnpacked', 'chrome.developerPrivate.installDroppedFile', 'chrome.developerPrivate.notifyDragInstallInProgress', 'chrome.developerPrivate.loadDirectory', 'chrome.developerPrivate.choosePath', 'chrome.developerPrivate.packDirectory', 'chrome.developerPrivate.isProfileManaged', 'chrome.developerPrivate.requestFileSource', 'chrome.developerPrivate.openDevTools', 'chrome.developerPrivate.deleteExtensionErrors', 'chrome.developerPrivate.repairExtension', 'chrome.developerPrivate.showOptions', 'chrome.developerPrivate.showPath', 'chrome.developerPrivate.setShortcutHandlingSuspended', 'chrome.developerPrivate.updateExtensionCommand', 'chrome.developerPrivate.addHostPermission', 'chrome.developerPrivate.removeHostPermission', 'chrome.developerPrivate.enable', 'chrome.developerPrivate.allowIncognito', 'chrome.developerPrivate.allowFileAccess', 'chrome.developerPrivate.inspect', 'chrome.developerPrivate.onItemStateChanged', 'chrome.developerPrivate.onProfileStateChanged', 'chrome.feedbackPrivate.getUserEmail', 'chrome.feedbackPrivate.getSystemInformation', 'chrome.feedbackPrivate.sendFeedback', 'chrome.feedbackPrivate.getStrings', 'chrome.feedbackPrivate.readLogSource', 'chrome.feedbackPrivate.loginFeedbackComplete', 'chrome.feedbackPrivate.onFeedbackRequested', 'chrome.networkingPrivate.getProperties', 'chrome.networkingPrivate.getManagedProperties', 'chrome.networkingPrivate.getState', 'chrome.networkingPrivate.setProperties', 'chrome.networkingPrivate.createNetwork', 'chrome.networkingPrivate.forgetNetwork', 'chrome.networkingPrivate.getNetworks', 'chrome.networkingPrivate.getVisibleNetworks', 'chrome.networkingPrivate.getEnabledNetworkTypes', 'chrome.networkingPrivate.getDeviceStates', 'chrome.networkingPrivate.enableNetworkType', 'chrome.networkingPrivate.disableNetworkType', 'chrome.networkingPrivate.requestNetworkScan', 'chrome.networkingPrivate.startConnect', 'chrome.networkingPrivate.startDisconnect', 'chrome.networkingPrivate.startActivate', 'chrome.networkingPrivate.getCaptivePortalStatus', 'chrome.networkingPrivate.unlockCellularSim', 'chrome.networkingPrivate.setCellularSimState', 'chrome.networkingPrivate.selectCellularMobileNetwork', 'chrome.networkingPrivate.getGlobalPolicy', 'chrome.networkingPrivate.getCertificateLists', 'chrome.networkingPrivate.onNetworksChanged', 'chrome.networkingPrivate.onNetworkListChanged', 'chrome.networkingPrivate.onDeviceStateListChanged', 'chrome.networkingPrivate.onPortalDetectionCompleted', 'chrome.networkingPrivate.onCertificateListsChanged', 'chrome.runtime.sendNativeMessage', 'chrome.runtime.connectNative']
NO_PERMISSIONS_NEEDED = ['chrome.devtools.inspectedWindow.eval', 'chrome.devtools.inspectedWindow.reload', 'chrome.devtools.inspectedWindow.getResources', 'chrome.devtools.inspectedWindow.tabId', 'chrome.devtools.inspectedWindow.onResourceAdded', 'chrome.devtools.inspectedWindow.onResourceContentCommitted', 'chrome.devtools.network.getHAR', 'chrome.devtools.network.onRequestFinished', 'chrome.devtools.network.onNavigated', 'chrome.devtools.panels.create', 'chrome.devtools.panels.setOpenResourceHandler', 'chrome.devtools.panels.openResource', 'chrome.devtools.panels.elements', 'chrome.devtools.panels.sources', 'chrome.devtools.panels.themeName', 'chrome.extension.sendRequest', 'chrome.extension.getURL', 'chrome.extension.getViews', 'chrome.extension.getBackgroundPage', 'chrome.extension.getExtensionTabs', 'chrome.extension.isAllowedIncognitoAccess', 'chrome.extension.isAllowedFileSchemeAccess', 'chrome.extension.setUpdateUrlData', 'chrome.extension.lastError', 'chrome.extension.inIncognitoContext', 'chrome.extension.onRequest', 'chrome.extension.onRequestExternal', 'chrome.management.getSelf', 'chrome.management.uninstallSelf', 'chrome.management.getPermissionWarningsByManifest', 'chrome.permissions.getAll', 'chrome.permissions.contains', 'chrome.permissions.request', 'chrome.permissions.remove', 'chrome.permissions.onAdded', 'chrome.permissions.onRemoved', 'chrome.runtime.getBackgroundPage', 'chrome.runtime.openOptionsPage', 'chrome.runtime.getManifest', 'chrome.runtime.getURL', 'chrome.runtime.setUninstallURL', 'chrome.runtime.reload', 'chrome.runtime.requestUpdateCheck', 'chrome.runtime.restart', 'chrome.runtime.restartAfterDelay', 'chrome.runtime.connect', 'chrome.runtime.sendMessage', 'chrome.runtime.getPlatformInfo', 'chrome.runtime.getPackageDirectoryEntry', 'chrome.runtime.lastError', 'chrome.runtime.id', 'chrome.runtime.onStartup', 'chrome.runtime.onInstalled', 'chrome.runtime.onSuspend', 'chrome.runtime.onSuspendCanceled', 'chrome.runtime.onUpdateAvailable', 'chrome.runtime.onBrowserUpdateAvailable', 'chrome.runtime.onConnect', 'chrome.runtime.onConnectExternal', 'chrome.runtime.onConnectNative', 'chrome.runtime.onMessage', 'chrome.runtime.onMessageExternal', 'chrome.runtime.onRestartRequired', 'chrome.tabs.get', 'chrome.tabs.getCurrent', 'chrome.tabs.connect', 'chrome.tabs.sendRequest', 'chrome.tabs.sendMessage', 'chrome.tabs.getSelected', 'chrome.tabs.getAllInWindow', 'chrome.tabs.create', 'chrome.tabs.duplicate', 'chrome.tabs.query', 'chrome.tabs.highlight', 'chrome.tabs.update', 'chrome.tabs.move', 'chrome.tabs.reload', 'chrome.tabs.remove', 'chrome.tabs.detectLanguage', 'chrome.tabs.captureVisibleTab', 'chrome.tabs.executeScript', 'chrome.tabs.insertCSS', 'chrome.tabs.setZoom', 'chrome.tabs.getZoom', 'chrome.tabs.setZoomSettings', 'chrome.tabs.getZoomSettings', 'chrome.tabs.discard', 'chrome.tabs.goForward', 'chrome.tabs.goBack', 'chrome.tabs.TAB_ID_NONE', 'chrome.tabs.url', 'chrome.tabs.pendingUrl', 'chrome.tabs.title', 'chrome.tabs.favIconUrl', 'chrome.tabs.onCreated', 'chrome.tabs.onUpdated', 'chrome.tabs.onMoved', 'chrome.tabs.onSelectionChanged', 'chrome.tabs.onActiveChanged', 'chrome.tabs.onActivated', 'chrome.tabs.onHighlightChanged', 'chrome.tabs.onHighlighted', 'chrome.tabs.onDetached', 'chrome.tabs.onAttached', 'chrome.tabs.onRemoved', 'chrome.tabs.onReplaced', 'chrome.tabs.onZoomChange', 'chrome.windows.get', 'chrome.windows.getCurrent', 'chrome.windows.getLastFocused', 'chrome.windows.getAll', 'chrome.windows.create', 'chrome.windows.update', 'chrome.windows.remove', 'chrome.windows.WINDOW_ID_NONE', 'chrome.windows.WINDOW_ID_CURRENT', 'chrome.windows.onCreated', 'chrome.windows.onRemoved', 'chrome.windows.onFocusChanged', 'chrome.windows.onBoundsChanged', 'chrome.app.runtime.onEmbedRequested', 'chrome.app.runtime.onLaunched', 'chrome.app.runtime.onRestarted', 'chrome.app.window.create', 'chrome.app.window.current', 'chrome.app.window.getAll', 'chrome.app.window.get', 'chrome.app.window.canSetVisibleOnAllWorkspaces', 'chrome.app.window.onBoundsChanged', 'chrome.app.window.onClosed', 'chrome.app.window.onFullscreened', 'chrome.app.window.onMaximized', 'chrome.app.window.onMinimized', 'chrome.app.window.onRestored']
API_PERMISSIONS = ['chrome.alarms', 'chrome.app.runtime', 'chrome.app.window', 'chrome.audio', 'chrome.bookmarks', 'chrome.browser', 'chrome.browsingData', 'document', 'document', 'chrome.contextMenus', 'chrome.contentSettings', 'chrome.cookies', 'chrome.debugger', 'chrome.declarativeContent', 'chrome.declarativeNetRequest', 'chrome.desktopCapture', 'chrome.devtools.inspectedWindow', 'chrome.devtools.network', 'chrome.devtools.panels', 'chrome.downloads', 'chrome.events', 'chrome.extension', 'chrome.extensionTypes', 'chrome.fileSystem', 'chrome.fontSettings', 'chrome.gcm', 'chrome.instanceID', 'navigator.geolocation', 'chrome.hid', 'chrome.history', 'chrome.identity', 'chrome.idle', 'chrome.input.ime', 'chrome.management', 'chrome.mdns', 'chrome.mediaGalleries', 'chrome.networking.onc', 'chrome.notifications', 'chrome.pageCapture', 'chrome.permissions', 'chrome.power', 'chrome.printerProvider', 'chrome.privacy', 'chrome.proxy', 'chrome.runtime', 'chrome.serial', 'chrome.sessions', 'chrome.socket', 'chrome.storage', 'chrome.syncFileSystem', 'chrome.system.cpu', 'chrome.system.display', 'chrome.system.memory', 'chrome.system.network', 'chrome.system.powerSource', 'chrome.system.storage', 'chrome.tabCapture', 'chrome.tabs', 'chrome.topSites', 'chrome.tts', 'chrome.ttsEngine', 'chrome.types', 'chrome.usb', 'chrome.virtualKeyboard', 'chrome.webNavigation', 'chrome.webRequest', 'chrome.windows', 'chrome.accessibilityFeatures', 'chrome.certificateProvider', 'chrome.clipboard', 'chrome.documentScan', 'chrome.enterprise.deviceAttributes', 'chrome.enterprise.networkingAttributes', 'chrome.enterprise.platformKeys', 'chrome.fileBrowserHandler', 'chrome.fileSystemProvider', 'chrome.loginState', 'chrome.networking.config', 'chrome.platformKeys', 'chrome.printing', 'chrome.printingMetrics', 'chrome.vpnProvider', 'chrome.wallpaper', 'chrome.enterprise.hardwarePlatform', 'chrome.declarativeWebRequest', 'chrome.processes', 'chrome.signedInDevices', 'chrome.experimental', 'chrome.activityLogPrivate', 'chrome.brailleDisplayPrivate', 'chrome.commandLinePrivate', 'chrome.developerPrivate', 'chrome.feedbackPrivate', 'chrome.networkingPrivate']
PRIVACY_regex = r'chrome\.privacy\.(services|websites)\.'
NO_NEED_PERMISSIONS_regex = r'chrome\.(app|benchmarking|bluetoothLowEnergy|bluetoothSocket|\bbrowser\b|browserAction|cast|' \
                            r'commands|copresence|manifest|options|views|devtools|document|extension|i18n|omnibox|pageAction|permissions|' \
                            r'runtime|scriptBadge|localStorage|elementsTools|menus|experimental|systemPrivate|_tabInfo|' \
                            r'webstore|sidebar|ports)'
NOT_PERMISSIONS_BUT_KEYS = ['chrome.commands.onCommand', 'chrome.omnibox.onInputEntered', 'chrome.browserAction.onClicked',
                            'chrome.omnibox.onInputChanged', 'chrome.pageAction.onClicked', 'chrome.browserAction.setTitle',
                            'chrome.browserAction.setBadgeText', 'chrome.browserAction.setBadgeBackgroundColor',
                            'chrome.browserAction.setIcon', 'chrome.browserAction.setPopup', 'chrome.browserAction.getBadgeText',
                            'chrome.commands.getAll','chrome.pageAction.show', 'chrome.sockets.udp', 'chrome.sockets.tcp',
                            'chrome.sockets.tcpServer', 'chrome.socketsfunctionWebApplication', 'chrome.bluetoothLowEnergy.unregisterService',
                            'chrome.pageAction.setPopup', 'chrome.pageAction.setTitle', 'chrome.pageAction.setIcon',
                            'chrome.browserAction.disable', 'chrome.browserAction.enable', 'chrome.omnibox.onInputStarted',
                            'chrome.omnibox.onInputCancelled','chrome.omnibox.setDefaultSuggestion', 'chrome.pageAction.hide',
                            'chrome.browserAction.getPopup', 'chrome.scriptBadge.setPopup', 'chrome.pageAction.getTitle',
                            'chrome.pageAction.getPopup', 'chrome.scriptBadge.getAttention', 'chrome.omnibox.sendSuggestions',
                            ]
DEVELOPER_regex = r'chrome\.(developerPrivate)\..+?'
ACCESIBILITY = ['chrome.accessibilityFeatures.spokenFeedback', 'chrome.accessibilityFeatures.largeCursor',
'chrome.accessibilityFeatures.stickyKeys', 'chrome.accessibilityFeatures.highContrast',
'chrome.accessibilityFeatures.screenMagnifier', 'chrome.accessibilityFeatures.autoclick',
'chrome.accessibilityFeatures.virtualKeyboard', 'chrome.accessibilityFeatures.caretHighlight',
'chrome.accessibilityFeatures.cursorHighlight', 'chrome.accessibilityFeatures.focusHighlight',
'chrome.accessibilityFeatures.selectToSpeak', 'chrome.accessibilityFeatures.switchAccess',
'chrome.accessibilityFeatures.animationPolicy']
WEBVIEW_regex = r'chrome\.(webviewTag|webview|webViewRequest)\..+?'
NFC_regex = r'chrome\.nfc\..+?'
FILEBROWSERHANDLER = ['chrome.fileBrowserHandlerInternal.selectFile']

TMP_DIR = 'tmp'

def unzipExtension(extension, extension_path, dirpath=""):
    try:
        unpack(dirpath + '/' + extension + '.crx')
    except:
        try:
            zip_ref = zipfile.ZipFile(extension_path, 'r')
            zip_ref.extractall(dirpath + '/' + extension)
            zip_ref.close()
        except:
            print("[+] Error in {}: {}".format(extension_path, 'OK'))
    finally:
        path = dirpath + '/' + extension

    return dirpath, path

def static_analysis(path):
    total_apis = []
    output = {}
    is_eval = False
    
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('.js') or filename.endswith('.html') or filename.endswith('.html'):
                output[filename] = []
                esprima_token = False
                try:
                    with open(dirpath + os.sep + filename, encoding='utf-8', errors='ignore') as dataFile:
                        data = dataFile.read()
                    
                    if filename.endswith('.html') or filename.endswith('.htm'):
                        webview = re.findall('(?si)<webview (.*?)</webview>', data)
                        geolocation = re.findall(r"navigator\.geolocation\.(.*?)\(", data)
                        clipboard = re.findall(
                            r"(?si)document\.[execCommand|clipboard\.readText|clipboard.writeText|clipboard\.read|clipboard\.write]\((.+?)\)",
                            data)
                        chrome_api = re.findall(r"chrome\.(.*?)\(", data)
                        
                        if geolocation:
                            if ("navigator.geolocation.getCurrentPosition" in data):
                                output[filename].append("navigator.geolocation.getCurrentPosition")
                            elif ("navigator.geolocation.watchPosition" in data):
                                output[filename].append("navigator.geolocation.watchPosition")
                            elif ("navigator.geolocation.clearWatch" in data):
                                output[filename].append("navigator.geolocation.clearWatch")
                        
                        if chrome_api:
                            for aux in chrome_api:
                                aux = "chrome.{}".format(aux)
                                
                                if aux.endswith(".addListener"):
                                    aux = aux.split(".addListener")[0]
                                if (aux in PERMISSIONS_NEEDED) or (aux in NO_PERMISSIONS_NEEDED) or (
                                        aux in API_PERMISSIONS):
                                    output[filename].append(aux)
                                else:
                                    aux = ".".join(aux.split(".")[:-1])
                                    if (aux in PERMISSIONS_NEEDED) or (aux in NO_PERMISSIONS_NEEDED) or (
                                            aux in API_PERMISSIONS):
                                        output[filename].append(aux)
                        
                        data = "\n".join(re.findall('(?si)<script>(.*?)</script>', data))
                        
                        if clipboard:
                            if "paste" in clipboard:
                                output[filename].append("document.execCommand('paste')")
                            elif "cut" in clipboard:
                                output[filename].append("document.execCommand('cut')")
                            elif "copy" in clipboard:
                                output[filename].append("document.execCommand('copy')")
                            elif "readText" in clipboard:
                                output[filename].append("document.clipboard.readText")
                            elif "writeText" in clipboard:
                                output[filename].append("document.clipboard.writeText")
                        
                        if webview:
                            output[filename].append("webview")
                    
                    esprima_token = esprima.tokenize(data)
                
                except Exception as e:
                    data = data.split("function")
                    final_data = ""
                    for chunk in data:
                        try:
                            esprima_token = esprima.tokenize(chunk)
                            final_data += chunk + "\n"
                        except:
                            pass
                
                if esprima_token:
                    for ind, elem in enumerate(esprima_token):
                        
                        if elem.value == "chrome":
                            cont = 1
                            api_call = "chrome"
                            if ((ind + cont) < len(esprima_token)):
                                while (esprima_token[ind + cont].value == '.'):
                                    api_call += "{}{}".format(esprima_token[ind + cont].value,
                                                              esprima_token[ind + cont + 1].value)
                                    if ((ind + cont + 2) < len(esprima_token)):
                                        cont += 2
                                    else:
                                        break
                            
                            if api_call.endswith(".addListener"):
                                api_call = api_call.split(".addListener")[0]
                            if (api_call in PERMISSIONS_NEEDED) or (api_call in NO_PERMISSIONS_NEEDED) or (
                                    api_call in API_PERMISSIONS):
                                output[filename].append(api_call)
                            else:
                                api_call = ".".join(api_call.split(".")[:-1])
                                if (api_call in PERMISSIONS_NEEDED) or (api_call in NO_PERMISSIONS_NEEDED) or (
                                        api_call in API_PERMISSIONS):
                                    output[filename].append(api_call)
                                else:
                                    if re.findall(PRIVACY_regex, api_call):
                                        output[filename].append('chrome.privacy.services')
                                    else:
                                        aux_r = re.findall(NO_NEED_PERMISSIONS_regex, api_call)
                                        if (not aux_r) and (api_call != 'chrome') and (api_call):
                                            print(api_call)
                        
                        elif (elem.value == 'geolocation'):
                            if ("navigator.geolocation.getCurrentPosition" in data):
                                output[filename].append("navigator.geolocation.getCurrentPosition")
                            elif ("navigator.geolocation.watchPosition" in data):
                                output[filename].append("navigator.geolocation.watchPosition")
                            elif ("navigator.geolocation.clearWatch" in data):
                                output[filename].append("navigator.geolocation.clearWatch")
                        
                        elif (elem.value == 'clipboard'):
                            if (esprima_token[ind - 1].value == ".") and (esprima_token[ind + 1].value == ".") and (
                                    esprima_token[ind + 2].value in ["readText", "read", "writeText", "write"]):
                                # print('{}clipboard (JS): {}'.format(Fore.MAGENTA, Fore.RESET))
                                cad = esprima_token[ind - 2].value + esprima_token[ind - 1].value + esprima_token[
                                    ind].value + esprima_token[ind + 1].value + esprima_token[ind + 2].value
                                output[filename].append(cad)
                        
                        elif not is_eval:
                            if (esprima_token[ind].value in ["eval(", "Function(", "write(",
                                                             "setTimeout("]) and not is_eval:
                                is_eval = True
                            if (esprima_token[ind].value == "write") and (esprima_token[ind - 1].value == ".") and (
                                    esprima_token[ind - 2].value == "document"):
                                is_eval = True
                
                if len(output[filename]) == 0:
                    del (output[filename])
            
            if filename in output.keys():
                output[filename] = list(set(output[filename]))
                total_apis.append(output[filename])
    
    return output, list(set([item for sublist in total_apis for item in sublist]))

def load_manifest(path):
    for dirpath, dirnames, filenames in os.walk(path):
        if 'manifest.json' in filenames:
            input_file = os.path.join(path, 'manifest.json')
            input_file2 = codecs.decode(open(input_file).read().encode(), 'utf-8-sig')
            manifest = json.loads(input_file2)
            return manifest
    return False

def get_permissions(dirpath):
    manifest = load_manifest(dirpath)
    if 'permissions' not in manifest.keys():
        manifest['permissions'] = []
    if 'optional_permissions' not in manifest.keys():
        manifest['optional_permissions'] = []
    return manifest['permissions'] + manifest['optional_permissions']

def staticAnalysis(extensionFileName):
    output = {}
    extension = extensionFileName.split('.zip')[0]
    extension_tmp_path = os.path.join(TMP_DIR, extension)
    
    if not os.path.isdir(extension_tmp_path):
        os.mkdir(extension_tmp_path)
    
    dirpath, path = unzipExtension(extension, extensionFileName, extension_tmp_path)
    
    aux, total_apis = static_analysis(path)
    output[extension] = aux
    
    permissions = get_permissions(path)
    
    shutil.rmtree(dirpath)
    
    return output, permissions, total_apis

def clean_permissions(permissions):
    to_exclude = set(['*', 'http', 'https', 'chrome://favicon/'])
    
    if permissions:
        to_delete = []
        for elem in permissions:
            if elem:
                for elem_exclude in to_exclude:
                    if elem_exclude in elem:
                        to_delete.append(elem)
            else:
                to_delete.append(elem)
        
        cleaned_permissions = list(set(permissions).difference(to_delete))
        if cleaned_permissions:
            if (("unlimitedStorage" in cleaned_permissions) or (
                    "unlimited_storage" in cleaned_permissions)) and ("storage" not in cleaned_permissions):
                print("Overprivileged: storage")
                return False
            
            if (("downloads.open" in cleaned_permissions) or (
                    "downloads.shelf" in cleaned_permissions)) and ("downloads" not in cleaned_permissions):
                print("Overprivileged: downloads")
                return False
        
        if to_delete:
            if len(to_delete) > 1:
                cleaned_permissions.append("host_permissions")
            elif 'chrome://favicon/' not in to_delete:
                cleaned_permissions.append("host_permissions")
        
        if ("webRequestBlocking" in cleaned_permissions) and ("webRequest" not in cleaned_permissions) and (
                ("host_permissions" not in cleaned_permissions) or (
                "<all_urls>" not in cleaned_permissions)):
            print("Overprivileged: webRequestBlocking OR webRequest without {<all_urls>, host_permissions}")
            return False
        
        return cleaned_permissions

def is_API_used(call, permissions_bbdd, permissions_dict):
    if call == "webview":
        return "webview" if "webview" in permissions_bbdd else False
    
    if call in ["navigator.geolocation.getCurrentPosition", "navigator.geolocation.watchPosition",
                "navigator.geolocation.clearWatch"]:
        return "geolocation" if "geolocation" in permissions_bbdd else False
    
    if call == "navigator.clipboard.readText":
        return "clipboardRead" if "clipboardRead" in permissions_bbdd else False
    
    if call == "navigator.clipboard.writeText":
        return "clipboardWrite" if "clipboardWrite" in permissions_bbdd else False
    
    api = call.split("chrome.")[1]
    
    if (api in ['tabs.title', 'tabs.favIconUrl']) or (api.split(".")[0] == "webRequest"):
        if 'activeTab' in permissions_bbdd:
            return 'activeTab'
    
    if api in ["runtime.sendNativeMessage", "runtime.connectNative"]:
        return 'nativeMessaging' if "nativeMessaging" in permissions_bbdd else False
    
    if api.split(".")[0] == "webRequest":
        if ('<all_urls>' in permissions_bbdd) or ('host_permissions' in permissions_bbdd) or (
                'activeTab' in permissions_bbdd) or ('webRequest' in permissions_bbdd):
            return api.split(".")[0]
        else:
            return False
    
    permissions_aux = permissions_dict.keys()
    
    if api in permissions_aux:
        return api
    if api.split(".")[0] in permissions_aux:
        return api.split(".")[0]
    if ".".join(api.split(".")[:-1]) in permissions_aux:
        return ".".join(api.split(".")[:-1])
    if api == 'tabs.captureVisibleTab':
        if '<all_urls>' in permissions_bbdd:
            return '<all_urls>'
        if 'activeTab' in permissions_aux:
            return 'activeTab'
    if 'serialDevice' in api and 'serial' in permissions_aux:
        return 'serial'
    if 'instanceID' in api and 'gcm' in permissions_aux:
        return 'gcm'
    if call in ACCESIBILITY and 'accessibilityFeatures.read' in permissions_aux:
        return 'accessibilityFeatures.read'
    if re.findall(DEVELOPER_regex, call):
        if 'developerPrivate' in permissions_aux:
            return 'developerPrivate'
        if 'management' in permissions_aux:
            return 'management'
    if re.findall(WEBVIEW_regex, call) and 'webview' in permissions_aux:
        return 'webview'
    if "chrome." + api in FILEBROWSERHANDLER and 'fileBrowserHandler' in permissions_aux:
        return 'fileBrowserHandler'
    if re.findall(NFC_regex, call) and 'usb' in permissions_aux:
        return 'usb'
    if api == 'onButtonClicked.onClicked' and 'notifications' in permissions_aux:
        return 'notifications'
    
    return False

def overprivileged(total_apis, permissions):
    
    api_calls = list(set(total_apis).difference(set(NO_PERMISSIONS_NEEDED)).difference(set(NOT_PERMISSIONS_BUT_KEYS)))
    
    if api_calls:
        per_dict = {}
        for permission in permissions:
            if permission not in ['host_permissions', '<all_urls>', 'background', 'windows']:
                try:
                    permission = list(json.loads(permission).keys())[0]
                except:
                    pass
                if permission in ["unlimitedStorage", 'unlimited_storage']:
                    per_dict[permission] = 'storage' in permissions
                else:
                    per_dict[permission] = False
        
        # check api_calls and permissions
        for call in api_calls:
            if call in list(set(NO_PERMISSIONS_NEEDED).union(set(PERMISSIONS_NEEDED)).union(set(API_PERMISSIONS))):
                per_aux = is_API_used(call, permissions, per_dict)
                if per_aux:
                    per_dict[per_aux] = True
        
        aux2 = all(value == True for value in per_dict.values())
        if aux2:
            print('Not Overprivileged!')
            return False
        else:
            unused_permissions = []
            for key in per_dict.keys():
                if not per_dict[key]:
                    unused_permissions.append(key)
            print('\nOverprivileged!')
            print('Permissions used (true) and not used (false): {}'.format(json.dumps(per_dict)))
            return True
    else:
        unused_permissions = []
        for key in permissions:
            if key not in ['host_permissions', '<all_urls>', 'background', 'windows']:
                unused_permissions.append(key)
        
        if len(unused_permissions) == 0:
            print('Not Overprivileged!')
            return False
        else:
            print('Overprivileged!')
            return True

def underprivileged(total_apis, permissions):
    api_calls = list(set(total_apis).difference(set(NO_PERMISSIONS_NEEDED)))
    
    if api_calls:
        per_dict = {}
        for permission in permissions:
            try:
                permission = list(json.loads(permission).keys())[0]
            except:
                pass
            per_dict[permission] = False
        
        for call in api_calls:
            if "geolocation" in call:
                call = "navigator.geolocation.getCurrentPosition"
            if call == "webview" and call in per_dict.keys():
                per_dict[call] = True
            
            if call in list(set(NO_PERMISSIONS_NEEDED).union(set(PERMISSIONS_NEEDED)).union(set(API_PERMISSIONS)).union(set(API_PERMISSIONS))):
                if not is_API_used(call, permissions, per_dict):
                    print('\nUnderprivileged!')
                    return
                
    print('\nNot underprivileged!')

    


if __name__ == "__main__":
    extensionFileName = 'inpcombdapfeodjmffokhkingnblebdh.zip'
    
    apis, permissions, total_apis = staticAnalysis(extensionFileName)
    cleaned = clean_permissions(permissions)
    print('Permissions: {}'.format(cleaned))
    print('API calls detected: {}'.format(total_apis))
    
    if cleaned:
        if total_apis:
            overprivileged(total_apis, cleaned)
        else:
            print('\nOverprivileged!\n Not APIs found')
    else:
        print('Not overprivileged!')
    
    underprivileged(total_apis, cleaned)