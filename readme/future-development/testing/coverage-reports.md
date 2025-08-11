# Coverage Reports

After running tests with coverage, view the HTML report:

```bash
# Generate coverage report
pytest --cov=DormitoriesPlus --cov-report=html

# Open coverage report
open htmlcov/index.html
```

The coverage report shows:

* Overall coverage percentage
* Line-by-line coverage details
* Missing coverage areas
* Branch coverage information
