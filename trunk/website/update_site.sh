#!/bin/sh

# syncs remote site with local version
# -z use compression
# --delete delete files not present on sender's side
# -u only update remote site 
# -v verbose
# -e ssh use ssh as shell
# -r recursive directories
rsync -z --delete -u -v -e ssh -r site/* ibooij@berlios:/home/groups/hac4trainer/htdocs
