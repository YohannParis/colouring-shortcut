#!/bin/bash
PROMPT="Create a printable coloring image in black and white, for kids to fill the empty spaces. Keep it simple. Use the following idea: __input__"
FINAL_PROMPT="${PROMPT//__input__/$1}"
curl -s -X POST "https://api.openai.com/v1/images/generations" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -H "Content-type: application/json" \
    -d "{
       \"model\": \"gpt-image-1\",
       \"prompt\": \"$FINAL_PROMPT\"\
    }" | jq -r '.data[0].b64_json' | base64 -D | lpr
