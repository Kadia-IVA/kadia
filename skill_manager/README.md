
## Deployment to GCP
```shell
PROJECT_ID=majestic-disk-281618
IMAGE=skill_manager

gcloud builds submit . --tag gcr.io/$PROJECT_ID/$IMAGE
```

### Local deployment
```shell
uvicorn run:app --port 8081
```
