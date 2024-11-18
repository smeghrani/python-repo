from fastapi import APIRouter, HTTPException
from src.modules.jira.jira_implementation import JiraClient
import requests

router = APIRouter(
    tags=["JIRA"],
    responses={
        200: {"description": "Success"},
        400: {"description": "Bad Request"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"}
    }
)

jira_client = JiraClient()

@router.get("/tickets/")
async def get_tickets(project_key: str):
    """
    API endpoint to fetch a list of tickets from a Jira project.
    :param project_key: The key of the Jira project (e.g., "TEST").
    :return: JSON response with the list of tickets.
    """
    try:
        tickets = jira_client.get_tickets(project_key)
        return tickets
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ticket/{ticket_id}/")
async def get_ticket(ticket_id: str):
    """
    API endpoint to fetch details of a single Jira ticket.
    :param ticket_id: The ID or key of the Jira ticket (e.g., "TEST-1").
    :return: JSON response with ticket details.
    """
    try:
        ticket = jira_client.get_issue(ticket_id)
        return ticket
    except requests.HTTPError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))