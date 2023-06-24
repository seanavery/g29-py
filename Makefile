build:
	poetry build
install:
	poetry install
	pip install dist/*.whl
test:
	poetry run pytest -s
signin:
	poetry config pypi-token.pypi ${PYPI_TOKEN}
publish:
	poetry publish
