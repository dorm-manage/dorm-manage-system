# CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy to Railway
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: railway/cli@v1
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
```
