name: Environment Variable Check

on:
  workflow_dispatch:
  push:
    branches:
      - main

jobs:
  env-check:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install python-dotenv

      - name: Run env validation
        env:
          AZURE_OPENAI_ENDPOINT: ${{ secrets.AZURE_OPENAI_ENDPOINT }}
          AZURE_OPENAI_API_KEY: ${{ secrets.AZURE_OPENAI_API_KEY }}
          AZURE_OPENAI_API_VERSION: ${{ secrets.AZURE_OPENAI_API_VERSION }}
          AZURE_LOCATION: ${{ secrets.AZURE_LOCATION }}

          AZURE_OPENAI_DEPLOYMENT_ORCHESTRATOR: ${{ secrets.AZURE_OPENAI_DEPLOYMENT_ORCHESTRATOR }}
          AZURE_OPENAI_DEPLOYMENT_CLASSIFIER: ${{ secrets.AZURE_OPENAI_DEPLOYMENT_CLASSIFIER }}
          AZURE_OPENAI_DEPLOYMENT_HR: ${{ secrets.AZURE_OPENAI_DEPLOYMENT_HR }}
          AZURE_OPENAI_DEPLOYMENT_IT: ${{ secrets.AZURE_OPENAI_DEPLOYMENT_IT }}
          AZURE_OPENAI_DEPLOYMENT_FINANCE: ${{ secrets.AZURE_OPENAI_DEPLOYMENT_FINANCE }}
          AZURE_OPENAI_DEPLOYMENT_ARCHITECT: ${{ secrets.AZURE_OPENAI_DEPLOYMENT_ARCHITECT }}
          AZURE_OPENAI_DEPLOYMENT_SECURITY: ${{ secrets.AZURE_OPENAI_DEPLOYMENT_SECURITY }}
          AZURE_OPENAI_DEPLOYMENT_OPS: ${{ secrets.AZURE_OPENAI_DEPLOYMENT_OPS }}

        run: python backend/check_env.py
