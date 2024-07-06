#!/bin/sh

gray todo-list \
    -f add-trailing-comma,autoflake,fixit,isort,pyupgrade,trim,unify,black \
    --isort-line-length 120 \
    --black-line-length 120
