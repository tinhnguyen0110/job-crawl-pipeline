# Makefile for triggering CI/CD by creating .trigger-* files

.PHONY: all backend frontend airflow

TRIGGER_SCRIPT=./trigger.sh

# Default: trigger all components
all:
	$(TRIGGER_SCRIPT)

backend:
	$(TRIGGER_SCRIPT) backend

frontend:
	$(TRIGGER_SCRIPT) frontend

airflow:
	$(TRIGGER_SCRIPT) airflow
