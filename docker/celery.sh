#!/bin/bash

celery --app=tasks.celery:celeryApp worker -l INFO
