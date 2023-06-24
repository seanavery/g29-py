build:
	poetry build
install:
	poetry install
	pip install dist/*.whl
test:
	poetry run pytest -s --log-cli-level=DEBUG
signin:
	poetry config pypi-token.pypi ${PYPI_TOKEN}
publish:
	poetry publish
