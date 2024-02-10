#!/bin/bash

celery --app=tasks.celery:celeryApp flower
