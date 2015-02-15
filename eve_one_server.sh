#!/usr/bin/env bash

if [ -z $1 ]
  then
    echo "Usage: $0 {start|stop|restart|status}"
fi

NAME="eve_one_server"
PATH_TO_APP="/opt/eveonescratch"
COMMAND="$1"
PID_FILE="/var/run/$NAME.pid"
OUT_LOG="/var/log/$NAME.log"
ERR_LOG="/var/log/$NAME.err"


get_pid(){
    cat "$PID_FILE"
}

is_running(){
    [ -f "$PID_FILE" ] && ps `get_pid` > /dev/null 2>&1
}


case "$COMMAND" in
    start)
        if is_running; then
            echo "Already started"
        else
            echo "Starting $NAME"
            cd "$PATH_TO_APP"
            sudo python eve_one_mesh.py >> "$OUT_LOG" 2>>"$ERR_LOG" &
            echo $! > "$PID_FILE"
            if ! is_running; then
                echo "Could not start $NAME, see $OUT_LOG and $ERR_LOG"
                exit 1
            fi
        fi
        ;;
    stop)
        if is_running; then
            echo -n "Stopping $NAME.."
            kill `get_pid`
            for i in {1..10}
            do
                if ! is_running; then
                    break
                fi
                echo -n "."
                sleep 1
            done
            echo

            if is_running; then
                echo "$NAME not stopped; may still be shutting down, or may have failed"
                exit 1;
            else
                echo "Stopped"
                if [ -f "$PID_FILE" ]; then
                    rm "$PID_FILE"
                fi
            fi
        else
            echo "Not running"
        fi
        ;;
    restart)
        $0 stop
        if is_running; then
            echo "Unable to stop, will not attempt to start"
            exit 1
        fi
        $0 start
        ;;
    status)
        if is_running; then
            echo "Running"
        else
            echo "Stopped"
            exit 1
        fi
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

exit 0
