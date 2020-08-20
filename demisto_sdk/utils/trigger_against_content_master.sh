#!/usr/bin/env bash

_branch=$1
_circle_token=$2
trigger_build_url=https://circleci.com/api/v2/project/github/demisto/demisto-sdk/pipeline

post_data=$(cat <<EOF
{
  "branch": "${_branch}",
  "parameters": {
    "FAKE_MASTER": "true"
  }
}
EOF)

curl \
--header "Accept: application/json" \
--header "Content-Type: application/json" \
--data "${post_data}" \
--request POST ${trigger_build_url}
--user "$_circle_token:"
