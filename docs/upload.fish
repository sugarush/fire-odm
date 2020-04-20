#!/usr/bin/env fish

cd _build/html

AWS_PROFILE=sugarush aws s3 cp --recursive . s3://sugar-odm-docs-sugarush-io/
