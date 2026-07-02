# Autoinfo Company Knowledge Platform

## Features
- Department-based knowledge hub
- Role and classification based security
- File upload and scan ingestion
- OCR extraction queue hook
- Permission-first search
- AI answer with citation

## Install
1. Copy module to `c:\odoo\addons_autoinfo\custom15_autoinfo`
2. Update `addons_path` in `c:\odoo\odoo-15.0\odoo.conf`
3. Run `c:\odoo\odoo-15.0\.venv\Scripts\python.exe c:\odoo\odoo-15.0\odoo-bin -c c:\odoo\odoo-15.0\odoo.conf -d <db_name> -i autoinfo_company_knowledge_platform --stop-after-init`

## Rollout
1. Seed departments and knowledge types
2. Assign `Knowledge Viewer`, `Knowledge Contributor`, `Knowledge Reviewer`, `Knowledge Department Manager`, `Knowledge Admin`
3. Publish one SOP, one FAQ, and one scanned policy as pilot content
4. Validate search and AI citations with users from two departments
5. Review unauthorized access scenarios before expanding to restricted content
