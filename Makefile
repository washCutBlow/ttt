build:
	python3 setup.py bdist_wheel

clean:
	python3 setup.py clean --all
	rm -r dist
	rm -r *.egg-info