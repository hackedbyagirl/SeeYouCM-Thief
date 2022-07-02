# Additional CUCM Scripts
Additional Scripts that can be of use when you find CUCM and Cisco Phones. Hopefully will be integrated in the future.

Scripts:
- Manual user enumeration if original doesnt work
- Retrieving Config files from CUCM server

## Files
Note: Could be port 6970 or 6972
```
Service Profile
- https://{CUCM}:6972/SPDefault.cnf.xml
- https://{CUCM}:6972/global-settings.xml
- https://{CUCM}:6972/homeClusterUser.xml
- https://{CUCM}:6972/CSF{username}.cnf.xml

Filesnames:
- SEPDefault.cnf
- MTPDefault.cnf
- CFBDefault.cnf
- SAADefault.cnf
- SDADefault.cnf
- lddefault.cfg
- gkdefault.cfg
- SIPDefault.cnf
- XMLDefault.cnf.xml.sgn
- AppDialRules.xml
- DirLookupDialRules.xml
- global-settings.xml.sgn

```
