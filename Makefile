py_dirs := site2graph
py_files = $(wildcard site2graph/*.py) $(wildcard site2graph/spiders/*.py)

.PHONY: fmt
fmt: env_ok
	env/bin/isort -sp .isort.cfg $(py_dirs)
	env/bin/black $(py_files)

.PHONY: test
test: check
	env/bin/python -m twisted.trial $(py_dirs)

.PHONY: check
check: env_ok
	env/bin/python -m mypy \
		--check-untyped-defs \
		--ignore-missing-imports \
		$(py_dirs)
	env/bin/python -m flake8 --select F $(py_dirs)
	env/bin/isort  -sp .isort.cfg  $(py_dirs) --check
	env/bin/black --check $(py_files)


env_ok: requirements.txt
	rm -rf env env_ok
	python3 -m venv env
	env/bin/pip install -r requirements.txt
	touch env_ok


.PHONY: clean
clean:
	rm -rf env env_ok test_env
