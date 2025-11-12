#!/bin/bash
# Setup script for deploying the Cosmic Trader on a server

echo "🌙 ✨ Setting up Autonomous Cosmic Trader ✨ 🌙"
echo ""

# Update system
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and dependencies
echo "🐍 Installing Python 3.11..."
sudo apt-get install -y python3.11 python3.11-venv python3-pip git

# Create virtual environment
echo "🌟 Creating virtual environment..."
python3.11 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📚 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Install aster connector
echo "⚡ Installing AsterDEX connector..."
git clone https://github.com/asterdex/aster-connector-python.git /tmp/aster-connector
cd /tmp/aster-connector && pip install .
cd -

# Create log directory
mkdir -p logs

# Set up systemd service (optional)
echo ""
echo "Would you like to set up systemd service for auto-start? (y/n)"
read -r setup_systemd

if [ "$setup_systemd" = "y" ]; then
    echo "📝 Setting up systemd service..."

    # Update service file with correct paths
    CURRENT_DIR=$(pwd)
    VENV_PYTHON="$CURRENT_DIR/venv/bin/python"

    sed -i "s|User=your-username|User=$USER|g" cosmic-trader.service
    sed -i "s|WorkingDirectory=/path/to/aster-dex|WorkingDirectory=$CURRENT_DIR|g" cosmic-trader.service
    sed -i "s|/path/to/venv/bin/python|$VENV_PYTHON|g" cosmic-trader.service
    sed -i "s|/path/to/aster-dex|$CURRENT_DIR|g" cosmic-trader.service

    # Copy service file
    sudo cp cosmic-trader.service /etc/systemd/system/

    # Enable and start service
    sudo systemctl daemon-reload
    sudo systemctl enable cosmic-trader.service

    echo ""
    echo "✅ Systemd service installed!"
    echo ""
    echo "To start the bot:"
    echo "  sudo systemctl start cosmic-trader"
    echo ""
    echo "To check status:"
    echo "  sudo systemctl status cosmic-trader"
    echo ""
    echo "To view logs:"
    echo "  tail -f cosmic_trader.log"
    echo ""
fi

echo ""
echo "🌙 ✨ Setup Complete! ✨ 🌙"
echo ""
echo "To run manually:"
echo "  source venv/bin/activate"
echo "  python autonomous_cosmic_trader.py"
echo ""
echo "Or with Docker:"
echo "  docker-compose up -d"
echo ""
echo "May the cosmos guide your trades! 🚀"
