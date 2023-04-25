from googleapiclient import discovery
import json

API_KEY = "AIzaSyCiHLACkA36E_tWcaWz8WbXtLdjLiRE6ew"

client = discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=API_KEY,
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
)

def is_offensive(text):
  analyze_request = {
    'comment': { 'text': text },
    'requestedAttributes': {'TOXICITY': {}}
  }

  response = client.comments().analyze(body=analyze_request).execute()
  response = response['attributeScores']['TOXICITY']['summaryScore']['value']
  if response >= 0.5: return 1
  return 0