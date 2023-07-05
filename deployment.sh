gcloud builds submit --tag gcr.io/linkedinconsulcode/tgi-openai2
gcloud run deploy --image gcr.io/linkedinconsulcode/tgi-openai2 --platform managed --set-env-vars OPENAI_KEY=<YOUR_KEY>
