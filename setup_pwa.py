#!/usr/bin/env python3
"""
PWA Setup Script for WisdomWeaver
This script helps configure and deploy the PWA components
"""

import os
import shutil
import json
from pathlib import Path

def check_files():
    """Check if all required PWA files exist"""
    required_files = [
        'manifest.json',
        'sw.js',
        'pwa.html',
        'static/icon-192.png',
        'static/icon-512.png'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    return missing_files

def validate_manifest():
    """Validate the manifest.json file"""
    try:
        with open('manifest.json', 'r') as f:
            manifest = json.load(f)
        
        required_fields = ['name', 'short_name', 'start_url', 'display', 'icons']
        missing_fields = [field for field in required_fields if field not in manifest]
        
        if missing_fields:
            print(f"❌ Missing required manifest fields: {missing_fields}")
            return False
        
        print("✅ Manifest.json is valid")
        return True
        
    except Exception as e:
        print(f"❌ Error validating manifest: {e}")
        return False

def setup_icons():
    """Check if all required icon sizes exist"""
    icon_sizes = ['72', '96', '128', '144', '152', '192', '384', '512']
    static_dir = Path('static')
    
    if not static_dir.exists():
        print("❌ Static directory not found")
        return False
    
    missing_icons = []
    for size in icon_sizes:
        icon_file = static_dir / f'icon-{size}.png'
        if not icon_file.exists():
            missing_icons.append(f'icon-{size}.png')
    
    if missing_icons:
        print(f"⚠️  Missing icon files: {missing_icons}")
        print("   Please ensure all icon sizes are present in /static/ directory")
        return False
    
    print("✅ All required icons are present")
    return True

def check_streamlit_config():
    """Check if Streamlit is configured for PWA"""
    config_dir = Path.home() / '.streamlit'
    config_file = config_dir / 'config.toml'
    
    if config_file.exists():
        with open(config_file, 'r') as f:
            content = f.read()
            if 'enableStaticServing = true' in content:
                print("✅ Streamlit static serving is enabled")
                return True
    
    print("⚠️  Streamlit static serving not configured")
    print("   Add this to ~/.streamlit/config.toml:")
    print("   [server]")
    print("   enableStaticServing = true")
    return False

def generate_deployment_commands():
    """Generate deployment commands for different platforms"""
    print("\n🚀 Deployment Commands:")
    print("\n1. For Streamlit Cloud:")
    print("   - Upload your repository to GitHub")
    print("   - Connect to Streamlit Cloud")
    print("   - Ensure requirements.txt includes all dependencies")
    
    print("\n2. For Heroku:")
    print("   - Add Procfile: 'web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0'")
    print("   - Configure static file serving")
    
    print("\n3. For local testing:")
    print("   streamlit run app.py --server.enableStaticServing=true")

def main():
    """Main setup function"""
    print("🕉️  WisdomWeaver PWA Setup Check")
    print("=" * 40)
    
    # Check required files
    missing_files = check_files()
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    else:
        print("✅ All PWA files are present")
    
    # Validate manifest
    if not validate_manifest():
        return False
    
    # Check icons
    if not setup_icons():
        return False
    
    # Check Streamlit config
    check_streamlit_config()
    
    # Generate deployment info
    generate_deployment_commands()
    
    print("\n✅ PWA setup complete!")
    print("\n📱 Your app will be installable when deployed with HTTPS")
    print("🌐 Visit /pwa.html for the PWA landing page")
    print("📋 The install button will appear in the sidebar")
    
    return True

if __name__ == "__main__":
    main()
