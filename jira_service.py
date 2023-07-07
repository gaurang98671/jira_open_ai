import requests
from jira import JIRA
from requests.auth import HTTPBasicAuth
import json

class Jira_service:
    def __init__(self, token, email):
        self.token = token
        self.email = email
        self.headers = {'Content-Type' : 'application/json;charset=iso-8859-1'}
        self.base_url = "https://deeeznuts.atlassian.net/rest/api/2/"
        self.auth = HTTPBasicAuth(email, token)

    def fetch(self, url):
        response = requests.get(url, headers=self.headers, auth=self.auth)
        return json.loads(response.text)
        
    def get_jira(self, jira_id):
        
        url = self.base_url + "issue/" + jira_id
        response = self.fetch(url)

        project_name = response["fields"]["project"]["name"]
        project_key = response["fields"]["project"]["key"]
        priority = response["fields"]["priority"]["name"]
        labels = response["fields"]["labels"]
        status = response["fields"]["status"]["name"]
        description = response["fields"]["description"]
        summary = response["fields"]["summary"]
        reporter = response["fields"]["reporter"]["emailAddress"]
        reporter_name = response["fields"]["reporter"]["displayName"]
        comments = response["fields"]["comment"]["comments"]
        comments = [{"email" : x["author"]["emailAddress"], "comment" : x["body"], "commented_on" : x["created"], "display_name" : x["author"]["displayName"]} for x in comments]
        linked_issues = response["fields"]["issuelinks"]
        assignee = response["fields"]["assignee"]
        created_on = response["fields"]["created"]
        ticket_logs = self.get_ticket_logs(jira_id)

        data = {
        'Issue Id' : jira_id,
        'Project Name' : project_name, 
        'Project key' : project_key,
        'Priority' : priority,
        'Labels' : labels,
        'Status' : status,
        'Description' : description,
        'Summary' : summary,
        'Reporter' : reporter,
        'Reporter name' : reporter_name,
        'Comments' : comments,
        'Linked issues' : linked_issues,
        'Assigned to' : assignee,
        'Created_on' : created_on,
        'Record type' : "jira",
        'Ticket logs' : ticket_logs
        }

        return data
        


    def get_all_issues(self, project_key):
        
        url = self.base_url + "search?jql=project=" + project_key
        
        response = self.fetch(url)

        issues = [x["key"] for x in response["issues"]]
        
        return issues
    
    def get_ticket_logs(self, jira_id):
        
        url = "{}issue/{}/changelog".format(self.base_url, jira_id)
        response = self.fetch(url)
        logs = []

        for i in response['values']:
            auth_name = i['author']['displayName']
            created_date = i['created'].split("T")[0]        
            for change in i['items']:
                logs.append("User {} changed {} from {} to {} on {}".format(auth_name, change['field'], change['from'], change['toString'], created_date))

        return logs
    
    def add_to_db(self, vectorstore, data):
        vectorstore.add_texts(data)


    def add_by_project_id(self, vectorstore, project_key):
        issues = self.get_all_issues(project_key)
        issue_data = [str(self.get_jira(x)) for x in issues]
        self.add_to_db(vectorstore, issue_data)