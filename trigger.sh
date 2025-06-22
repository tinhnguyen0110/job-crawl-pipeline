#!/bin/bash
set -e
# Danh sách component cần trigger (mặc định là cả 3)
components=("$@")
if [ ${#components[@]} -eq 0 ]; then
  components=("backend" "frontend" "airflow")
fi

echo "⚙️  Creating trigger files for CI/CD..."
created_files=()

for comp in "${components[@]}"; do
  file=".trigger-$comp"
  echo "⏳ Triggering $comp..."
  date > "$file"
  created_files+=("$file")
done

git add .
git commit -m "ci: trigger build for ${components[*]}"
git push origin main

echo "✅ CI/CD triggered via: ${created_files[*]}"