docker-compose run web sh -c "python link_shortener/core/wait_for_db.py && \
  python link_shortener/core/run_migration.py && \
  pytest --disable-pytest-warnings && \
  flake8"
