# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "collection"
app_title = "Collection"
app_publisher = "wayzon"
app_description = "App for society"
app_icon = "icon-inr"
app_color = "red"
app_email = "info@wayzon.com"
app_version = "0.0.1"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/collection/css/collection.css"
# app_include_js = "/assets/collection/js/collection.js"

# include js, css files in header of web template
# web_include_css = "/assets/collection/css/collection.css"
# web_include_js = "/assets/collection/js/collection.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "collection.install.before_install"
# after_install = "collection.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "collection.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
 	"all": [
 		"collection.collection.tasks.all"
 	],
 #	"daily": [
 #		"collection.collection.add_owner.add_owner.mail_send"
 #	],
 	"hourly": [
 		"collection.collection.tasks.hourly"
	],
# 	"weekly": [
# 		"collection.tasks.weekly"
# 	],
# 	"monthly": [
#		"collection.tasks.monthly"
# 	]
 }

# Testing
# -------

# before_tests = "collection.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "collection.event.get_events"
# }

