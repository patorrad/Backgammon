LOG='log.txt '
if test -f "$LOG"; then
    rm "$FILE"
fi
python gamemaster.py > log.txt