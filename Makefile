#!/bin/bash
set -e

echo "⚙️  Creating trigger files for CI/CD..."

# Tạo file trigger giả
date > .trigger-backend
date > .trigger-frontend
date > .trigger-airflow

git add .trigger-backend .trigger-frontend .trigger-airflow
git commit -m "ci: trigger full CI/CD via dummy trigger files"
git push

echo "✅ CI/CD triggered via trigger files!"
