#!/usr/bin/env bash
ARGS=$1
COMMIT_MSG=`head -n1 $ARGS`
PATTERN="^(feat|fix|ci|docs|settings|template|build|merge):+[[:space:]]+.+"
if ! [[ "$COMMIT_MSG" =~ $PATTERN ]]; then
    echo "Bad commit message '$COMMIT_MSG'. It must be in the format of 'feat: message' or 'fix: message' or
    'ci: message' or 'docs: message' or 'settings: message' or 'template: message' or 'build: message' or
    'merge: message'"
    exit 1
fi
