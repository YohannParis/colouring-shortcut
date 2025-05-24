# Coloring Page HTTP Server Setup

## Step 1: Make the files executable

```bash
chmod +x coloring_script.sh
chmod +x coloring_server.py
```

## Step 2: Test Your Setup

1. **Set your OpenAI API key**:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

2. **Test the script manually**:
```bash
~/coloring_script.sh "dinosaur"
```

3. **Test the server**:
```bash
python3 ~/coloring_server.py
```

4. **Test via HTTP** (in another terminal or from another device on your network):
```bash
# Local testing
curl "http://localhost:8080?idea=dinosaur"

# Test from another device using your computer's Bonjour name
# Replace "YourComputerName" with your actual computer name
curl "http://YourComputerName.local:8080?idea=dinosaur"
```

## Step 3: Set Up Auto-Start on macOS

1. **Edit the LaunchAgent file** (from the second artifact):
   - Replace `YOUR_USERNAME` with your actual username
   - Replace `YOUR_OPENAI_API_KEY_HERE` with your actual API key
   - Adjust file paths if you saved files elsewhere

2. **Save the plist file**:
```bash
# Replace YOUR_USERNAME with your actual username
sudo cp com.user.coloring-server.plist /Library/LaunchAgents/
```

3. **Load the service**:
```bash
launchctl load /Library/LaunchAgents/com.user.coloring-server.plist
```

4. **Start the service**:
```bash
launchctl start com.user.coloring-server
```

5. **Check if it's running**:
```bash
launchctl list | grep coloring-server
```

## Step 5: Configure Firewall (Important!)

To allow network access, you need to configure your Mac's firewall:

### Method 1: System Preferences (Recommended)
1. Go to **System Preferences > Security & Privacy > Firewall**
2. Click the **lock icon** and enter your password
3. If firewall is off, you can leave it off for LAN access
4. If firewall is on:
   - Click **"Firewall Options"**
   - Click **"+"** to add an application
   - Navigate to and select **Python** (`/usr/bin/python3`)
   - Set it to **"Allow incoming connections"**
   - Click **OK**

### Method 2: Command Line
```bash
# Allow Python through firewall
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /usr/bin/python3
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --unblockapp /usr/bin/python3
```

### Method 3: Disable Firewall (Less Secure)
```bash
# Only if you're on a trusted network
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off
```

## Step 4: Usage

Once set up, you can generate coloring pages from any device on your local network:

**From the same computer:**
- `http://localhost:8080?idea=dinosaur`

**From other devices on your network (phones, tablets, other computers):**
- `http://YourComputerName.local:8080?idea=dinosaur`
- `http://YourComputerName.local:8080?idea=princess%20castle`
- `http://YourComputerName.local:8080?idea=fire%20truck`
- `http://YourComputerName.local:8080?idea=ocean%20animals`

Replace "YourComputerName" with your Mac's actual computer name (found in System Preferences > Sharing).

The server will:
1. Take your idea from any device on the network
2. Generate a coloring page using OpenAI
3. Send it directly to the printer connected to your Mac
4. Return a JSON response confirming success

## Finding Your Computer's Bonjour Name

1. **System Preferences method:**
   - Go to System Preferences > Sharing
   - Look for "Computer Name" at the top
   - Your Bonjour name will be that name + ".local"

2. **Terminal method:**
```bash
scutil --get ComputerName
# Or
hostname
```

3. **The server will also display the Bonjour name when it starts**

## Troubleshooting

### Check server logs:
```bash
tail -f ~/coloring_server.log
tail -f ~/coloring_server_error.log
```

### Stop the service:
```bash
launchctl stop com.user.coloring-server
launchctl unload ~/Library/LaunchAgents/com.user.coloring-server.plist
```

### Restart the service:
```bash
launchctl unload ~/Library/LaunchAgents/com.user.coloring-server.plist
launchctl load ~/Library/LaunchAgents/com.user.coloring-server.plist
```

### Check if service is loaded:
```bash
launchctl list | grep coloring
```

## Requirements

- macOS with Python 3
- OpenAI API key
- `jq` installed (`brew install jq`)
- Connected printer
- `curl` and `base64` (usually pre-installed)
- **Network firewall configured to allow incoming connections on port 8080**

## Security Notes

- The server accepts GET requests from any device on your local network
- It only runs your predefined coloring script
- API key is stored in the plist file (consider using Keychain for production)
- Server is accessible to anyone on your local network (LAN)
- Consider setting up router-level access controls if needed
- Port 8080 needs to be open in your Mac's firewall
