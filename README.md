Incident Uploader to Supabase
Overview
This script uploads incident data from a SQLite database to a Supabase server using Remote Procedure Calls (RPC). It maps device information, categorizes incidents, and ensures secure communication with the server. Data deletion options are included for cleanup post-upload.

Features
Fetch and transform device metadata from Supabase.

Classify incidents as Minor or Major based on risk level.

Securely upload data to Supabase via RPC endpoints.

Optional SQLite data cleanup after upload.

Prerequisites
Python 3.8+

Libraries: pandas, numpy, sqlite3, supabase, requests, python-dateutil

Supabase project URL and API key.

SQLite database with an incidents table.

Setup
Install Dependencies

bash
pip install pandas numpy sqlite3 supabase requests python-dateutil
Configuration

Replace placeholder values in the script (e.g., ******.db, supabase_url, supabase_key).

Ensure the devices table in Supabase contains id, secret, vehicle_id, and company_id columns.

Environment Variables (Optional)
Store sensitive data (e.g., Supabase credentials) in a global_config.json file or environment variables.

Usage
Run the Script

bash
python incident_upload_rpc.py
Upload Process

The script connects to SQLite and Supabase.

Incident data is mapped to device/company metadata.

Records are uploaded individually via RPC.

Post-Upload Cleanup
Uncomment the SQLite deletion block (Option 1 or 2) if needed.

Security Notes
🔒 Do not commit credentials (e.g., supabase_key, SQLite paths) to version control.

Use environment variables or config files excluded via .gitignore.

Troubleshooting
400 Errors: Verify device secret and id mappings in the devices table.

Database Issues: Check SQLite connection paths and table schemas.

Note: Customize placeholders (e.g., ******) and test in a development environment before production use.
