#!/bin/bash

# WisdomWeaver PWA Startup Script
echo "🕉️  Starting WisdomWeaver with PWA Support"
echo "=" * 50

# Create Streamlit config directory if it doesn't exist
mkdir -p ~/.streamlit

# Create Streamlit config for PWA support
cat > ~/.streamlit/config.toml << 'EOF'
[server]
enableStaticServing = true
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#ff6b35"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
EOF

echo "✅ Streamlit configured for PWA support"

# Check if all PWA files exist
echo "🔍 Checking PWA files..."
python3 setup_pwa.py

echo ""
echo "🚀 Starting WisdomWeaver..."
echo "📱 The app will be installable as a PWA!"
echo "🌐 Look for the install button in your browser"
echo "📋 Install option available in sidebar"
echo ""

# Start the Streamlit app with PWA support
streamlit run app.py --server.enableStaticServing=true
