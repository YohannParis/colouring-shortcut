# Coloring Page HTTP Server Setup

## Step 1: Save Your Files

1. **Save your coloring script** as `~/coloring_script.sh`:

2. **Make the script executable**:
```bash
chmod +x ~/coloring_script.sh
```

3. **Save the Python server** as `~/coloring_server.py`

4. **Make the server executable**:
```bash
chmod +x ~/coloring_server.py
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

4. **Test via HTTP** (in another terminal):
```bash
curl "http://localhost:8080?idea=dinosaur"
```

## Step 3: Set Up Auto-Start on macOS

1. **Edit the LaunchAgent file** (from the second artifact):
   - Replace `YOUR_USERNAME` with your actual username
   - Replace `YOUR_OPENAI_API_KEY_HERE` with your actual API key
   - Adjust file paths if you saved files elsewhere

2. **Save the plist file**:
```bash
# Replace YOUR_USERNAME with your actual username
cp com.user.coloring-server.plist ~/Library/LaunchAgents/
```

3. **Load the service**:
```bash
launchctl load ~/Library/LaunchAgents/com.user.coloring-server.plist
```

4. **Start the service**:
```bash
launchctl start com.user.coloring-server
```

### Restart the service:
```bash
launchctl unload ~/Library/LaunchAgents/com.user.coloring-server.plist
launchctl load ~/Library/LaunchAgents/com.user.coloring-server.plist
```

5. **Check if it's running**:
```bash
launchctl list | grep coloring-server
```

## Step 4: Usage

Once set up, you can generate coloring pages by visiting:

- `http://localhost:8080?idea=dinosaur`
- `http://localhost:8080?idea=princess%20castle`
- `http://localhost:8080?idea=fire%20truck`
- `http://localhost:8080?idea=ocean%20animals`

The server will:
1. Take your idea
2. Generate a coloring page using OpenAI
3. Send it directly to your printer
4. Return a JSON response confirming success

## Requirements

- macOS with Python 3
- OpenAI API key
- `jq` installed (`brew install jq`)
- Connected printer
- `curl` and `base64` (usually pre-installed)

## Security Notes

- The server only accepts GET requests
- It only runs your predefined coloring script
- API key is stored in the plist file (consider using Keychain for production)
- Server runs on localhost only (not accessible from network)
