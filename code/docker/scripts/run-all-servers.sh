#!/usr/bin/env sh

echo "Starting DB init.."
coal_content_db_init -c /config/coal-contentserver.conf
coal_game_db_init -c /config/coal-gameserver.conf
coal_player_db_init -c /config/coal-playerserver.conf

echo "Starting servers..."
gunicorn --bind 0.0.0.0:8000 'coal_public_api_server.wsgi:main(config="/config/coal-apiserver.conf")' &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start API server: $status"
  exit $status
fi

gunicorn --bind 0.0.0.0:8200 'coal_content_server.wsgi:main(config="/config/coal-contentserver.conf")' &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start API server: $status"
  exit $status
fi

coal_game_server -c /config/coal-gameserver.conf &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start API server: $status"
  exit $status
fi

coal_player_server -c /config/coal-playerserver.conf &
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start API server: $status"
  exit $status
fi

coal_slackbot &
coal_discord &

while sleep 2; do
  ps aux |grep coal_public_api_server |grep -q -v grep
  PROCESS_1_STATUS=$?

  ps aux |grep coal_content_server |grep -q -v grep
  PROCESS_2_STATUS=$?

  ps aux |grep coal_game_server |grep -q -v grep
  PROCESS_3_STATUS=$?

  ps aux |grep coal_player_server |grep -q -v grep
  PROCESS_4_STATUS=$?

  ps aux |grep coal_player_server |grep -q -v grep
  PROCESS_5_STATUS=$?

  if [ $PROCESS_1_STATUS -ne 0 -o $PROCESS_2_STATUS -ne 0 -o $PROCESS_3_STATUS -ne 0 -o $PROCESS_4_STATUS -ne 0 -o $PROCESS_5_STATUS -ne 0 ]; then
    echo "Something died :("
    exit 1
  fi
done