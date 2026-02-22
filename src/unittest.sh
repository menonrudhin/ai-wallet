for f in tests/test_*.py
do
	python -m unittest $f
done

