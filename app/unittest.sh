for f in tests/test_*.py
do
	echo "Testing $f"
	python -m unittest $f
done

