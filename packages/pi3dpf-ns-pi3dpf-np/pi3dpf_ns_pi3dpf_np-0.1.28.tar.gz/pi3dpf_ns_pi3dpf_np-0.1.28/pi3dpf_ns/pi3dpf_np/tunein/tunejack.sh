#!/bin/bash
# From: https://gist.github.com/xndc/c732204e274743204f1f

# tunejack.sh uses the TuneIn public API (at opml.radiotime.com) to search for
# a radio station, print out its details and try to play it somehow.

if [ "$#" -eq 0 ]; then
	echo "$0: search for a radio station using the TuneIn API"
	echo "Usage: $0 PATTERN"
	exit 1
fi

# Grab the search pattern.
PATTERN="$*"

# Helper function for encoding a URL.
# See http://stackoverflow.com/questions/296536/
urlencode() {
	local string="$*"
	local strlen=${#string}
	local encoded=""

	for (( pos=0 ; pos<strlen ; pos++ )); do
		c=${string:$pos:1}
		case "$c" in
			[-_.~a-zA-Z0-9] ) o="${c}" ;;
			* )               printf -v o '%%%02x' "'$c"
		esac
		encoded+="${o}"
	done
	echo "${encoded}"
}

# Ask the API for search results.
# Supports both curl and wget.
API_TARGET="http://opml.radiotime.com/Search.ashx?query=$(urlencode $PATTERN)"

if which curl > /dev/null; then
	API_RESPONSE=$(curl --silent $API_TARGET)
elif which wget > /dev/null; then
	API_RESPONSE=$(wget --quiet --output-document=- $API_TARGET)
else
	echo "Error: script requires curl or wget installed."
	exit 1
fi

# Try to grab the first <outline> element from the response.
# It has to have attributes type="audio" and item="station".
# Discard results containing key="unavailable" - they're useless stubs.
API_RESULT_TAG=$(echo "$API_RESPONSE" \
	| grep '<outline type="audio"' \
	| grep 'item="station"' \
	| grep -v 'key="unavailable"' \
	| head -n 1)

if [[ "$API_RESULT_TAG" == "" ]]; then
	echo "No radio stations found."
	exit
else
	# Split the <outline> tag into multiple lines, so we can grep for each
	# XML attribute.
	API_RESULT_TAG=$(echo "$API_RESULT_TAG" | sed 's/" /"\n/g')

	# Helper function to extract a tag.
	# The sed is because we're not actually decoding XML, and things like
	# apostrophes are represented by HTML entities like &apos;.
	extract_tag() {
		TAG="${1}"
		echo "$API_RESULT_TAG" | grep "^$TAG=" | cut -d '"' -f 2 \
			| sed "s/&apos;/\'/g"
	}
	# Display the details we're interested in - name, subtext, URL.
	echo "$(extract_tag text)"
	echo "$(extract_tag subtext)"
	echo "$(extract_tag URL)"
	# Throw the URL in a variable for later purposes.
	API_URL="$(extract_tag URL)"
fi

# Get the actual server URL.
if which curl > /dev/null; then
	URL=$(curl --silent $API_URL)
elif which wget > /dev/null; then
	URL=$(wget --quiet -O - $API_URL)
fi

# Try and find a media player.
# Run GUI apps in the background - see http://superuser.com/questions/177218
if which mplayer > /dev/null; then
	mplayer $URL
elif which mpg123 > /dev/null; then
	mpg123 $URL
elif which vlc > /dev/null; then
	(vlc $URL &> /dev/null &)
elif which totem > /dev/null; then
	(totem $URL &> /dev/null &)
elif which audacious > /dev/null; then
	(audacious $URL &> /dev/null &)
elif which xdg-open > /dev/null; then
	# This will usually just open the stream status page.
	xdg-open $URL
fi
