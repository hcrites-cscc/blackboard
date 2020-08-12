# System Admin Panel Hacks
We have some support departments that need to have full Z admin access due to bugs in the Content Collection. We do not wish for these support departments to be able to access the majority of functions under the System Admin panel and in other administrative areas.  These hacks hide or block those functions.

We also have a support department with a custom system role, but there are 

## Limit Admin Access - Sys Admin tab (admin_remove_sys_adm.1.0.zip)
This hack hides whole modules and hides individual links.

### Customizations
To hide whole modules, you need the ID attribute for the module (which is often its pk1 value if you have database access). You can find this on the System Admin tab by looking at the source code for the module.  Each module is a <div> tag whose ID follows the pattern "module:_1690_1".  Update the code to target the modules you wish to hide.

To hide individual links, you need the ID attribute for the link. Again, you can view the source on the page to find the ID attribute.  If the link does not have an ID attribute, then you may need to get creative to target the link.

The last component of this hack is labeled as "// Add Disk Usage" - in this case, we are adding a link to the Disk Usage Report - which is normally nested under System Reporting - up on the Tools panel. This is one way to allow access to a nested function while blocking the parent link from the System Admin tab.

To target a specific institution role, update [institution_role] under the Restriction List.

## Limit ITSC Admin Access - Sys Admin tab (admin_remove_itsc.1.0.zip)
Our IT Support crew has a custom system role, but some tools still appear for them (e.g. Ally, Goals).  This hack removes those extraneous links.

### Customization
To hide individual links, you need the ID attribute for the link. Again, you can view the source on the page to find the ID attribute.  If the link does not have an ID attribute, then you may need to get creative to target the link.

To target a specific system role, update [system_role] under the Restriction List.

## Limit Admin Access - Users (admin_remove_users.1.0.zip)
This hack hides the ability for a specific institution role to create or delete users.

### Customizations
To target a specific institution role, update [institution_role] under the Restriction List.

## Limit Admin Access - System roles (admin_remove_sys_rol.1.0.zip)
This hack hides the ability for a specific institution role to modify the system roles of any user.  This prevents someone from making someone else a full System Admin.

### Customizations
To target a specific institution role, update [institution_role] under the Restriction List.

