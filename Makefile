build:
	poetry build
install:
	poetry install
	pip install dist/*.whl
publish:
	poetry publish
