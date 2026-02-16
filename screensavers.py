# Add to ~/.bashrc
if [ -z "$SSH_CLIENT" ] && [ -z "$SSH_TTY" ]; then
    # Only run on local console
    python3 /home/lucas/screensavers/s-save1.py
fi
