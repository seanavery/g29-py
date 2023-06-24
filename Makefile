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
udev:
	echo 'KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0664", GROUP="plugdev"' | sudo tee /etc/udev/rules.d/99-hidraw-permissions.rules
	sudo udevadm control --reload-rules
