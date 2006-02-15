Leo 4.4 experimental 1                                      February 15, 2006

My apologies for the key handling problems in Leo 4.4 b2.

This version is an emergency measure.  It's goals:

1.  To fix some of the key-handling issues in Leo 4.4 b2.
2.  To allow further experimentation with key handling.
3.  To allow easy reporting of any other key handling problems.

Please do not use this version (or Leo 4.4b2) unless you are ready to report bugs.

Here are the details of the key-handling changes:

- Added support for trace_key_event setting.
- Added support for ignore_caps_lock setting.
- Added Caps_Lock and Num_Lock to k.tkNamesList and in the list of
  special keys in k.masterCommand and k.masterKeyHandlerHelper.
- Added support for k.ignore_unbound_non_ascii_keys logic in masterKeyHandlerHelper.
- Disabled unknown keysym trace in k.strokeFromEvent.
- Enabled the international keyboard on XP as an aid to testing.
- Added support for swap_mac_keys setting in k.shortcutFromSetting.
- Added support for non-ascii characters in the minibuffer.