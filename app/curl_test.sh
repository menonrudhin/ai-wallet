curl -X POST http://localhost:8000/upload \
  -F "files=@./jan.pdf" \
    --output report.pdf
