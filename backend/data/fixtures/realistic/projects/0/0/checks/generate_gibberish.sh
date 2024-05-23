#!/bin/bash

# generate gibberish logs

# Function to generate a random sequence of characters
generate_sequence() {
    cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 50
    echo ""
}

# Counter
count=1

# Generating 50 random character sequences on each line
while [ $count -le 50 ]; do
    generate_sequence
    count=$((count+1))
done

# Generate an artifact

wget https://upload.wikimedia.org/wikipedia/commons/5/5e/Logo_UGent_NL_RGB_2400_kleur-op-wit.png -P artifacts
