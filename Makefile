build:
	poetry build
install:
	poetry install
	pip install dist/*.whl
signin:
	poetry config pypi-token.pypi ${PYPI_TOKEN}
publish:
	poetry publish
